from langgraph.types import interrupt

from graph.state import GraphState


def human_approval(state: GraphState):
    print("....... WAITING FOR HUMAN APPROVAL .......")

    findings = state["findings"]

    review_text = "\n\n".join(
        [
            f"""
Severity: {finding.severity}
Category: {finding.category}

Description:
{finding.description}

Suggestion:
{finding.suggestion}
File:
{finding.file}
Line:
{finding.line}
"""
            for finding in findings
        ]
    )

    while True:
        decision = interrupt(
            {
                "message": "CodeGuard found the following issues. Approve or reject the review.",
                "findings": review_text,
            }
        )
        decision = str(decision).strip().lower()
        if decision in ["approve", "reject"]:
            break

        print(f"Invalid decision: {decision}")

    print(f"Human decision: {decision}")

    return {
        "human_decision": decision
    }

def route_after_human_approval(state: GraphState):
    if state["human_decision"] == "approve":
        return "approved"

    return "rejected"