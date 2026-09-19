# CodeGuard 🛡️

CodeGuard is an **AI-powered code review agent** that automatically analyzes GitHub repository code, identifies potential issues, and provides actionable suggestions.

It uses **LangGraph** to build an agentic workflow that can decide when it needs additional code context before completing a review.

## What Does It Do?

CodeGuard can:

- 🔍 Analyze source code from a GitHub repository.
- 🤖 Use an LLM to review the code and detect potential issues.
- 🧠 Request additional files when more context is needed.
- 🔄 Manage the review process using a LangGraph workflow.
- 👤 Pause for **human approval** before finalizing the review.
- 🐳 Run as a Docker container.

## Workflow

```text
GitHub Repository
       ↓
Get Code
       ↓
Decide if More Context Is Needed
       ↓
Fetch Additional Files
       ↓
AI Code Review
       ↓
Human Approval
       ↓
Final Findings
```

## Tech Stack

- Python
- LangChain
- LangGraph
- OpenAI-compatible LLM APIs
- GitHub API
- Docker
- uv

## Example Findings

CodeGuard can identify issues such as:

- Security vulnerabilities
- Poor coding practices
- Potential bugs
- Performance problems
- Maintainability issues

For each finding, CodeGuard provides information such as its severity, category, description, and a suggested improvement.

## Running with Docker

Pull the image:

```bash
docker pull ahmedmohamed6/codeguard:1.0
```

Then run it while providing your environment variables:

```bash
docker run --env-file .env ahmedmohamed6/codeguard:1.0
```

## Running Locally

Clone the repository and install the dependencies using `uv`.

Then configure your environment variables in a `.env` file and run:

```bash
uv run python main.py
```

## Project Goal

CodeGuard was built as a practical project to demonstrate how **LLM-powered agents, LangChain, LangGraph, tool usage, context management, and human-in-the-loop workflows** can be combined to build an AI software-engineering tool.
