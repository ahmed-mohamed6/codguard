from graph.chains.code_reviewer import code_reviewer
from graph.state import GraphState


def review_code(state: GraphState) -> dict:
    print("........ CHECKING YOUR CODE ........")

    result = code_reviewer.invoke({
        "code": state["code"] ,
        "additional_context": state["context"]
    })

    print(f"\nOverall Review:\n{result.text}")

    if result.findings:
        print("\nIssues found:\n")

        for finding in result.findings:
            print(f"[{finding.severity}/10] {finding.category}")
            print(f"{finding.description}")
            print(f"Suggestion: {finding.suggestion}\n")
    else:
        print("\nNo issues found.")

    return {
        "findings": result.findings
    }