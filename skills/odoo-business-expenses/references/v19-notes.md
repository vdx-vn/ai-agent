# v19 Notes — Business Expenses

## hr.expense.sheet model removed (primary v19 change)
- `hr.expense.sheet` model removed in v19
- Expenses are now flat records on `hr.expense` with approval state directly on the expense
- `former_sheet_id` breadcrumb field available on `hr.expense` for historical traceability
- Source: `addons/hr_expense/models/hr_expense.py` (canonical); `hr_expense_sheet.py` removed

## Workflow impact
- Submit → Approve → Post flow now operates entirely on `hr.expense` records
- Sheet-level approval reports and wizards must be replaced with expense-level equivalents
- ACLs referencing `hr.expense.sheet` must be updated to `hr.expense`

## View tag rename
- `<tree>` → `<list>` in expense list views
