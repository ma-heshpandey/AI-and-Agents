# Course Architect

A multi-agent AI system that automatically creates structured course outlines on any topic. Built with **AWS Strands Agents** and powered by **Amazon Bedrock** (or Anthropic API directly).

---

## Architecture

```
User Input (topic)
      │
      ▼
┌─────────────────────────────────────────┐
│           Orchestrator Agent            │
│  Coordinates the pipeline via tools     │
└────────┬──────────────┬────────────────┘
         │              │
         ▼              ▼
   ┌──────────┐   ┌──────────┐
   │Researcher│   │  Judge   │◄──── loops up to 3x
   │  Agent   │   │  Agent   │      until APPROVED
   └──────────┘   └──────────┘
         │              │
         │   research   │  verdict
         └──────┬───────┘
                │ APPROVED
                ▼
        ┌───────────────┐
        │ Content Builder│
        │    Agent       │
        └───────────────┘
                │
                ▼
        Final Course Outline
```

### Agents

| Agent | Role |
|---|---|
| **Orchestrator** | Entry point. Coordinates the full pipeline using the Agent-as-Tool pattern |
| **Researcher** | Searches the web and synthesizes comprehensive information on the topic |
| **Judge** | Evaluates research quality. Returns `APPROVED` or `NEEDS_REVISION` with specific feedback |
| **Content Builder** | Transforms approved research into a complete, structured course outline |

The Judge creates a feedback loop — if research is lacking, it sends revision instructions back to the Researcher. This repeats up to 3 times before the Builder proceeds with the best available content.

---

## Prerequisites

