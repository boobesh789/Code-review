---
title: AI Code Review Environment
emoji: 💻
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
tags:
  - openenv
  - code-review
  - reinforcement-learning
  - ai-agent
---

# 💻 AI Code Review Environment

> A production-grade OpenEnv environment where AI agents learn to review code like senior software engineers.

## 🎯 Overview

This environment simulates **real-world code review** — one of the most critical tasks in software engineering. An AI agent is presented with code snippets and must identify bugs, security vulnerabilities, and quality issues across multiple programming languages.

This is not a toy problem. Code review is a skill that takes years for humans to master. This environment provides a structured way to train and evaluate AI agents on this task.

## 🌍 Supported Languages
| Language | Coverage |
|----------|----------|
| Python 🐍 | Syntax, quality, security, bugs |
| JavaScript 🌐 | Security, quality, best practices |
| Java ☕ | Null safety, resource management |

## 📊 Task Difficulty Levels

### 🟢 Easy — Syntax Detection
Agent must identify basic syntax errors.
- Missing colons, brackets, parentheses
- Baseline score: **0.85**

### 🟡 Medium — Code Quality
Agent must identify quality issues.
- Poor naming, too many parameters
- Functions doing too many things
- Baseline score: **0.65**

### 🔴 Hard — Security & Bugs
Agent must identify critical issues.
- SQL injection vulnerabilities
- Hardcoded passwords
- Division by zero
- Null pointer exceptions
- No error handling
- Baseline score: **0.45**

## 🎮 Action Space
| Field | Type | Range | Description |
|-------|------|-------|-------------|
| has_syntax_error | bool | true/false | Does code have syntax errors? |
| quality_score | float | 0.01-0.99 | Overall code quality |
| issues | list | 1-5 items | List of issues found |
| severity | str | low/medium/high | Overall severity |

## 👁️ Observation Space
| Field | Type | Description |
|-------|------|-------------|
| code_snippet | str | Code to review |
| language | str | Programming language |
| task_type | str | easy/medium/hard |
| task_description | str | What to look for |
| score | float | Score for last action |
| feedback | str | Detailed feedback |
| episode_step | int | Current step number |

## 🏆 Reward Function
| Correct Action | Reward |
|---------------|--------|
| Syntax detection | +0.30 |
| Severity assessment | +0.20 |
| Issues identified | +0.50 |
| **Maximum per step** | **0.99** |
| **Minimum per step** | **0.01** |

## 📈 Baseline Results
| Task | Baseline Score | Difficulty |
|------|---------------|------------|
| Easy | 0.85 | Beginner |
| Medium | 0.65 | Intermediate |
| Hard | 0.45 | Expert |
| **Average** | **0.65** | - |

## 🚀 API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /reset | Start new episode |
| POST | /step | Execute action |
| GET | /state | Get current state |
| GET | /schema | Get action/observation schemas |
| GET | /health | Health check |
| GET | /docs | Swagger UI |

## 🛠️ Setup & Installation
```bash
pip install openenv-core
openenv init code_review
uvicorn server.app:app --host 0.0.0.0 --port 7860
🤖 Example Agent Interaction
import requests

# Reset environment
obs = requests.post('https://boobesh007-code-review.hf.space/reset').json()

# Take action
action = {
    'has_syntax_error': True,
    'quality_score': 0.8,
    'issues': ['missing colon after function definition'],
    'severity': 'high'
}
result = requests.post('https://boobesh007-code-review.hf.space/step', json=action).json()
print(result['reward'])
📁 Project Structure
code_review/
├── models.py          # Action and Observation models
├── inference.py       # Baseline inference script
├── server/
│   ├── app.py         # FastAPI application
│   └── code_review_environment.py  # Environment logic
├── Dockerfile         # Container configuration
└── README.md          # Documentation
👨‍💻 Built With
Python 3.11
FastAPI
OpenEnv Core
Pydantic
Docker
Hugging Face Spaces
📜 License
BSD-3-Clause
