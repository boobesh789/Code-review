from uuid import uuid4
import random
from openenv.core.env_server.interfaces import Environment
from openenv.core.env_server.types import State

try:
    from ..models import CodeReviewAction, CodeReviewObservation
except ImportError:
    from models import CodeReviewAction, CodeReviewObservation

TASKS = {
    "easy": [
        {
            "code": "def add(a, b)\n    return a + b",
            "language": "python",
            "description": "Find syntax errors in this code",
            "has_syntax_error": True,
            "expected_issues": ["missing colon after function definition"],
            "severity": "high"
        },
        {
            "code": "x = [1, 2, 3\nprint(x)",
            "language": "python",
            "description": "Find syntax errors in this code",
            "has_syntax_error": True,
            "expected_issues": ["missing closing bracket"],
            "severity": "high"
        },
        {
            "code": "def multiply(a, b):\n    return a * b",
            "language": "python",
            "description": "Find syntax errors in this code",
            "has_syntax_error": False,
            "expected_issues": [],
            "severity": "low"
        },
    ],
    "medium": [
        {
            "code": "def x(a, b, c, d, e, f):\n    return a+b+c+d+e+f",
            "language": "python",
            "description": "Find code quality issues: naming and complexity",
            "has_syntax_error": False,
            "expected_issues": ["poor function name", "too many parameters"],
            "severity": "medium"
        },
        {
            "code": "def calculate(a, b):\n    result = a + b\n    result2 = a - b\n    result3 = a * b\n    return result, result2, result3",
            "language": "python",
            "description": "Find code quality issues",
            "has_syntax_error": False,
            "expected_issues": ["poor variable names", "function does too many things"],
            "severity": "medium"
        },
    ],
    "javascript": [
        {
            "code": "function add(a, b) {\n    return a + b\n}\nconsole.log(add(1, 2))",
            "language": "javascript",
            "description": "Find code quality issues in this JavaScript code",
            "has_syntax_error": False,
            "expected_issues": ["missing semicolons"],
            "severity": "low"
        },
        {
            "code": "var password = 'admin123';\nif (userInput == password) {\n    grantAccess();\n}",
            "language": "javascript",
            "description": "Full review: find bugs and security issues",
            "has_syntax_error": False,
            "expected_issues": ["hardcoded password", "use === instead of ==", "security risk"],
            "severity": "high"
        },
        {
            "code": "function fetchData(url) {\n    var result = null;\n    $.ajax({url: url, async: false, success: function(data) { result = data; }});\n    return result;\n}",
            "language": "javascript",
            "description": "Full review: find bugs and performance issues",
            "has_syntax_error": False,
            "expected_issues": ["synchronous ajax call", "performance issue", "blocks main thread"],
            "severity": "high"
        },
    ],
    "java": [
        {
            "code": "public class Main {\n    public static void main(String[] args) {\n        String s = null;\n        System.out.println(s.length());\n    }\n}",
            "language": "java",
            "description": "Full review: find bugs and security issues",
            "has_syntax_error": False,
            "expected_issues": ["null pointer exception", "no null check"],
            "severity": "high"
        },
        {
            "code": "public void readFile(String path) {\n    FileReader fr = new FileReader(path);\n    BufferedReader br = new BufferedReader(fr);\n    System.out.println(br.readLine());\n}",
            "language": "java",
            "description": "Full review: find bugs and security issues",
            "has_syntax_error": False,
            "expected_issues": ["resource leak", "no try-finally", "file not closed"],
            "severity": "high"
        },
    ],
    "hard": [
       {
           "code": "def divide(a, b):\n    return a / b",
           "language": "python",
           "description": "Full review: find bugs, security issues and performance problems",
           "has_syntax_error": False,
           "expected_issues": ["division by zero", "no error handling"],
           "severity": "high"
       },
       {
           "code": "password = \"admin123\"\nif user_input == password:\n    grant_access()",
           "language": "python",
           "description": "Full review: find bugs, security issues and performance problems",
           "has_syntax_error": False,
           "expected_issues": ["hardcoded password", "security risk"],
           "severity": "high"
       },
        {
            "code": "import os\ndef delete_files(path):\n    files = os.listdir(path)\n    for f in files:\n        os.remove(f)",
            "language": "python",
            "description": "Full review: find bugs, security issues and performance problems",
            "has_syntax_error": False,
            "expected_issues": ["missing path join", "security risk", "no error handling", "deletes wrong files"],
            "severity": "high"
        },
        {
            "code": "def get_user(id):\n    query = 'SELECT * FROM users WHERE id=' + id\n    return db.execute(query)",
            "language": "python",
            "description": "Full review: find bugs, security issues and performance problems",
            "has_syntax_error": False,
            "expected_issues": ["SQL injection vulnerability", "no input validation", "security risk"],
            "severity": "high"
        },
    ]
}

class CodeReviewEnvironment(Environment):
    SUPPORTS_CONCURRENT_SESSIONS: bool = True

    def __init__(self):
        self._state = State(episode_id=str(uuid4()), step_count=0)
        self._current_task = None
        self._task_type = "easy"
        self._score = 0.0
        self._step = 0

    def _get_task(self):
        task_type = random.choice(["easy", "medium", "hard", "javascript", "java"])
        self._task_type = task_type
        return random.choice(TASKS[task_type])

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
        if action.has_syntax_error == task["has_syntax_error"]:
            reward += 0.3
        if action.severity == task["severity"]:
            reward += 0.2
        if task["expected_issues"]:
            matched = sum(
                1 for issue in action.issues
                if any(exp in issue.lower() for exp in task["expected_issues"])
            )
            issue_score = matched / len(task["expected_issues"])
            reward += 0.5 * issue_score
        else:
            if len(action.issues) == 0:
                reward += 0.5
        result = min(reward, 1.0)
        result = max(0.01, min(result, 0.99))
        return result

    def step(self, action: CodeReviewAction) -> CodeReviewObservation:
        self._state.step_count += 1
        self._step += 1
        reward = self._grade(action)
        self._score = reward
        feedback = f"Score: {reward:.2f}. "
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
