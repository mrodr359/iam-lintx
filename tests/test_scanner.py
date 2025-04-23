from iam_lintx.scanner import scan_json_policy


def test_scan_policy_detects_wildcard_action(tmp_path):
    # Create a test policy with a wildcard action
    policy_data = {
        "Version": "2012-10-17",
        "Statement": [{"Effect": "Allow", "Action": "*", "Resource": "*"}],
    }

    # Write to a temporary JSON file
    policy_file = tmp_path / "test_policy.json"
    policy_file.write_text(str(policy_data).replace("'", '"'))  # make it valid JSON

    # Run the scan
    issues = scan_json_policy(policy_file)

    # Assert a wildcard action was found
    assert len(issues) == 2
    assert any("wildcard Action" in issue["message"] for issue in issues)
    assert any("wildcard Resource" in issue["message"] for issue in issues)


def test_scan_policy_detects_wildcard_resource(tmp_path):
    policy_data = {
        "Version": "2012-10-17",
        "Statement": [{"Effect": "Allow", "Action": "s3:ListBucket", "Resource": "*"}],
    }

    policy_file = tmp_path / "test_resource_policy.json"
    policy_file.write_text(str(policy_data).replace("'", '"'))

    issues = scan_json_policy(policy_file)

    assert len(issues) == 1
    assert issues[0]["type"] == "WARN"
    assert "wildcard Resource" in issues[0]["message"]


def test_scan_policy_warns_on_sensitive_action_without_condition(tmp_path):
    policy_data = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": "s3:PutObject",
                "Resource": "arn:aws:s3:::example-bucket/*",
                # No Condition block
            }
        ],
    }

    policy_file = tmp_path / "test_sensitive.json"
    policy_file.write_text(str(policy_data).replace("'", '"'))

    issues = scan_json_policy(policy_file)

    assert len(issues) == 1
    assert issues[0]["type"] == "SUGGESTION"
    assert "without a Condition" in issues[0]["message"]
