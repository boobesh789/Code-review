from openenv.core.env_server.types import Action, Observation
from pydantic import Field
from typing import List

class CodeReviewAction(Action):
    has_syntax_error: bool = Field(..., description="Does the code have syntax errors?")
    quality_score: float = Field(..., description="Code quality score 0.0-1.0")
    issues: List[str] = Field(default=[], description="List of issues found")
    severity: str = Field(default="low", description="Severity: low, medium, high")

class CodeReviewObservation(Observation):
    code_snippet: str = Field(default="", description="Code snippet to review")
    language: str = Field(default="python", description="Programming language")
    task_type: str = Field(default="easy", description="Task difficulty: easy/medium/hard")
    task_description: str = Field(default="", description="What to look for")
    score: float = Field(default=0.0, description="Current score 0.0-1.0")
    feedback: str = Field(default="", description="Feedback on last action")
    episode_step: int = Field(default=0, description="Current step in episode")
