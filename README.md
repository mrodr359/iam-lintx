# 🔐 iam-lintx

**A lightweight, developer-friendly CLI tool to analyze and validate AWS IAM policies in JSON and Terraform formats.**  
Built for cloud engineers, security teams, and DevOps pipelines.

![CI](https://img.shields.io/badge/status-active-brightgreen)  
[MIT License](./LICENSE)

---

## ✨ Features

- ✅ Scan **JSON** IAM policies or **Terraform** IAM resources
- ✅ Identify over-permissive actions and missing security conditions
- ✅ Assign a **risk score (0–100)** with severity rating
- ✅ Generate **Markdown audit reports**
- ✅ Designed for **CI/CD pipelines**, developer workflows, and PR comments
- ✅ Fast, extensible, and open source

---

## 🚀 Quick Start

### 📦 Install

```bash
pip install iam-lintx
```

### 🧪 Scan a policy file

```bash
iam-lintx scan examples/policy.json --score
```

### 📁 Scan a Terraform file

```bash
iam-lintx scan examples/iam.tf --report md --output report.md
```

## 🧠 Sample Output

```csharp
[WARN] Statement uses "Action": "*"
[WARN] Wildcard resource detected
[SUGGESTION] Add "Condition" for sensitive actions like s3:PutObject

Risk Score: 62/100 – HIGH RISK
```
## 📄 Example Markdown Report

```markdown
# IAM Lintx Scan Report

**Risk Score:** 62/100 (High Risk)

- Wildcard Action: "*"
- _Wildcard Resource_: "*"
- Missing Condition Block

Suggestions:
- Limit actions to specific services
- Add conditions like IP/mfa for sensitive operations
```

## 🔎 What We're Trying to Solve

Managing IAM policies at scale — especially across Terraform and JSON — is tedious, risky, and prone to human error.

We're building `iam-lintx` to help developers and DevOps teams:

- ✅ Detect overly permissive IAM policies early
- ✅ Understand the *real* risk level of their access definitions
- ✅ Standardize security checks across cloud environments and CI/CD
- ✅ Shift IAM security left — before it hits production

Whether you're writing custom policies or auditing team contributions, `iam-lintx` helps keep your infrastructure secure, compliant, and reviewable.

## License

This project is licensed under the [MIT License](./LICENSE).  
Feel free to use, modify, and contribute — contributions and PRs are welcome!
