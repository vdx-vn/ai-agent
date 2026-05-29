# v19 Notes — Business HR

## hr.expense.sheet removed (cross-app impact on HR)
- `hr.expense.sheet` model removed in v19; expense approval now on `hr.expense` directly
- HR flows linking employees to expense sheets must be updated to link to `hr.expense`
- `former_sheet_id` field on `hr.expense` provides historical reference

## HR doc structure
- `content/applications/hr.rst` is a thin toctree stub in v19
- Real HR content: `content/applications/hr/` subdirectory (payroll, attendance, time off, etc.)

## View tag rename
- `<tree>` → `<list>` in HR list views (employees, contracts, attendances)
