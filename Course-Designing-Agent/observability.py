"""Step-by-step logging for every LLM call and tool call in the pipeline."""
import base64
import json
import logging
import os
import pathlib

from strands.hooks import (
    AfterModelCallEvent,
    AfterToolCallEvent,
    BeforeModelCallEvent,
    BeforeToolCallEvent,
    HookProvider,
    HookRegistry,
)

LOG_PATH = pathlib.Path("logs/pipeline.log")
RAW_LOG_PATH = pathlib.Path("logs/raw_io.log")


def get_logger() -> logging.Logger:
    """Singleton logger writing every pipeline step to logs/pipeline.log."""
    logger = logging.getLogger("kllm_pipeline")
    if not logger.handlers:
        LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        handler = logging.FileHandler(LOG_PATH, encoding="utf-8")
        handler.setFormatter(logging.Formatter("%(asctime)s %(message)s"))
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
        logger.propagate = False
    return logger


def get_raw_logger() -> logging.Logger:
    """Singleton logger writing FULL untruncated request/response JSON to logs/raw_io.log."""
    logger = logging.getLogger("kllm_raw_io")
    if not logger.handlers:
        RAW_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        handler = logging.FileHandler(RAW_LOG_PATH, encoding="utf-8")
        handler.setFormatter(logging.Formatter("%(message)s"))  # we format records ourselves
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
        logger.propagate = False
    return logger


def _message_text(message: dict, limit: int = 4000) -> str:
    """Flatten a Strands content-block message into a single log-friendly string."""
    parts = []
    for block in message.get("content", []):
        if "text" in block:
            parts.append(block["text"])
        elif "toolUse" in block:
            tu = block["toolUse"]
            parts.append(f"[tool_use:{tu['name']}] {json.dumps(tu.get('input', {}))[:limit]}")
        elif "toolResult" in block:
            tr = block["toolResult"]
            text = " ".join(c.get("text", "") for c in tr.get("content", []) if "text" in c)
            parts.append(f"[tool_result:{tr.get('status')}] {text[:limit]}")
    return "\n".join(parts) or "(empty)"


class LLMStepLogger(HookProvider):
    """Attach to an Agent to log every model call and tool call it makes."""

    def __init__(self, agent_name: str, logger: logging.Logger | None = None):
        self.agent_name = agent_name
        self.logger = logger or get_logger()
        self._call_index = 0

    def register_hooks(self, registry: HookRegistry) -> None:
        registry.add_callback(BeforeModelCallEvent, self._before_model_call)
        registry.add_callback(AfterModelCallEvent, self._after_model_call)
        registry.add_callback(BeforeToolCallEvent, self._before_tool_call)
        registry.add_callback(AfterToolCallEvent, self._after_tool_call)

    def _before_model_call(self, event: BeforeModelCallEvent) -> None:
        self._call_index += 1
        self.logger.info(
            f"[{self.agent_name}] LLM call #{self._call_index} -> requesting "
            f"(~{event.projected_input_tokens or '?'} input tokens)"
        )

    def _after_model_call(self, event: AfterModelCallEvent) -> None:
        if event.exception is not None:
            self.logger.error(
                f"[{self.agent_name}] LLM call #{self._call_index} FAILED: {event.exception!r}"
            )
            return
        if event.stop_response is None:
            self.logger.warning(f"[{self.agent_name}] LLM call #{self._call_index} <- no response")
            return
        text = _message_text(event.stop_response.message)
        self.logger.info(
            f"[{self.agent_name}] LLM call #{self._call_index} <- "
            f"stop_reason={event.stop_response.stop_reason}\n{text}"
        )

    def _before_tool_call(self, event: BeforeToolCallEvent) -> None:
        name = event.tool_use.get("name")
        args = json.dumps(event.tool_use.get("input", {}))[:2000]
        self.logger.info(f"[{self.agent_name}] TOOL call -> {name}({args})")

    def _after_tool_call(self, event: AfterToolCallEvent) -> None:
        name = event.tool_use.get("name")
        text = " ".join(c.get("text", "") for c in event.result.get("content", []) if "text" in c)
        self.logger.info(
            f"[{self.agent_name}] TOOL result <- {name} "
            f"status={event.result.get('status')}\n{text[:2000]}"
        )


