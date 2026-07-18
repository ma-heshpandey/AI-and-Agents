"""Model configuration — builds the LLM backend (Amazon Bedrock or Anthropic API)."""
import os
import sys

from botocore.config import Config
from rich.console import Console
from strands.models import BedrockModel

from observability import attach_wire_logger

console = Console()

DEFAULT_BEDROCK_MODEL_ID = "us.anthropic.claude-3-7-sonnet-20250219-v1:0"


def get_model():
    """Return a Strands model, preferring the Anthropic API if a key is set,
    otherwise falling back to Amazon Bedrock."""
    model_id = os.getenv("AWS_BEDROCK_MODEL_ID", DEFAULT_BEDROCK_MODEL_ID)
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")

    if anthropic_key:
        # Imported lazily: the `anthropic` extra is optional (uv sync --extra anthropic).
        try:
            from strands.models.anthropic import AnthropicModel
        except ImportError:
            console.print("[yellow]anthropic package not installed; falling back to Bedrock.[/yellow]")
        else:
            api_model_id = (
                model_id
                .replace("us.anthropic.", "")
                .replace("anthropic.", "")
                .rstrip("-v1:0").rstrip("-v2:0")
            )
            console.print(f"[dim]Using Anthropic API | Model: {api_model_id}[/dim]")
            return AnthropicModel(client_args={"api_key": anthropic_key}, model_id=api_model_id)

    aws_key = os.getenv("AWS_ACCESS_KEY_ID")
    if not aws_key:
        console.print("[red]Error:[/red] No credentials found.")
        console.print("Set [bold]AWS_ACCESS_KEY_ID[/bold] + [bold]AWS_SECRET_ACCESS_KEY[/bold] in .env")
        sys.exit(1)

    region = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
    console.print(f"[dim]Using Amazon Bedrock | Region: {region} | Model: {model_id}[/dim]")
    boto_config = Config(read_timeout=300, connect_timeout=30, retries={"max_attempts": 2})
    # streaming=False so the raw response logs as one JSON object (not stream chunks)
    model = BedrockModel(model_id=model_id, region_name=region,
                         boto_client_config=boto_config, streaming=False)
    attach_wire_logger(model, agent_name="bedrock")
    return model
