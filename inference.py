import os
import json
import requests
from openai import OpenAI

API_BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:8000")
MODEL_NAME = os.environ.get("MODEL_NAME", "gpt-4")
HF_TOKEN = os.environ.get("HF_TOKEN", "")

client = OpenAI(base_url=API_BASE_URL, api_key=HF_TOKEN)

def reset_env():
    return requests.post(f"{API_BASE_URL}/reset").json()

def step_env(action):
    return requests.post(f"{API_BASE_URL}/step", json=action).json()

def run_episode():
    obs = reset_env()
    total_score = 0.0
    steps = 0
    while not obs.get("done", False):
        code = obs.get("code_snippet", "")
        task_desc = obs.get("task_description", "")
        task_type = obs.get("task_type", "easy")
        prompt = f"You are an expert code reviewer. Task type: {task_type}. Task: {task_desc}. Code: {code}. Respond in JSON only: {{'has_syntax_error': true or false, 'quality_score': 0.0 to 1.0, 'issues': ['issue1'], 'severity': 'low or medium or high'}}"
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
        )
        text = response.choices[0].message.content
        try:
            clean = text.strip().replace("```json", "").replace("```", "")
            action = json.loads(clean)
        except:
            action = {"has_syntax_error": False, "quality_score": 0.5, "issues": [], "severity": "low"}
        obs = step_env(action)
        total_score += obs.get("reward", 0.0)
        steps += 1
        print(f"Step {steps}: score={obs.get('reward', 0.0):.2f}")
    avg = total_score / max(steps, 1)
    print(f"Episode score: {avg:.2f}")
    return avg

if __name__ == "__main__":
    scores = [run_episode() for _ in range(3)]
    print(f"Final baseline score: {sum(scores)/len(scores):.2f}")
