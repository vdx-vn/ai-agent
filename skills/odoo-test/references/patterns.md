# Advanced Test Patterns

Pick the pattern that matches your scenario:

| Scenario | Pattern |
|----------|---------|
| Test depends on current date/time | `freeze_time` |
| Test sends email / notifications | `mock_mail_gateway` |
| Test expects `AccessError` | `assertRaises` + `mute_logger` |
| Test checks onchange / view defaults | `Form` object |
| Test uses a wizard | Create → set fields → call action → assert |
| Test guards against perf regression | `assertQueryCount` + `@warmup` |
| Test involves multiple companies | `setup_other_company` + `with_company` |
| Test checks WebSocket / bus messages | `assertBus` |
| Test data needs stable XML IDs | `_load_records` |
| Fixture with many2many fields | `Command.link` / `Command.set` |
| State machine / stage transitions | Assert state before and after each step |
| Queue / async job | Call job method directly; mock dispatch |

---

## freeze_time

```python
from freezegun import freeze_time

with freeze_time("2024-01-15"):
    cron.method_direct_trigger()
    self.assertEqual(record.state, 'posted')
```

For cron/scheduler tests also wrap with `enter_registry_test_mode()`:

```python
with freeze_time("2024-01-15"), self.enter_registry_test_mode():
    cron.method_direct_trigger()
```

---

## mock_mail_gateway

```python
with self.mock_mail_gateway(mail_unlink_sent=False):
    record.action_send()
    self.assertEqual(len(self._new_mails), 1)
    self.assertIn('Invoice', self._new_mails[0].subject)
```

---

## Access Control (assertRaises + mute_logger)

```python
from odoo.exceptions import AccessError
from odoo.tools import mute_logger

@mute_logger('odoo.addons.base.models.ir_model', 'odoo.addons.base.models.ir_rule')
def test_user_cannot_read(self):
    with self.assertRaises(AccessError):
        record.with_user(self.user_b).read()
```

Use `with_user()` to switch context mid-test without a new environment:

```python
order_as_manager = order.with_user(self.user_manager)
order_as_manager.action_confirm()
```

---

## Form (onchange / view defaults)

Only use `Form` when testing onchange behavior, computed defaults, or form-level restrictions.
For simple model logic with no onchange — use direct ORM calls instead.

```python
from odoo.tests import Form

form = Form(self.env['sale.order'])
form.partner_id = self.partner
with form.order_line.new() as line:
    line.product_id = self.product
    self.assertEqual(line.price_unit, self.product.list_price)
order = form.save()
```

---

## Wizard

```python
wizard = self.env['my.wizard'].with_context(active_ids=records.ids).create({
    'field_a': 'value',
})
wizard.action_confirm()
self.assertFalse(records.filtered(lambda r: r.state != 'done'))
```

For multi-step wizards use `assertRecordValues` to assert all fields at once:

```python
self.assertRecordValues(wizard.line_ids, [
    {'display_type': 'line_section', 'record_id': record_1.id},
    {'display_type': 'account',      'record_id': record_2.id},
])
```

---

## assertQueryCount (performance)

```python
from odoo.tests.common import warmup

@warmup
def test_perf(self):
    with self.assertQueryCount(manager=45):
        self.env['crm.lead'].with_user(self.manager)._assign()
```

---

## Multi-Company

```python
cls.company_data_2 = cls.setup_other_company()

record = self.env['account.account'].create({
    'code': '180001',
    'name': 'Account in Company 2',
    'company_ids': [Command.link(self.company_data_2['company'].id)],
})
self.assertRecordValues(
    record.with_company(self.company_data_2['company']),
    [{'code': '180001'}],
)
```

---

## assertBus (WebSocket / real-time notifications)

```python
with self.assertBus(
    [(self.cr.dbname, 'res.partner', partner.id)],
    [{'type': 'mail.message/delete', 'payload': {'message_ids': [msg.id]}}],
):
    msg.unlink()
```

---

## _load_records (stable XML IDs)

Use when test data needs stable XML IDs for later `env.ref()` lookups:

```python
cls.accounts = cls.env['account.account']._load_records([
    {
        'xml_id': 'my_module.test_account_receivable',
        'values': {
            'name': 'Test Receivable',
            'code': '100100',
            'account_type': 'asset_receivable',
        },
    },
])
```

---

## Command (many2many in fixtures)

Use `Command` instead of raw `[(4, id)]` tuples — it is the supported API since Odoo 15.

```python
from odoo.models import Command

cls.record = cls.env['my.model'].create({
    'name': 'Test',
    # Link existing records
    'tag_ids': [Command.link(cls.tag_a.id), Command.link(cls.tag_b.id)],
    # Replace the entire set
    'user_ids': [Command.set([user1.id, user2.id])],
    # Create and link inline
    'line_ids': [Command.create({'name': 'Line 1', 'qty': 1.0})],
})
```

---

## State Machine / Stage Transitions

Test each valid transition individually. Assert the state before the action so the test fails clearly if preconditions change.

```python
def test_confirm_moves_to_in_progress(self):
    self.assertEqual(self.request.state, 'draft')
    self.request.action_confirm()
    self.assertEqual(self.request.state, 'in_progress')

def test_cannot_confirm_cancelled_request(self):
    self.request.action_cancel()
    with self.assertRaises(UserError):
        self.request.action_confirm()
```

For multi-step flows, walk through the full path and assert at each step:

```python
def test_full_approval_flow(self):
    self.request.action_submit()
    self.assertEqual(self.request.state, 'submitted')
    self.request.with_user(self.manager).action_approve()
    self.assertEqual(self.request.state, 'approved')
    self.request.action_done()
    self.assertRecordValues(self.request, [{'state': 'done', 'date_done': fields.Date.today()}])
```

---

## Queue / Async Jobs

Do not enqueue — call the job method directly in tests. Mock the enqueue call if you only want to verify it was triggered.

```python
# Call directly — no queue, synchronous, inspectable
def test_sync_job_processes_records(self):
    self.env['my.queue.job'].with_context(test_mode=True)._run_sync(self.records)
    self.assertTrue(all(r.state == 'done' for r in self.records))

# Verify job was enqueued without running it
from unittest.mock import patch

def test_action_triggers_job(self):
    with patch.object(type(self.env['my.model']), '_enqueue_sync') as mock_enqueue:
        self.record.action_start_sync()
        mock_enqueue.assert_called_once()
```

Always assert the **full expected outcome** (all records processed), not just absence of exceptions — partial failures may silently succeed in batch operations using savepoints.
