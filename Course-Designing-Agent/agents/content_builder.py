from strands import Agent
from models import CourseOutline
from observability import LLMStepLogger
from prompts import CONTENT_BUILDER_SYSTEM_PROMPT


def create_content_builder_agent(model) -> Agent:
    return Agent(
        model=model,
        system_prompt=CONTENT_BUILDER_SYSTEM_PROMPT,
        tools=[],
        structured_output_model=CourseOutline,
        name="ContentBuilder",
        hooks=[LLMStepLogger("ContentBuilder")],
    )
