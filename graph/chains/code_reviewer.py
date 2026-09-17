from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openrouter import ChatOpenRouter
from pydantic import BaseModel, Field

load_dotenv()

#"nvidia/nemotron-3-super-120b-a12b:free"
llm = ChatOpenRouter(
    #model="nvidia/nemotron-3-super-120b-a12b:free",
    model="openai/gpt-oss-120b",
    temperature=0,
)


class Finding(BaseModel):
    severity: int = Field(
        ge=1,
        le=10,
        description="Severity of the issue from 1 to 10, where 1 is minimal and 10 is extremely severe."
    )

    category: str = Field(
        description="Category of the issue: bug, security, performance, or code_quality."
    )

    description: str = Field(
        description="Clear and concise description of the issue."
    )

    suggestion: str = Field(
        description="Practical and actionable suggestion to fix the issue."
    )
    file:str = Field(
        description="File path of the issue."
    )
    line:int = Field(
        description="Line number of the issue."
    )

class Review(BaseModel):
    """Structured review of the provided code."""

    text: str = Field(
        description="A concise overall review of the code."
    )

    findings: list[Finding] = Field(
        description="Genuine and actionable issues identified in the code."
    )


structured_review = llm.with_structured_output(Review)


system = """
You are an expert software engineer and code reviewer.

Your task is to review the provided code and identify genuine issues
that could negatively affect the software.

Focus on:
- Bugs and incorrect behavior
- Security vulnerabilities
- Performance problems
- Error handling issues
- Edge cases
- Maintainability and code quality

Only report issues that are reasonably supported by the provided code.
Do not invent problems or make assumptions about code that is not provided.

For each identified issue, provide a clear and concise explanation.
If no issues are found, return an empty bugs list.

Keep the review practical, precise, and actionable.
"""


code_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "Review the following code:\n\n{code}\n\n and here is additional context:\n\n{additional_context}"),
    ]
)


code_reviewer = code_prompt | structured_review