- [`uv`](https://docs.astral.sh/uv/) (manages Python and dependencies)
- AWS account with Bedrock access **OR** an Anthropic API key

> `uv` will install the correct Python version automatically — you don't need Python set up separately.

---

## Setup

### 1. Clone / enter the project

```bash
cd Course-Architect
```

### 2. Install dependencies

```bash
uv sync
```

This creates the virtual environment and installs everything from `pyproject.toml` /
`uv.lock` in one step. To also enable the Anthropic API provider:

```bash
uv sync --extra anthropic
```

### 3. Configure credentials

Copy the example env file and fill in your credentials:

```bash
cp .env.example .env
```

Then edit `.env`:

```env
# --- Option A: Amazon Bedrock (recommended) ---
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_DEFAULT_REGION=us-east-1
AWS_BEDROCK_MODEL_ID=us.anthropic.claude-3-7-sonnet-20250219-v1:0

# --- Option B: Anthropic API directly ---
# ANTHROPIC_API_KEY=sk-ant-...
```

> **Bedrock model access**: Make sure the model you choose is enabled in your AWS region via the [Bedrock console](https://console.aws.amazon.com/bedrock/home#/modelaccess).

---

## Usage

Run everything through `uv run` — it uses the project's environment automatically, with no
manual activation needed.

```bash
# Run with a topic
uv run python main.py "Introduction to Machine Learning"

# Save the course outline to a file
uv run python main.py "Python for Beginners" --output course.md

# Interactive mode — prompts you to enter a topic
uv run python main.py

# Set a default topic in .env
COURSE_TOPIC=Docker for DevOps Engineers
uv run python main.py
```

### Example output

```
── Course Creation AI Agent ──────────────────────────────────
  Topic: Introduction to Machine Learning
  Pipeline:
    1. Researcher  — gathers comprehensive information
    2. Judge       — evaluates quality (loops until approved)
    3. Builder     — creates the final course outline

── Pipeline running... ───────────────────────────────────────
╭─ Researcher ──╮  investigating: Introduction to Machine Learning
╭─ Judge ───────╮  evaluating research quality...
                   VERDICT: APPROVED  SCORE: 8/10
╭─ Content Builder ╮  creating course outline...

── Course Creation Complete ──────────────────────────────────
╭─ Course: Introduction to Machine Learning ──────────────────╮
│  COURSE OVERVIEW                                            │
│  Title: From Zero to ML: A Practical Introduction          │
│  ...                                                        │
╰─────────────────────────────────────────────────────────────╯
```

---

## Models

### Amazon Bedrock

Set `AWS_BEDROCK_MODEL_ID` to any Bedrock model your account has access to, as
long as it supports tool use / function calling via the Converse API (required
for structured output and the researcher's `web_search` tool). For example:

```env
AWS_BEDROCK_MODEL_ID=us.anthropic.claude-3-7-sonnet-20250219-v1:0
```

### Anthropic API (direct)

Install the extra and set `ANTHROPIC_API_KEY`. When it's set, the app uses the
Anthropic API instead of Bedrock and derives the model name from
`AWS_BEDROCK_MODEL_ID` — again, any tool-use-capable Claude model works.

```bash
uv sync --extra anthropic
```

---

## Observability

Every run writes two local log files automatically (no setup needed):

| File | Contents |
|---|---|
| `logs/pipeline.log` | Human-readable per-agent summary of each LLM/tool step |
| `logs/raw_io.log` | The exact raw request/response JSON sent to and from Bedrock |

### Langfuse tracing (optional)

[Langfuse](https://langfuse.com/) gives you a UI to inspect traces of every model and tool
call — timelines, token usage, and nested spans. It is **disabled by default** and only
turns on when you explicitly enable it.

**1. Have Langfuse running locally (Docker).** If your instance is already up, just note its
URL (default `http://localhost:3000`) and skip to step 2. To start one from scratch:

```bash
git clone https://github.com/langfuse/langfuse.git
cd langfuse
docker compose up -d          # starts Langfuse at http://localhost:3000
```

Then open the URL, create an account, and create a project.

**2. Get your API keys.** In the Langfuse UI: **Project → Settings → API Keys → Create**.
Copy the **public key** (`pk-lf-...`) and **secret key** (`sk-lf-...`).

**3. Enable it in `.env`:**

```env
LANGFUSE_ENABLED=true
LANGFUSE_PUBLIC_KEY=pk-lf-...
LANGFUSE_SECRET_KEY=sk-lf-...
LANGFUSE_BASE_URL=http://localhost:3000
```

Tracing activates only when `LANGFUSE_ENABLED=true` **and** all three values are set —
otherwise the app runs normally with no tracing. When enabled, the app prints
`Tracing to Langfuse: http://localhost:3000` at startup, and traces appear in the
Langfuse UI under your project.

> To turn it off again, set `LANGFUSE_ENABLED=false` (or remove the line). You can leave the
> keys in place; they're ignored while disabled.

---

## Project Structure

```
Course-Architect/
├── .env                     # Your credentials (not committed)
├── .env.example             # Credential template
├── pyproject.toml           # Project metadata + dependencies (uv)
├── uv.lock                  # Pinned dependency lockfile (uv)
├── .python-version          # Python version for uv
├── main.py                  # CLI entry point
├── observability.py         # Logging + raw request/response capture
├── agents/
│   ├── __init__.py
│   ├── orchestrator.py      # Pipeline coordinator
│   ├── researcher.py        # Web research agent
│   ├── judge.py             # Quality evaluation agent
│   └── content_builder.py   # Course content generation agent
├── config.py                # Model setup (Bedrock / Anthropic)
├── output.py                # Terminal rendering + file saving
├── models/                  # Pydantic output schemas
├── prompts/                 # Agent system prompts
├── tools/
│   ├── __init__.py
│   └── search.py            # DuckDuckGo web search tool
├── logs/                    # pipeline.log + raw_io.log (auto-generated)
└── docs/                    # Architecture deep-dives (local only, git-ignored)
```

---

## Dependencies

| Package | Purpose |
|---|---|
| `strands-agents` | Core agent framework |
| `boto3` | AWS SDK (Bedrock access) |
| `python-dotenv` | Load `.env` credentials |
| `rich` | Terminal output formatting |
| `opentelemetry-exporter-otlp-proto-http` | Optional Langfuse/OTel tracing |

---

## Troubleshooting

**`No credentials found` error**
Make sure `.env` has either `AWS_ACCESS_KEY_ID` or `ANTHROPIC_API_KEY` set correctly.


**`No module named 'anthropic'`**
Install the extra: `uv sync --extra anthropic`. Only needed when using `ANTHROPIC_API_KEY`.

**Research quality is low / Judge keeps rejecting**
Try a more capable model (e.g. Claude 3.7 Sonnet) or make the topic more specific.
