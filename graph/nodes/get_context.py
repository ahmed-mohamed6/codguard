from graph.tools.github_tools import get_file_content
from graph.state import GraphState


def get_context(state: GraphState):
    print(".....Getting context......")

    file_path = state["file_path"]

    new_context = get_file_content.invoke({
        "file_path": file_path
    })

    current_context = state["context"]

    if current_context:
        combined_context = (
            current_context
            + f"\n\n--- {file_path} ---\n"
            + new_context
        )
    else:
        combined_context = (
            f"--- {file_path} ---\n"
            + new_context
        )

    return {
        "context": combined_context,
        "context_requests": state["context_requests"] + 1

    }