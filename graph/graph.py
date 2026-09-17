from langgraph.graph import END, START, StateGraph

from graph.consts import (
    DECIDE_CONTEXT,
    GET_CONTEXT,
    REVIEW_CODE,
    VALIDATE_FINDINGS,
    GET_PR_FILES,
    HUMAN_APPROVAL,
    UPDATE_PULL_REQUEST,
)

from graph.nodes.review_code import review_code
from graph.nodes.validate_findings import validate_findings
from graph.nodes.decide_context import (
    decide_context,
    route_after_context_decision,
)
from graph.nodes.get_context import get_context

from graph.nodes.get_pr_files import get_pr_files

from graph.nodes.human_approve import human_approval , route_after_human_approval

from graph.nodes.update_pull_request import update_pull_request

from graph.state import GraphState

from langgraph.checkpoint.memory import InMemorySaver

checkpointer = InMemorySaver()


graph = StateGraph(GraphState)

graph.add_node(GET_PR_FILES, get_pr_files)
graph.add_node(DECIDE_CONTEXT, decide_context)
graph.add_node(GET_CONTEXT, get_context)
graph.add_node(REVIEW_CODE, review_code)
graph.add_node(VALIDATE_FINDINGS, validate_findings)
graph.add_node(HUMAN_APPROVAL, human_approval)
graph.add_node(UPDATE_PULL_REQUEST, update_pull_request)


graph.add_edge(START, GET_PR_FILES)

graph.add_edge(GET_PR_FILES, DECIDE_CONTEXT)

graph.add_conditional_edges(
    DECIDE_CONTEXT,
    route_after_context_decision,
    {
        GET_CONTEXT: GET_CONTEXT,
        REVIEW_CODE: REVIEW_CODE,
    },
)

graph.add_edge(GET_CONTEXT, DECIDE_CONTEXT)

graph.add_edge(REVIEW_CODE, VALIDATE_FINDINGS)

graph.add_edge(VALIDATE_FINDINGS, HUMAN_APPROVAL)

graph.add_conditional_edges(
    HUMAN_APPROVAL,
    route_after_human_approval,
    {
        "approved": UPDATE_PULL_REQUEST,
        "rejected": END,
    },
)
graph.add_edge(UPDATE_PULL_REQUEST, END)

app = graph.compile(checkpointer=checkpointer)