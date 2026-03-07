# Odoo Planning Examples

Worked examples for Odoo requirement normalization and planning.

## Example 1: Approval Request Module

### Request
"Create an approval request module for internal spending requests. Employees submit requests, managers approve or reject them, and finance validates payment status."

## Requirements Output Shape

```markdown
# Requirements: Approval Request

## Source
- Type: prompt
- Notebook: 
- Summary: Internal spending approval workflow

## Business Requirements
- Employee can create spending request
- Request has amount, reason, department, requester, approver, and payment status
- Manager can approve or reject
- Finance can mark as paid
- Users cannot edit approved requests except allowed roles

## Models
### Approval Request
- Purpose: Main approval document
- Main fields: name, requester_id, department_id, amount, reason, state, payment_status
- Workflow states: draft, submitted, approved, rejected, paid
- Buttons: submit, approve, reject, mark_paid
- Tabs: details, approvals, finance_notes
- Security: employee create own, manager approve, finance update payment info
```

## Discovery Notes
- Existing employee/department relations may be reusable from HR modules
- State flow requires statusbar and button visibility logic
- Security requires ACL + record rules

## Approach Summary
- Create main model `x_approval.request`
- Add `many2one` fields for employee, department, manager
- Use selection field for `state` and `payment_status`
- Build form view with notebook tabs: Details, Approval, Finance
- Restrict editing after approval except finance payment fields

---

## Example 2: NotebookLM-Sourced Purchase Customization

### Request
"Use NotebookLM notebook Purchase Custom to plan the module"

## Planning Flow
1. Detect notebook name: `Purchase Custom`
2. Load `notebooklm-project`
3. Fetch all requirements from the notebook
4. Normalize into `requirements.md`
5. Convert into model/view/action/security structure

## Expected `requirements.md` Content
- Full requirement text from NotebookLM
- JSON definition of purchase request models
- Assumptions separated from confirmed requirements
- Open questions for unclear approval or vendor logic

## Typical Design Result
- Extend purchase-related models or define a new request model
- Add approval states
- Add tabs for line items, approval trail, vendor notes
- Add actions for submit/approve/reject/convert
- Define manager and purchase officer permissions

---

## Decision Tree: When to Use NotebookLM

```text
User explicitly provides notebook name?
├── YES → Read NotebookLM requirements first
└── NO  → Plan from prompt and mark assumptions
```

## Decision Tree: Odoo Planning Focus

```text
Requirements ready?
├── NO  → Normalize into requirements.md first
└── YES → Discovery → Synthesis → Verification → Work Packages → Execution Order
```
