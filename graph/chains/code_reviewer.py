from dotenv import load_dotenv
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_openrouter import ChatOpenRouter
from graph.models.review import Review
from graph.models.finding import Finding


load_dotenv()

model = os.getenv("REVIEWER_MODEL")
llm = ChatOpenRouter(
    model=model,
    temperature=0,
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
