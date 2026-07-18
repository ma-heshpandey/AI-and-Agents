from __future__ import annotations

from enum import Enum
from typing import Annotated

from pydantic import BaseModel, Field


# ── Researcher output ─────────────────────────────────────────────────────────

class KeyConcept(BaseModel):
    concept: str = Field(description="Name of the concept")
    explanation: str = Field(description="Clear, concise explanation suitable for a learner")
    importance: Annotated[int, Field(ge=1, le=5)] = Field(
        description="How central this concept is to the topic (1 = supplementary, 5 = essential)"
    )


class ResearchReport(BaseModel):
    topic: str = Field(description="The exact topic that was researched")
    overview: str = Field(description="2-3 sentence summary of the topic")
    why_it_matters: str = Field(description="Why learners should care about this topic")
    target_audience: str = Field(description="Who this course is best suited for")
    prerequisites: list[str] = Field(description="Knowledge or skills learners need before starting")
    key_concepts: list[KeyConcept] = Field(description="Core concepts to teach, ordered from foundational to advanced")
    suggested_modules: list[str] = Field(description="Proposed module titles in logical learning order")
    learning_objectives: list[str] = Field(description="What learners will be able to DO after completing the course")
    practical_examples: list[str] = Field(description="Real-world examples or use cases to illustrate the topic")
    common_misconceptions: list[str] = Field(description="Frequent misunderstandings that the course should address")
    recommended_resources: list[str] = Field(description="Books, websites, or tools worth referencing")


# ── Judge output ──────────────────────────────────────────────────────────────

class Verdict(str, Enum):
    APPROVED = "APPROVED"
    NEEDS_REVISION = "NEEDS_REVISION"


class JudgeVerdict(BaseModel):
    verdict: Verdict = Field(description="Whether the research meets quality standards")
    score: Annotated[int, Field(ge=1, le=10)] = Field(
        description="Overall quality score (1-10). Must be >= 7 to be APPROVED"
    )
    strengths: list[str] = Field(description="Specific things the research does well")
    gaps: list[str] = Field(description="Specific missing or weak areas in the research")
    revision_instructions: str = Field(
        description=(
            "If NEEDS_REVISION: detailed instructions on what to research or improve. "
            "If APPROVED: 'None - content meets quality standards.'"
        )
    )


# ── Content Builder output ────────────────────────────────────────────────────

class Lesson(BaseModel):
    title: str = Field(description="Lesson title")
    key_teaching_points: list[str] = Field(description="3-5 bullet points of what this lesson teaches")
    estimated_minutes: Annotated[int, Field(ge=5, le=120)] = Field(description="Estimated lesson duration in minutes")


class Module(BaseModel):
    title: str = Field(description="Module title")
    description: str = Field(description="One sentence describing what this module covers")
    learning_objectives: list[str] = Field(description="Measurable objectives — what learners can DO after this module")
    lessons: list[Lesson] = Field(description="Ordered list of lessons in this module")
    hands_on_activity: str = Field(description="A practical exercise or project for this module")
    key_takeaways: list[str] = Field(description="The 3-5 most important things to remember from this module")


class Assessment(BaseModel):
    quiz_topics: list[str] = Field(description="Topics to cover in knowledge check quizzes")
    capstone_project: str = Field(description="Description of the final project or assignment")
    grading_criteria: list[str] = Field(description="How student work will be evaluated")


class CourseOutline(BaseModel):
    title: str = Field(description="Compelling, clear course title")
    tagline: str = Field(description="One-sentence hook that sells the course")
    target_audience: str = Field(description="Who this course is for")
    prerequisites: list[str] = Field(description="What learners need before starting")
    total_duration_hours: Annotated[float, Field(ge=0.5)] = Field(description="Estimated total course length in hours")
    learning_outcomes: list[str] = Field(description="Top-level skills or knowledge gained upon completion")
    modules: list[Module] = Field(description="All course modules in teaching order")
    assessment: Assessment = Field(description="How learners are tested and graded")
    recommended_tools: list[str] = Field(description="Software, platforms, or materials students will need")
    next_steps: list[str] = Field(description="What learners can pursue after completing this course")
