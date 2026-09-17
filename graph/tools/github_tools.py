import os
import base64
from dotenv import load_dotenv
from graph.tools.git_res import ChangedFile
import requests
from dotenv import load_dotenv
from langchain_core.tools import tool

load_dotenv()


BASE_URL = "https://api.github.com"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
BASE_URL = "https://api.github.com"
owner = os.getenv("OWNER")
repo = os.getenv("REPO")
pull_number = os.getenv("PULL_NUMBER")

@tool
def get_pull_request_files() -> list[ChangedFile]:
    """Get the files changed in a GitHub pull request."""

    print(
        f"Getting files for PR #{pull_number} "
        f"from {owner}/{repo}..."
    )

    url = (
        f"{BASE_URL}/repos/"
        f"{owner}/{repo}/pulls/{pull_number}/files"
    )

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=30,
    )

    response.raise_for_status()

    files = response.json()

    return [
        ChangedFile(
            filename=file["filename"],
            status=file["status"],
            additions=file["additions"],
            deletions=file["deletions"],
            changes=file["changes"],
            patch=file.get("patch"),
        )
        for file in files
    ]

def format_changed_files(files: list[ChangedFile]) -> str:
    sections = []

    for file in files:
        sections.append(
            f"""
--- File: {file.filename} ---
Status: {file.status}
Changes: +{file.additions} -{file.deletions}

{file.patch or "No patch available."}
"""
        )

    return "\n".join(sections)

@tool
def get_file_content(file_path: str) -> str:
    """Get the content of a file from the GitHub repository."""

    print(f"Getting file content: {file_path}")

    url = (
        f"{BASE_URL}/repos/"
        f"{owner}/{repo}/contents/{file_path}"
    )

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=30,
    )

    response.raise_for_status()

    data = response.json()

    if data["type"] != "file":
        raise ValueError(
            f"'{file_path}' is not a file."
        )

    content = base64.b64decode(
        data["content"]
    ).decode("utf-8")

    return content

def create_pull_request_review(body: str) -> dict:
    """Create a review on the configured GitHub pull request."""

    url = (
        f"{BASE_URL}/repos/"
        f"{owner}/{repo}/pulls/{pull_number}/reviews"
    )

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    payload = {
        "body": body,
        "event": "COMMENT",
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=30,
    )

    response.raise_for_status()

    return response.json()