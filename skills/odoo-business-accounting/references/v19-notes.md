# v19 Notes — Business Accounting

## hr.expense.sheet removed (accounting impact)
- `hr.expense.sheet` removed; expense journal entries now originate from `hr.expense` directly
- Reconciliation and posting flows that referenced sheet-level moves must target `hr.expense`
- `former_sheet_id` on `hr.expense` for traceability

## View tag rename
- `<tree>` → `<list>` in accounting list views (journal entries, invoices, moves)

## Doc structure
- Finance docs now in subdirectories under `content/applications/finance/`
- `content/applications/finance/accounting.rst` may be a stub; use `content/applications/finance/accounting/` for deep links
