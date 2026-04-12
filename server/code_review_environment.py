from uuid import uuid4
import random
from openenv.core.env_server.interfaces import Environment
from openenv.core.env_server.types import State

try:
    from ..models import CodeReviewAction, CodeReviewObservation
except ImportError:
    from models import CodeReviewAction, CodeReviewObservation

TASKS = [
    {
        "code": "def add(a, b)\n    return a + b",
        "language": "python",
        "description": "Find syntax errors in this code",
        "has_syntax_error": True,
        "expected_issues": ["missing colon"],
        "severity": "high",
        "difficulty": "easy"
    },
    {
        "code": "x = [1, 2, 3\nprint(x)",
        "language": "python",
        "description": "Find syntax errors in this code",
        "has_syntax_error": True,
        "expected_issues": ["missing bracket"],
        "severity": "high",
        "difficulty": "easy"
    },
    {
        "code": "def multiply(a, b):\n    return a * b",
        "language": "python",
        "description": "Find syntax errors in this code",
        "has_syntax_error": False,
        "expected_issues": [],
        "severity": "low",
        "difficulty": "easy"
    },
    {
        "code": "for i in range(10)\n    print(i)",
        "language": "python",
        "description": "Find syntax errors in this code",
        "has_syntax_error": True,
        "expected_issues": ["missing colon"],
        "severity": "high",
        "difficulty": "easy"
    },
    {
        "code": "def x(a, b, c, d, e, f):\n    return a+b+c+d+e+f",
        "language": "python",
        "description": "Find code quality issues",
        "has_syntax_error": False,
        "expected_issues": ["poor name", "too many parameters"],
        "severity": "medium",
        "difficulty": "medium"
    },
    {
        "code": "def calculate(a, b):\n    r1 = a + b\n    r2 = a - b\n    r3 = a * b\n    return r1, r2, r3",
        "language": "python",
        "description": "Find code quality issues",
        "has_syntax_error": False,
        "expected_issues": ["poor variable names", "too many things"],
        "severity": "medium",
        "difficulty": "medium"
    },
    {
        "code": "import os\ndef delete_files(path):\n    files = os.listdir(path)\n    for f in files:\n        os.remove(f)",
        "language": "python",
        "description": "Full review: find bugs and security issues",
        "has_syntax_error": False,
        "expected_issues": ["missing path join", "no error handling"],
        "severity": "high",
        "difficulty": "hard"
    },
    {
        "code": "def get_user(id):\n    query = 'SELECT * FROM users WHERE id=' + id\n    return db.execute(query)",
        "language": "python",
        "description": "Full review: find bugs and security issues",
        "has_syntax_error": False,
        "expected_issues": ["sql injection", "no validation"],
        "severity": "high",
        "difficulty": "hard"
    },
    {
        "code": "def divide(a, b):\n    return a / b",
        "language": "python",
        "description": "Full review: find bugs and security issues",
        "has_syntax_error": False,
        "expected_issues": ["division by zero", "no error handling"],
        "severity": "high",
        "difficulty": "hard"
    },
    {
        "code": "var password = 'admin123';\nif (userInput == password) {\n    grantAccess();\n}",
        "language": "javascript",
        "description": "Full review: find security issues",
        "has_syntax_error": False,
        "expected_issues": ["hardcoded password", "security risk"],
        "severity": "high",
        "difficulty": "hard"
    },
    {
        "code": "public void readFile(String path) {\n    FileReader f = new FileReader(path);\n    f.read();\n}",
        "language": "java",
        "description": "Full review: find bugs and security issues",
        "has_syntax_error": False,
        "expected_issues": ["resource not closed", "no exception handling"],
        "severity": "medium",
        "difficulty": "hard"
    },
]

class CodeReviewEnvironment(Environment):
    SUPPORTS_CONCURRENT_SESSIONS: bool = True

    def __init__(self):
        self._state = State(episode_id=str(uuid4()), step_count=0)
        self._current_task = None
        self._task_type = "easy"
        self._score = 0.0
        self._step = 0

    def _get_task(self):
        task = random.choice(TASKS)
        self._task_type = task["difficulty"]
        return task

    def reset(self) -> CodeReviewObservation:
        self._state = State(episode_id=str(uuid4()), step_count=0)
        self._current_task = self._get_task()
        self._score = 0.0
        self._step = 0
        return CodeReviewObservation(
            code_snippet=self._current_task["code"],
            language=self._current_task["language"],
            task_type=self._task_type,
            task_description=self._current_task["description"],
            score=0.0,
            feedback="New code snippet ready for review!",
            episode_step=0,
            done=False,
            reward=0.0,
        )

    def _grade(self, action: CodeReviewAction) -> float:
        task = self._current_task
        reward = 0.0
        try:
            if action.has_syntax_error == task["has_syntax_error"]:
                reward += 0.3
            if action.severity == task["severity"]:
                reward += 0.2
            if task["expected_issues"]:
                matched = 0
                for issue in action.issues:
                    for exp in task["expected_issues"]:
                        if exp.lower() in issue.lower():
                            matched += 1
                            break
                issue_score = matched / len(task["expected_issues"])
                reward += 0.5 * issue_score
            else:
                if len(action.issues) == 0:
                    reward += 0.5
        except Exception:
            reward = 0.5
        return max(0.01, min(reward, 0.99))

    def step(self, action: CodeReviewAction) -> CodeReviewObservation:
        self._state.step_count += 1
        self._step += 1
        reward = self._grade(action)
        self._score = reward
        feedback = "Score: " + str(round(reward, 2)) + ". "
        if reward >= 0.8:
            feedback += "Excellent review!"
        elif reward >= 0.5:
            feedback += "Good review, some issues missed."
        else:
            feedback += "Review needs improvement."
        self._current_task = self._get_task()
        done = self._step >= 5
        return CodeReviewObservation(
            code_snippet=self._current_task["code"],
            language=self._current_task["language"],
            task_type=self._task_type,
            task_description=self._current_task["description"],
            score=reward,
            feedback=feedback,
            episode_step=self._step,
            done=done,
            reward=reward,
        )

    @property
    def state(self) -> State:
        return self._state
