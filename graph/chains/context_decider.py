from dotenv import load_dotenv
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_openrouter import ChatOpenRouter
from pydantic import BaseModel, Field


load_dotenv()

model = os.getenv("DECIDER_MODEL")

llm = ChatOpenRouter(
    model=model,
    temperature=0,
)


class ContextDecision(BaseModel):
    needs_context: bool | None = Field(
        description="Whether additional source code context is required."
    )

    file_path: str | None = Field(
        description="The related file that should be inspected if more context is needed. Null if no additional context is required."
    )

    reason: str = Field(
        default=None,
        description="A concise explanation for the decision."
    )


structured_decision = llm.with_structured_output(ContextDecision)


system = """
You are an expert software engineer reviewing source code.

Your task is to determine whether the provided code can be reliably
reviewed using only the currently available code and context.

Request additional context only when it is genuinely necessary to
understand the behavior of the code.

If additional context is needed:
- Set needs_context to true.
- Specify the most relevant file_path.
- Explain why it is needed.

If the provided code is sufficient:
- Set needs_context to false.
- Set file_path to null.

Do not request additional context merely because it might be useful.
Only request it when the current information is insufficient to make
a reliable review.
"""


context_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        (
            "human",
            """
Code being reviewed:

{code}

Additional context already available:

{context}

Determine whether additional source code context is required.
"""
        ),
    ]
)


context_decider = context_prompt | structured_decision