"""Course outline output — terminal rendering and file saving."""
import json
import pathlib

from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule
from rich.table import Table
from rich import box

from models import CourseOutline

console = Console()


def render_course_outline(outline_json: str) -> None:
    """Pretty-print a CourseOutline JSON to the terminal."""
    try:
        data = json.loads(outline_json)
        outline = CourseOutline.model_validate(data)
    except Exception:
        console.print(outline_json)
        return

    console.print(Rule(f"[bold green]{outline.title}[/bold green]"))
    console.print(f"[italic]{outline.tagline}[/italic]\n")

    # Header info table
    info = Table(box=box.SIMPLE, show_header=False, padding=(0, 2))
    info.add_column(style="dim")
    info.add_column()
    info.add_row("Audience", outline.target_audience)
    info.add_row("Duration", f"~{outline.total_duration_hours} hours")
    info.add_row("Prerequisites", ", ".join(outline.prerequisites) or "None")
    console.print(info)

    # Learning outcomes
    console.print("[bold]Learning Outcomes[/bold]")
    for outcome in outline.learning_outcomes:
        console.print(f"  [green]✓[/green] {outcome}")

    # Modules
    console.print()
    for i, module in enumerate(outline.modules, 1):
        total_min = sum(l.estimated_minutes for l in module.lessons)
        console.print(Panel(
            "\n".join([
                f"[dim]{module.description}[/dim]",
                "",
                "[bold]Objectives:[/bold]",
                *[f"  • {o}" for o in module.learning_objectives],
                "",
                "[bold]Lessons:[/bold]",
                *[f"  {j}. {l.title} ({l.estimated_minutes}m)" for j, l in enumerate(module.lessons, 1)],
                "",
                f"[bold]Activity:[/bold] {module.hands_on_activity}",
            ]),
            title=f"[bold cyan]Module {i}: {module.title}[/bold cyan]  [dim]({total_min}m)[/dim]",
            border_style="cyan",
        ))

    # Assessment
    console.print(Panel(
        "\n".join([
            "[bold]Quiz Topics:[/bold]",
            *[f"  • {q}" for q in outline.assessment.quiz_topics],
            "",
            f"[bold]Capstone Project:[/bold] {outline.assessment.capstone_project}",
            "",
            "[bold]Grading Criteria:[/bold]",
            *[f"  • {c}" for c in outline.assessment.grading_criteria],
        ]),
        title="[bold magenta]Assessment[/bold magenta]",
        border_style="magenta",
    ))

    # Next steps
    console.print("[bold]Next Steps after this course:[/bold]")
    for step in outline.next_steps:
        console.print(f"  → {step}")


def save_outline(outline_json: str, path: str) -> None:
    """Save the course outline as formatted JSON and a readable markdown file."""
    base = pathlib.Path(path).stem
    out_dir = pathlib.Path(path).parent

    # Save raw JSON
    json_path = out_dir / f"{base}.json"
    with open(json_path, "w") as f:
        json.dump(json.loads(outline_json), f, indent=2)

    # Save readable markdown
    try:
        outline = CourseOutline.model_validate(json.loads(outline_json))
        md_path = out_dir / f"{base}.md"
        lines = [
            f"# {outline.title}",
            f"_{outline.tagline}_",
            "",
            f"**Audience:** {outline.target_audience}  ",
            f"**Duration:** ~{outline.total_duration_hours} hours  ",
            f"**Prerequisites:** {', '.join(outline.prerequisites) or 'None'}",
            "",
            "## Learning Outcomes",
            *[f"- {o}" for o in outline.learning_outcomes],
            "",
        ]
        for i, module in enumerate(outline.modules, 1):
            total_min = sum(l.estimated_minutes for l in module.lessons)
            lines += [
                f"## Module {i}: {module.title} ({total_min}m)",
                f"_{module.description}_",
                "",
                "**Objectives:**",
                *[f"- {o}" for o in module.learning_objectives],
                "",
                "**Lessons:**",
                *[f"{j}. {l.title} ({l.estimated_minutes}m)" for j, l in enumerate(module.lessons, 1)],
                "",
                f"**Activity:** {module.hands_on_activity}",
                "",
                "**Takeaways:**",
                *[f"- {t}" for t in module.key_takeaways],
                "",
            ]
        lines += [
            "## Assessment",
            f"**Capstone:** {outline.assessment.capstone_project}",
            "",
            "**Grading:**",
            *[f"- {c}" for c in outline.assessment.grading_criteria],
            "",
            "## Next Steps",
            *[f"- {s}" for s in outline.next_steps],
        ]
        with open(md_path, "w") as f:
            f.write("\n".join(lines))
        console.print(f"[green]Saved:[/green] {json_path}  +  {md_path}")
    except Exception as e:
        console.print(f"[green]Saved JSON:[/green] {json_path}  [dim](markdown failed: {e})[/dim]")
