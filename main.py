from langgraph.types import Command

from graph.graph import app


config = {
    "configurable": {
        "thread_id": "full-graph-test-1"
    }
}


initial_state = {
    "code": "",
    "needs_context": False,
    "context": "",
    "findings": [],
    "file_path": None,
    "context_requests": 0,
    "human_decision": None,
    "github_review_url": None,
}


print("\n========== STARTING CODEGUARD ==========\n")

result = app.invoke(
    initial_state,
    config,
)

print("\n========== GRAPH INTERRUPTED ==========\n")

print(result["__interrupt__"])


decision = input("\nApprove or reject? ")

result = app.invoke(
    Command(resume=decision.strip().lower()),
    config,
)


print("\n========== FINAL RESULT ==========\n")

print("Human decision:")
print(result["human_decision"])

print("\nFindings:")

for finding in result["findings"]:
    print(f"\nSeverity: {finding.severity}")
    print(f"Category: {finding.category}")
    print(f"Description: {finding.description}")
    print(f"Suggestion: {finding.suggestion}")
    print(f"File: {finding.file}")
    print(f"Line: {finding.line}")

print("\nGitHub review URL:")
print(result.get("github_review_url"))