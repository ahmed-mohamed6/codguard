from graph.state import GraphState
from graph.tools.github_tools import (
    get_pull_request_files,
    format_changed_files,
)
from dotenv import load_dotenv
load_dotenv()
import os


def get_pr_files(state: GraphState):
    print(".....Getting PR files......")

    files = get_pull_request_files.invoke({})

    code = format_changed_files(files)

    print(f"Retrieved {len(files)} changed files.")

    return {
        "code": code
    }