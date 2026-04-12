---
title: AI Code Review Environment
emoji: 💻
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
tags:
  - openenv
---

# AI Code Review Environment

## Description
An OpenEnv environment where AI agents review code snippets and identify bugs, security issues, and quality problems. This simulates a real-world task that software engineers do daily.

## Supported Languages
- Python 🐍
- JavaScript 🌐
- Java ☕

## Action Space
| Field | Type | Description |
|-------|------|-------------|
| has_syntax_error | bool | Does the code have syntax errors? |
| quality_score | float | Code quality score 0.0-1.0 |
| issues | list | List of issues found |
| severity | str | low / medium / high |

## Observation Space
| Field | Type | Description |
|-------|------|-------------|
| code_snippet | str | Code to review |
| language | str | Programming language |
| task_type | str | easy / medium / hard |
| task_description | str | What to look for |
| score | float | Score for last action |
| feedback | str | Feedback on last action |

## Tasks
- Easy: Detect syntax errors (baseline: 0.85)
- Medium: Find code quality issues (baseline: 0.65)
- Hard: Full review - bugs, security, performance (baseline: 0.45)

## Reward Function
- +0.3 correct syntax detection
- +0.2 correct severity
- +0.5 issues found correctly
- All scores strictly between 0.01 and 0.99

## Baseline Scores
| Task | Score |
|------|-------|
| Easy | 0.85 |
| Medium | 0.65 |
| Hard | 0.45 |
| Average | 0.65 |

## Setup
pip install openenv-core

## API Endpoints
- POST /reset - Start new episode
- POST /step - Execute action
- GET /state - Get current state
- GET /health - Health check
