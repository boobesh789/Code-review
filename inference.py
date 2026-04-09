import os
import json
import requests
from openai import OpenAI

API_BASE_URL = os.getenv('API_BASE_URL', 'https://api.openai.com/v1')
MODEL_NAME = os.getenv('MODEL_NAME', 'gpt-4')
HF_TOKEN = os.getenv('HF_TOKEN', 'dummy')
ENV_URL = 'https://boobesh007-code-review.hf.space'

client = OpenAI(base_url=API_BASE_URL, api_key=HF_TOKEN)

def reset_env():
    try:
        return requests.post(ENV_URL + '/reset', timeout=30).json()
    except Exception as e:
        print('Reset failed: ' + str(e))
        return {'done': True, 'code_snippet': '', 'task_type': 'easy', 'task_description': ''}

def step_env(action):
    try:
        return requests.post(ENV_URL + '/step', json=action, timeout=30).json()
    except Exception as e:
        print('Step failed: ' + str(e))
        return {'done': True, 'reward': 0.0}

def get_action(obs):
    code = obs.get('code_snippet', '')
    task_desc = obs.get('task_description', '')
    task_type = obs.get('task_type', 'easy')
    prompt = 'Review this code. Task: ' + task_desc + ' Code: ' + code + ' Reply in JSON: {"has_syntax_error": false, "quality_score": 0.5, "issues": ["issue"], "severity": "low"}'
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{'role': 'user', 'content': prompt}],
            max_tokens=300,
        )
        text = response.choices[0].message.content
        clean = text.strip().replace('```json', '').replace('```', '').strip()
        return json.loads(clean)
    except Exception as e:
        print('LLM error: ' + str(e))
        return {'has_syntax_error': False, 'quality_score': 0.5, 'issues': ['issue'], 'severity': 'low'}

def run_episode(n):
    print('START episode=' + str(n))
    obs = reset_env()
    total = 0.0
    steps = 0
    while not obs.get('done', False) and steps < 5:
        action = get_action(obs)
        obs = step_env(action)
        score = obs.get('reward', 0.0)
        total += score
        steps += 1
        print('STEP ' + str(steps) + ': score=' + str(round(score, 2)))
    avg = total / max(steps, 1)
    print('END episode=' + str(n) + ' score=' + str(round(avg, 2)))
    return avg

if __name__ == '__main__':
    scores = []
    for i in range(3):
        try:
            scores.append(run_episode(i + 1))
        except Exception as e:
            print('END episode=' + str(i+1) + ' score=0.00')
            scores.append(0.0)
    print('FINAL_SCORE=' + str(round(sum(scores)/len(scores), 2)))
