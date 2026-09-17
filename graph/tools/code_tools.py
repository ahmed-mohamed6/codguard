from langchain_core.tools import tool


@tool
def get_file_content(file_path: str) -> str:
    """Get the content of a related source code file."""
    print(f"\nGetting file content from '{file_path}'...")
    files = {
        "user_service.py": """
class UserService:

    def get_user(self, user_id):
        user = self.repository.get(user_id)

        if user is None:
            return None

        return user
""",
        "auth_service.py": """
class AuthService:

    def authorize(self, user):
        return user.role == "admin"
""",
    }

    return files.get(
        file_path,
        f"File '{file_path}' was not found."
    )