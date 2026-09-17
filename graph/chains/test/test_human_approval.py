from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command

from graph.nodes.human_approve import human_approval
from graph.state import GraphState
from graph.chains.code_reviewer import Finding


# Build a tiny graph containing only the human approval node

builder = StateGraph(GraphState)

builder.add_node("HUMAN_APPROVAL", human_approval)

builder.add_edge(START, "HUMAN_APPROVAL")
builder.add_edge("HUMAN_APPROVAL", END)

checkpointer = InMemorySaver()

app = builder.compile(
    checkpointer=checkpointer
)


# Fake findings for testing

findings = [
    Finding(
        severity=8,
        category="security",
        description="User input is used without validation.",
        suggestion="Validate the user input before processing it."
    ),
    Finding(
        severity=5,
        category="code_quality",
        description="The method does not handle the missing user case explicitly.",
        suggestion="Handle the missing user case with a clear response."
    ),
]


config = {
    "configurable": {
        "thread_id": "human-approval-test"
    }
}


initial_state = {
    "code": "",
    "needs_context": False,
    "context": "",
    "findings": findings,
    "file_path": None,
    "context_requests": 0,
    "human_decision": None,
}


print("\nStarting Human Approval test...\n")

result = app.invoke(
    initial_state,
    config
)

print("\nGraph interrupted.")

print("\nInterrupt information:")
print(result)
decision = input("\nApprove or reject? ")

result = app.invoke(
    Command(resume=decision),
    config,
)

print("\n========== FINAL RESULT ==========\n")
print(result)