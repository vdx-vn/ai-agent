# Skill: Odoo API Integration

## Goal
Integrate external systems with safe networking and retries.

## Tools
- `requests` or `urllib3` usage (depending on Odoo version/base libs)
- Use `ir.cron` for scheduled sync
- Store tokens in `ir.config_parameter` or encrypted fields (if available)

## Rules
- Timeouts always set
- Retry with backoff for transient failures
- Log meaningful messages (no leaking secrets)
- Use queue models if sync is heavy

## Example Prompt
"Sync customer data from an external REST API nightly with error tracking."
