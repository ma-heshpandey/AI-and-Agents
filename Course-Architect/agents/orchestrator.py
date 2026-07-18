from strands import Agent, tool
from rich.console import Console
from rich.panel import Panel
from models import CourseOutline, JudgeVerdict, ResearchReport, Verdict
from observability import LLMStepLogger
from prompts import ORCHESTRATOR_SYSTEM_PROMPT

console = Console()


def create_orchestrator_agent(model, researcher, judge, content_builder) -> Agent:
    # The orchestrator's own final text response isn't a reliable place to read the
    # CourseOutline JSON from — the model sometimes just summarizes instead of
    # repeating it. Capture it directly from the tool call that produced it instead.
    captured = {"outline_json": None}

    @tool
    def research_topic(prompt: str) -> str:
        """
        Research a course topic. The prompt should be the topic, optionally with
        revision instructions appended. Returns a ResearchReport as a JSON string.
        """
        console.print(Panel(
            f"[bold]Prompt:[/bold] {prompt[:120]}{'...' if len(prompt) > 120 else ''}",
            title="[cyan]Researcher[/cyan]",
            border_style="cyan",
        ))
        result = researcher(f"Research this topic for course creation: {prompt}")
        report: ResearchReport = result.structured_output
        if report is None:
            return str(result)
        console.print(f"[dim cyan]  ✓ Research complete — {len(report.key_concepts)} concepts, "
                      f"{len(report.suggested_modules)} modules[/dim cyan]")
        return report.model_dump_json(indent=2)

    @tool
    def evaluate_research(research_report_json: str) -> str:
        """
        Evaluate the quality of a research report. Accepts a ResearchReport JSON string.
        Returns a JudgeVerdict as a JSON string with verdict, score, and revision instructions.
        """
        console.print(Panel(
            "Evaluating research quality against pedagogical standards...",
            title="[magenta]Judge[/magenta]",
            border_style="magenta",
        ))
        result = judge(
            f"Evaluate this research report for course creation quality:\n\n{research_report_json}"
        )
        verdict: JudgeVerdict = result.structured_output
        if verdict is None:
            return str(result)

        verdict_color = "green" if verdict.verdict == Verdict.APPROVED else "yellow"
        console.print(
            f"[{verdict_color}]  Verdict: {verdict.verdict.value} | Score: {verdict.score}/10[/{verdict_color}]"
        )
        if verdict.gaps:
            for gap in verdict.gaps:
                console.print(f"[dim yellow]    - {gap}[/dim yellow]")
        return verdict.model_dump_json(indent=2)

    @tool
    def build_course_content(research_report_json: str) -> str:
        """
        Build a complete course outline from an approved research report.
        Accepts a ResearchReport JSON string. Returns a CourseOutline as a JSON string.
        """
        console.print(Panel(
            "Transforming research into a structured course outline...",
            title="[green]Content Builder[/green]",
            border_style="green",
        ))
        result = content_builder(
            f"Create a complete course outline based on this approved research:\n\n{research_report_json}"
        )
        outline: CourseOutline = result.structured_output
        if outline is None:
            return str(result)
        console.print(f"[dim green]  ✓ Course built — {len(outline.modules)} modules, "
                      f"~{outline.total_duration_hours}h total[/dim green]")
        captured["outline_json"] = outline.model_dump_json(indent=2)
        return captured["outline_json"]

    agent = Agent(
        model=model,
        system_prompt=ORCHESTRATOR_SYSTEM_PROMPT,
        tools=[research_topic, evaluate_research, build_course_content],
        name="Orchestrator",
        hooks=[LLMStepLogger("Orchestrator")],
    )
    agent.captured = captured
    return agent
