from strands import Agent
from models import JudgeVerdict
from observability import LLMStepLogger
from prompts import JUDGE_SYSTEM_PROMPT


def create_judge_agent(model) -> Agent:
    return Agent(
        model=model,
        system_prompt=JUDGE_SYSTEM_PROMPT,
        tools=[],
        structured_output_model=JudgeVerdict,
        name="Judge",
        hooks=[LLMStepLogger("Judge")],
    )
