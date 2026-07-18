#!/usr/bin/env python3
"""
Course Creation AI Agent — AWS Strands + Pydantic structured output
Pipeline: Orchestrator → Researcher → Judge (quality loop) → Content Builder
"""
import os
import re
import sys
import argparse

from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule

from config import get_model
from output import render_course_outline, save_outline
from observability import LOG_PATH, setup_langfuse_tracing
from agents import (
    create_researcher_agent,
    create_judge_agent,
    create_content_builder_agent,
    create_orchestrator_agent,
)

load_dotenv()

console = Console()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="AI Course Creation Agent (AWS Strands + Pydantic)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py "Introduction to Machine Learning"
  python main.py "Python for Beginners" --output course
  python main.py   # interactive topic prompt
        """,
    )
    parser.add_argument("topic", nargs="?", default=os.getenv("COURSE_TOPIC", ""),
                        help="Topic to create a course about")
    parser.add_argument("--output", "-o", default="course_output",
                        help="Base name for output files (creates <name>.json + <name>.md, default: course_output)")
    return parser.parse_args()


def run_pipeline(topic: str) -> str | None:
    """Build the agents, run the orchestrator, and return the CourseOutline JSON."""
    model = get_model()

    if setup_langfuse_tracing():
        console.print(f"[dim]Tracing to Langfuse: {os.getenv('LANGFUSE_BASE_URL')}[/dim]")
    console.print(f"[dim]Logging every LLM/tool step to: {LOG_PATH}[/dim]")

    researcher = create_researcher_agent(model)
    judge = create_judge_agent(model)
    content_builder = create_content_builder_agent(model)
    orchestrator = create_orchestrator_agent(model, researcher, judge, content_builder)

    console.print(Rule("[dim]Pipeline running...[/dim]"))
    result = orchestrator(f"Create a complete course on: {topic}")

    # Prefer the JSON captured directly from the build_course_content tool call —
    # the orchestrator's own final text response sometimes only summarizes the
    # result instead of repeating the full JSON, which broke JSON parsing.
    outline_json = orchestrator.captured.get("outline_json")
    if not outline_json:
        # Fall back to pulling JSON out of the orchestrator's final text.
        json_match = re.search(r'\{[\s\S]+\}', str(result))
        outline_json = json_match.group(0) if json_match else None

    if not outline_json:
        console.print(Rule("[bold red]Pipeline Failed[/bold red]"))
        console.print("[red]Error:[/red] No CourseOutline JSON was produced. "
                      "The orchestrator's final response was:\n")
        console.print(str(result))
    return outline_json


def main() -> None:
    args = parse_args()

    topic = args.topic.strip()
    if not topic:
        topic = console.input("[bold]Enter the course topic:[/bold] ").strip()
    if not topic:
        console.print("[red]Error:[/red] No topic provided.")
        sys.exit(1)

    console.print(Rule("[bold blue]Course Creation AI Agent[/bold blue]"))
    console.print(Panel(
        f"[bold]Topic:[/bold] {topic}\n\n"
        "[dim]Pipeline:[/dim]\n"
        "  1. [cyan]Researcher[/cyan]      — structured ResearchReport (Pydantic validated)\n"
        "  2. [magenta]Judge[/magenta]          — structured JudgeVerdict  (loops until APPROVED)\n"
        "  3. [green]Content Builder[/green] — structured CourseOutline  (Pydantic validated)",
        title="[bold]Starting Pipeline[/bold]",
        border_style="blue",
    ))

    outline_json = run_pipeline(topic)
    if not outline_json:
        sys.exit(1)

    console.print(Rule("[bold green]Pipeline Complete[/bold green]"))
    render_course_outline(outline_json)
    save_outline(outline_json, args.output)


if __name__ == "__main__":
    main()
