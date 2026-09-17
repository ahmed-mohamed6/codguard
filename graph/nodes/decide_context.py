from graph.chains.context_decider import context_decider
from graph.state import GraphState
MAX_CONTEXT_REQUESTS = 1

def decide_context(state: GraphState) -> dict:
    print(".....Deciding context......")
    result = context_decider.invoke({
        "code": state["code"],
        "context": state["context"],
    })

    return {
        "needs_context": result.needs_context,
        "file_path": result.file_path,
    }


def route_after_context_decision(state: GraphState):

    if state["needs_context"]:
        if state["context_requests"] >= MAX_CONTEXT_REQUESTS:
            print("Maximum context requests reached.")
            return "review_code"

        return "get_context"

    return "review_code"