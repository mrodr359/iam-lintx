import json
from pathlib import Path

SENSITIVE_ACTIONS = [
    "s3:PutObject",
    "s3:DeleteObject",
    "ec2:StartInstances",
    "ec2:StopInstances",
    "iam:PassRole",
    "kms:Decrypt",
    "kms:Encrypt",
]


def scan_json_policy(file_path: Path) -> list[dict]:
    """
    Scans a JSON IAM policy file for wildcard Actions.
    Returns a list of issue dictionaries.
    """
    issues = []

    try:
        with open(file_path, "r") as f:
            policy = json.load(f)
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON")

    statements = policy.get("Statement", [])
    if not isinstance(statements, list):
        statements = [statements]

    for idx, stmt in enumerate(statements):
        action = stmt.get("Action")
        if action == "*":
            issues.append(
                {
                    "type": "WARN",
                    "statement_index": idx,
                    "message": 'Statement uses wildcard Action: "*"',
                }
            )

        resource = stmt.get("Resource")
        if resource == "*":
            issues.append(
                {
                    "type": "WARN",
                    "statement_index": idx,
                    "message": 'Statement uses wildcard Resource: "*"',
                }
            )

    condition = stmt.get("Condition")
    action = stmt.get("Action")

    # Normalize action into a list (can be str or list)
    actions = [action] if isinstance(action, str) else action or []

    if condition is None:
        for act in actions:
            if act.lower() in [a.lower() for a in SENSITIVE_ACTIONS]:
                issues.append(
                    {
                        "type": "SUGGESTION",
                        "statement_index": idx,
                        "message": f'Statement grants sensitive action "{act}" without a Condition block',
                    }
                )

    return issues
