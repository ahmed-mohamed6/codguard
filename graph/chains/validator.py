from dotenv import load_dotenv
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_openrouter import ChatOpenRouter
from pydantic import BaseModel, Field

load_dotenv()

model = os.getenv("VALIDATOR_MODEL")

llm = ChatOpenRouter(
    model=model,
    temperature=0,
)


class ValidationResult(BaseModel):
    is_valid: bool | None = Field(
        description="Whether the finding is valid and sufficiently supported by the provided code."
    )

    reason: str | None = Field(
        description="A concise explanation for why the finding is valid or invalid."
    )


structured_validator = llm.with_structured_output(ValidationResult)


system = """
You are a senior software engineer responsible for validating AI-generated
code review findings.

Your task is to determine whether the provided finding is a legitimate
and actionable issue in the provided code.

A finding is valid only if:

1. The issue is actually supported by the provided code.
2. The described behavior is technically plausible.
3. The issue is relevant to the code being reviewed.
4. The suggested fix is reasonable for the identified issue.
5. The finding is not based on unsupported assumptions.

Reject findings that are:
- False positives
- Too vague to verify
- Based on assumptions about code that was not provided
- Technically incorrect
- Unrelated to the provided code
- Merely stylistic preferences presented as real bugs

Be conservative. If there is insufficient evidence to confirm the issue,
mark the finding as invalid.

Return only the structured validation result.
"""


validation_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        (
            "human",
            """
Review the following code and validate the proposed finding.

Code:
{code}

Finding:
{finding}
"""
        ),
    ]
)


finding_validator = validation_prompt | structured_validator

# result = finding_validator.invoke({
#     "code": """
#     def divide(a, b):
#         return a / b
# """,
#     "finding": """
#     severity=2 category='Correctness' description='No type validation; non-numeric inputs cause TypeError.' suggestion='Add type checks or rely on type hints and let callers handle errors, but document expected types.'
#     """
# })
# print(result)