class RawIOLogger(HookProvider):
    """Attach to an Agent to log the COMPLETE, untruncated request and response
    for every model call to logs/raw_io.log.

    - REQUEST  = the exact content Strands serializes into the Bedrock Converse call:
                 system prompt + tool specs + the full messages array.
    - RESPONSE = the full response message (all content blocks) + stop_reason.

    Nothing is truncated, so you can see exactly what went over the wire.
    """

    def __init__(self, agent_name: str, logger: logging.Logger | None = None):
        self.agent_name = agent_name
        self.logger = logger or get_raw_logger()
        self._call_index = 0

    def register_hooks(self, registry: HookRegistry) -> None:
        registry.add_callback(BeforeModelCallEvent, self._before_model_call)
        registry.add_callback(AfterModelCallEvent, self._after_model_call)

    def _banner(self, header: str) -> str:
        import datetime
        ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        bar = "=" * 100
        return f"\n{bar}\n{ts} | {header}\n{bar}"

    def _dump(self, obj) -> str:
        try:
            return json.dumps(obj, indent=2, ensure_ascii=False, default=str)
        except Exception as e:  # never let logging crash the run
            return f"(could not serialize: {e})\n{obj!r}"

    def _tool_origins(self, agent) -> dict:
        """Map each tool name to its origin: user-defined vs auto-added by Strands.

        - 'function' tools are ones WE passed via tools=[...] (e.g. web_search).
        - 'structured_output' tools are auto-generated by Strands from the Pydantic
          model (e.g. ResearchReport) and registered dynamically at call time.
        """
        origins = {}
        try:
            reg = agent.tool_registry
            all_tools = {**getattr(reg, "registry", {}), **getattr(reg, "dynamic_tools", {})}
            for name, tool in all_tools.items():
                ttype = getattr(tool, "tool_type", "?")
                if ttype == "structured_output":
                    origins[name] = "AUTO-ADDED BY STRANDS (structured output — from your Pydantic model)"
                elif ttype == "function":
                    origins[name] = "USER-DEFINED (passed via tools=[...])"
                else:
                    origins[name] = f"tool_type={ttype}"
        except Exception:
            pass
        return origins

    def _before_model_call(self, event: BeforeModelCallEvent) -> None:
        self._call_index += 1
        agent = event.agent
        try:
            tool_specs = agent.tool_registry.get_all_tool_specs()
        except Exception:
            tool_specs = list(getattr(agent, "tool_names", []))
        origins = self._tool_origins(agent)
        self.logger.info(self._banner(
            f"{self.agent_name} | REQUEST | model call #{self._call_index} "
            f"| ~{event.projected_input_tokens or '?'} input tokens"
        ))
        self.logger.info("SYSTEM PROMPT:\n" + (agent.system_prompt or "(none)"))
        if origins:
            self.logger.info("\nTOOL ORIGINS (who added each tool):\n" + self._dump(origins))
        self.logger.info(
            "\nTOOL SPECS SENT (the exact tool schemas the model receives):\n" + self._dump(tool_specs)
        )
        self.logger.info("\nMESSAGES (Strands' internal message list):\n" + self._dump(agent.messages))

    def _after_model_call(self, event: AfterModelCallEvent) -> None:
        if event.exception is not None:
            self.logger.info(self._banner(
                f"{self.agent_name} | RESPONSE | model call #{self._call_index} | FAILED"
            ))
            self.logger.info(f"EXCEPTION: {event.exception!r}")
            return
        if event.stop_response is None:
            self.logger.info(self._banner(
                f"{self.agent_name} | RESPONSE | model call #{self._call_index} | (no response)"
            ))
            return
        self.logger.info(self._banner(
            f"{self.agent_name} | RESPONSE | model call #{self._call_index} "
            f"| stop_reason={event.stop_response.stop_reason}"
        ))
        self.logger.info("RESPONSE MESSAGE (full):\n" + self._dump(event.stop_response.message))


def attach_wire_logger(bedrock_model, agent_name: str = "bedrock") -> None:
    """Hook boto3's event system on the Bedrock client to log the TRUE wire-level
    request and response — the exact JSON payload sent to / received from the
    Bedrock Converse API (modelId, system, messages, toolConfig, inferenceConfig,
    additionalModelRequestFields, etc.).

    Call this once per BedrockModel. Best paired with streaming=False so the response
    is a single JSON object instead of fragmented stream chunks.
    """
    logger = get_raw_logger()
    client = bedrock_model.client
    events = client.meta.events

    def _banner(header: str) -> str:
        import datetime
        ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        bar = "#" * 100
        return f"\n{bar}\n{ts} | {header}\n{bar}"

    def _dump(obj) -> str:
        try:
            return json.dumps(obj, indent=2, ensure_ascii=False, default=str)
        except Exception as e:
            return f"(could not serialize: {e})\n{obj!r}"

    def _log_request(params, **kwargs):
        body = params.get("body")
        if isinstance(body, (bytes, bytearray)):
            body = body.decode("utf-8", errors="replace")
        try:
            body_obj = json.loads(body) if isinstance(body, str) else body
        except Exception:
            body_obj = body
        logger.info(_banner("REQUEST"))
        logger.info(_dump(body_obj))

    def _log_response(http_response, parsed, **kwargs):
        # strip boto3's ResponseMetadata so only the model's actual output remains
        if isinstance(parsed, dict):
            parsed = {k: v for k, v in parsed.items() if k != "ResponseMetadata"}
        logger.info(_banner("RESPONSE"))
        logger.info(_dump(parsed))

    # register (unique_id prevents duplicate handlers if called twice)
    events.register("before-call.bedrock-runtime", _log_request, unique_id=f"wirelog-req-{agent_name}")
    events.register("after-call.bedrock-runtime", _log_response, unique_id=f"wirelog-resp-{agent_name}")


def _env_flag(name: str, default: bool = False) -> bool:
    """Read a boolean-ish environment variable (true/1/yes/on)."""
    val = os.getenv(name)
    if val is None:
        return default
    return val.strip().lower() in ("true", "1", "yes", "on")


def setup_langfuse_tracing() -> bool:
    """Export every model/tool call as an OTel span to a local Langfuse instance.

    Disabled by default. Set LANGFUSE_ENABLED=true in the environment to turn it on;
    it then also requires LANGFUSE_PUBLIC_KEY / LANGFUSE_SECRET_KEY / LANGFUSE_BASE_URL.
    No-ops (returns False) unless explicitly enabled and configured.
    """
    if not _env_flag("LANGFUSE_ENABLED", default=False):
        return False

    public_key = os.getenv("LANGFUSE_PUBLIC_KEY")
    secret_key = os.getenv("LANGFUSE_SECRET_KEY")
    base_url = os.getenv("LANGFUSE_BASE_URL")
    if not (public_key and secret_key and base_url):
        return False

    from strands.telemetry import StrandsTelemetry

    auth = base64.b64encode(f"{public_key}:{secret_key}".encode()).decode()
    StrandsTelemetry().setup_otlp_exporter(
        endpoint=f"{base_url.rstrip('/')}/api/public/otel/v1/traces",
        headers={
            "Authorization": f"Basic {auth}",
            "x-langfuse-ingestion-version": "4",
        },
    )
    return True
