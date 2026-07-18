from strands import Agent
from tools.search import web_search
from models import ResearchReport
from observability import LLMStepLogger
from prompts import RESEARCHER_SYSTEM_PROMPT


def create_researcher_agent(model) -> Agent:
    return Agent(
        model=model,
        system_prompt=RESEARCHER_SYSTEM_PROMPT,
        tools=[web_search],
        structured_output_model=ResearchReport,
        name="Researcher",
        hooks=[LLMStepLogger("Researcher")],
    )
