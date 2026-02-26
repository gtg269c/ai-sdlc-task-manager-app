# Plan: AWS CloudFormation Deployment — Task Manager Backend

**Date:** 2026-02-26
**Author:** Cloud Architect (Claude)
**Sources:**
- `taskManager/app.py` — Flask app, 2 REST endpoints (`POST /tasks`, `GET /tasks`)
- `taskManager/task_service.py` — stores tasks in a local `tasks.json` file
- `aidlc-docs/design-artifacts/task_component_model.md`
- `aidlc-docs/design-artifacts/task_management_unit.md`
**Chosen architecture:** Option B — Lambda + API Gateway + DynamoDB (serverless)
**Target region:** `us-east-1`
**Output folder:** `DEPLOYMENT/`

---

## Architectural Observations (from code review)

| Concern | Current behaviour | Cloud treatment |
|---------|-------------------|-----------------|
| Storage | `tasks.json` on local filesystem | Replace with DynamoDB `put_item` / `scan` in `TaskService` |
| Runtime | Python 3, Flask, single process | Lambda Python 3.12, Flask wrapped with `aws-wsgi` WSGI adapter |
| Port | 5000 (dev mode) | API Gateway HTTP API terminates port 80/443 |
| Dependencies | `flask` only | Add `aws-wsgi`, `boto3` (boto3 is pre-installed in Lambda runtime) |

---

## AWS Resource Set

| CF Resource | Type | Purpose |
|-------------|------|---------|
| `TasksTable` | `AWS::DynamoDB::Table` | Persistent task storage; partition key `id` (String); PAY_PER_REQUEST |
| `LambdaExecutionRole` | `AWS::IAM::Role` | Lambda execution role; policies: `AWSLambdaBasicExecutionRole` + inline DynamoDB `PutItem`/`Scan` on `TasksTable` only |
| `TaskManagerFunction` | `AWS::Lambda::Function` | Python 3.12, handler `app.handler`, references S3 ZIP; env var `DYNAMODB_TABLE` |
| `TasksApi` | `AWS::ApiGatewayV2::Api` | HTTP API (not REST API — simpler, cheaper) |
| `TasksIntegration` | `AWS::ApiGatewayV2::Integration` | `AWS_PROXY` integration → Lambda |
| `DefaultRoute` | `AWS::ApiGatewayV2::Route` | `$default` route catches all paths/methods → integration |
| `DefaultStage` | `AWS::ApiGatewayV2::Stage` | `$default` auto-deploy stage with access logging |
| `LambdaInvokePermission` | `AWS::Lambda::Permission` | Allow API Gateway to invoke the Lambda function |
| `LogGroup` | `AWS::Logs::LogGroup` | CloudWatch log group for Lambda; 14-day retention |

---

## Code Changes Required to `TaskService`

The only required code change is in `task_service.py`:

| Method | Current | New |
|--------|---------|-----|
| `__init__` | loads from JSON file | accepts `table_name` from env var; creates boto3 DynamoDB resource |
| `_load()` | reads JSON file | `table.scan()` → returns list of `Task` |
| `_save()` | writes JSON file | replaced by `_put(task)` → `table.put_item()` called from `add_task` |

`app.py` and `task.py` are **unchanged**.

---

## Steps

- [x] **Step 1 — Read all source files and design artifacts**

- [x] **Step 2 — Write deployment_plan.md (this document)**

- [x] **Step 3 — Architecture choice confirmed**
  Chosen: **Option B — Lambda + API Gateway + DynamoDB**

- [x] **Step 4 — Region confirmed**
  Chosen: **`us-east-1`** (parameterised in template so it can be overridden)

- [ ] **Step 5 — Document prerequisites in plan**
  The following must exist before `aws cloudformation deploy` is run:
  1. An AWS account with programmatic access (access key + secret) or an IAM role assumed via SSO
  2. IAM permissions for the deploying user/role:
     `cloudformation:*`, `lambda:*`, `apigateway:*`, `dynamodb:*`,
     `iam:CreateRole`, `iam:AttachRolePolicy`, `iam:PutRolePolicy`,
     `iam:PassRole`, `logs:*`, `s3:PutObject`, `s3:GetObject`
  3. AWS CLI v2 installed and configured (`aws configure`)
  4. Python 3.12 and `pip` installed locally (for building the Lambda ZIP)
  5. An S3 bucket in `us-east-1` to upload the Lambda deployment package
     (the deployment guide will provide the `aws s3 mb` command)

- [ ] **Step 6 — Create `DEPLOYMENT/lambda/` source tree**
  Files:
  - `DEPLOYMENT/lambda/task.py` — copied unchanged from `taskManager/`
  - `DEPLOYMENT/lambda/task_service.py` — modified for DynamoDB
  - `DEPLOYMENT/lambda/app.py` — add `aws-wsgi` handler; read `DYNAMODB_TABLE` env var
  - `DEPLOYMENT/lambda/requirements.txt` — `flask`, `aws-wsgi`

- [ ] **Step 7 — Write `DEPLOYMENT/cloudformation-template.yaml`**
  CloudFormation YAML with:
  - `Parameters`: `EnvironmentName` (default `dev`), `LambdaS3Bucket`, `LambdaS3Key` (default `task-manager.zip`)
  - All 9 resources listed in the table above
  - `Outputs`: `ApiEndpoint` (the HTTP API invoke URL)
  - Full inline comments explaining every section

- [ ] **Step 8 — Write `DEPLOYMENT/deployment-guide.md`**
  Operator guide covering:
  1. Prerequisites checklist
  2. Package Lambda: `pip install -r requirements.txt -t package/ && zip -r task-manager.zip .`
  3. Upload ZIP to S3: `aws s3 cp task-manager.zip s3://<bucket>/task-manager.zip`
  4. Deploy stack: `aws cloudformation deploy ...`
  5. Retrieve endpoint URL from stack outputs
  6. Smoke-test with `curl` examples for both endpoints
  7. Tear-down: `aws cloudformation delete-stack ...`

- [ ] **Step 9 — Write validation plan and execute**
  Checks:
  | Check | Tool | What it validates |
  |-------|------|-------------------|
  | CF template syntax | `cfn-lint cloudformation-template.yaml` | Resource types, required props, deprecated features |
  | CF template parse | `aws cloudformation validate-template --template-body file://...` | AWS parser (dry-run) |
  | IAM least-privilege | Manual review | Lambda role has only needed DynamoDB actions on only `TasksTable` ARN |
  | Security group / network | N/A (Lambda is VPC-less) | Not applicable |
  | UserData | N/A | Not applicable |
  | Outputs | Manual review | `ApiEndpoint` is correct URL format |
  | Lambda handler reference | Manual review | `app.handler` resolves to the `handler` function in `app.py` |

- [ ] **Step 10 — Write `DEPLOYMENT/validation-report.md`**
  Table with: Check | Tool | Result (PASS/WARN/FAIL) | Notes / Remediation

- [ ] **Step 11 — Fix all FAIL items; re-run checks**
  Update `cloudformation-template.yaml` and `validation-report.md` until all items are PASS or justified WARN.

- [ ] **Step 12 — Commit and push to branch `claude/setup-project-structure-cFyY0`**

---

## Questions for the Approver

All critical decisions have been captured above and confirmed:

- [x] Deployment target: Lambda + API Gateway + DynamoDB
- [x] Region: us-east-1 (parameterised)

> **Please review this plan and confirm approval to proceed with Step 5 onwards.**
