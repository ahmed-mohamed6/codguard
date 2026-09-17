from graph.chains.validator import finding_validator
from graph.state import GraphState


def validate_findings(state: GraphState) -> dict:
    """Validate each finding and keep only valid findings."""

    print("....... VALIDATING FINDINGS .......")

    code = state["code"]
    findings = state["findings"]

    valid_findings = []

    for finding in findings:
        print(f"\nVALIDATING: {finding.description}")

        result = finding_validator.invoke({
            "code": code,
            "finding": finding,
        })

        if result.is_valid:
            print(f"VALID: {result.reason}")
            valid_findings.append(finding)
        else:
            print(f"INVALID: {result.reason}")

    print(
        f"\nValidation complete: "
        f"{len(valid_findings)}/{len(findings)} findings are valid."
    )

    return {
        "findings": valid_findings
    }