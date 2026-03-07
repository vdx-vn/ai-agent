# Automation and Workflow Reference

## Automated Actions

### Server Actions

```xml
<!-- data/ir_cron.xml -->
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data noupdate="1">
        <!-- Simple Server Action - Execute Python Code -->
        <record id="action_mark_done" model="ir.actions.server">
            <field name="name">Mark as Done</field>
            <field name="model_id" ref="model_my_model"/>
            <field name="state">code</field>
            <field name="code">
for record in records:
    if record.state == 'confirmed':
        record.action_done()
            </field>
        </record>

        <!-- Server Action - Create Record -->
        <record id="action_create_task" model="ir.actions.server">
            <field name="name">Create Task</field>
            <field name="model_id" ref="model_my_model"/>
            <field name="state">create</field>
            <field name="use_create">new</field>
            <field name="link_field_id" ref="field_my_model_task_ids"/>
            <!-- Target model configuration -->
            <field name="crud_model_id" ref="model_project_task"/>
            <field name="lines">
                <field name="value" eval="False"/>
                <field name="type">value</field>
                <field name="name">name</field>
            </field>
        </record>

        <!-- Server Action - Update Record -->
        <record id="action_update_state" model="ir.actions.server">
            <field name="name">Update State</field>
            <field name="model_id" ref="model_my_model"/>
            <field name="state">update</field>
            <field name="use_write">current</field>
            <field name="lines">
                <field name="col1" eval="True"/>
                <field name="col2" ref="state_done"/>
                <field name="type">value</field>
                <field name="name">state</field>
            </field>
        </record>

        <!-- Server Action - Send Email -->
        <record id="action_send_email" model="ir.actions.server">
            <field name="name">Send Confirmation Email</field>
            <field name="model_id" ref="model_my_model"/>
            <field name="state">email</field>
            <field name="template_id" ref="email_template_my_model"/>
        </record>

        <!-- Server Action - Execute Client Action -->
        <record id="action_client_action" model="ir.actions.server">
            <field name="name">Open Dashboard</field>
            <field name="model_id" ref="model_my_model"/>
            <field name="state">client_action</field>
            <field name="action_id" ref="action_my_dashboard"/>
        </record>

        <!-- Server Action - Trigger Next Action -->
        <record id="action_multi" model="ir.actions.server">
            <field name="name">Multi Step Action</field>
            <field name="model_id" ref="model_my_model"/>
            <field name="state">trigger</field>
            <field name="trigger_name">action_mark_done</field>
        </record>
    </data>
</odoo>
```

### Python Code in Server Actions

```python
# In server action code field:
# Can access: records, env, user, context

# Example 1: Loop through records
for record in records:
    record.message_post(body='Processed by automated action')
    record.write({'processed': True})

# Example 2: Create related records
for record in records:
    env['mail.message'].create({
        'res_id': record.id,
        'model': 'my.model',
        'body': 'Automatically created message',
    })

# Example 3: Compute and update
for record in records:
    total = sum(line.amount for line in record.line_ids)
    record.total_amount = total

# Example 4: Conditional logic
for record in records:
    if record.state == 'draft' and record.date <= fields.Date.today():
        record.action_confirm()
    elif record.state == 'confirmed':
        record.write({'urgent': True})

# Example 5: Using datetime
from datetime import timedelta
deadline = fields.Date.today() + timedelta(days=7)
for record in records:
    record.write({'reminder_date': deadline})

# Example 6: Send notifications
for record in records:
    record.message_post(
        subject='Automated Notification',
        body='Your record %s has been processed' % record.name,
        message_type='notification',
        subtype_xmlid='mail.mt_comment',
        partner_ids=[record.partner_id.id],
    )
```

## Scheduled Actions (Cron)

### Basic Cron Jobs

```xml
<!-- data/ir_cron.xml -->
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data noupdate="1">
        <!-- Daily scheduled action -->
        <record id="ir_cron_daily_process" model="ir.cron">
            <field name="name">Daily Process</field>
            <field name="model_id" ref="model_my_model"/>
            <field name="state">code</field>
            <field name="code">model._cron_daily_process()</field>
            <field name="interval_number">1</field>
            <field name="interval_type">days</field>
            <field name="numbercall">-1</field>  <!-- -1 = infinite -->
            <field name="doall">False</field>
            <field name="active">True</field>
            <field name="user_id" ref="base.user_root"/>
            <field name="nextcall" eval="(DateTime.now() + timedelta(days=1)).strftime('%Y-%m-%d 00:00:00')"/>
        </record>

        <!-- Hourly sync -->
        <record id="ir_cron_hourly_sync" model="ir.cron">
            <field name="name">Hourly External Sync</field>
            <field name="model_id" ref="model_my_model"/>
            <field name="state">code</field>
            <field name="code">model._sync_external_data()</field>
            <field name="interval_number">1</field>
            <field name="interval_type">hours</field>
            <field name="numbercall">-1</field>
            <field name="active">True</field>
        </record>

        <!-- Weekly report -->
        <record id="ir_cron_weekly_report" model="ir.cron">
            <field name="name">Send Weekly Report</field>
            <field name="model_id" ref="model_my_model"/>
            <field name="state">code</field>
            <field name="code">model._send_weekly_report()</field>
            <field name="interval_number">1</field>
            <field name="interval_type">weeks</field>
            <field name="day_of_week">0</field>  <!-- Monday = 0 -->
            <field name="active">True</field>
        </record>

        <!-- Monthly cleanup -->
        <record id="ir_cron_monthly_cleanup" model="ir.cron">
            <field name="name">Monthly Cleanup</field>
            <field name="model_id" ref="model_my_model"/>
            <field name="state">code</field>
            <field name="code">model._cleanup_old_records()</field>
            <field name="interval_number">1</field>
            <field name="interval_type">months</field>
            <field name="day_of_month">1</field>
            <field name="active">True</field>
        </record>

        <!-- One-time execution -->
        <record id="ir_cron_one_time" model="ir.cron">
            <field name="name">One Time Migration</field>
            <field name="model_id" ref="model_my_model"/>
            <field name="state">code</field>
            <field name="code">model._migration_one_time()</field>
            <field name="numbercall">1</field>  <!-- Run only once -->
            <field name="active">True</field>
        </record>
    </data>
</odoo>
```

### Cron Methods in Model

```python
class MyModel(models.Model):
    _name = 'my.model'

    @api.model
    def _cron_daily_process(self):
        """Process draft orders that need confirmation"""
        # Find records meeting criteria
        to_process = self.search([
            ('state', '=', 'draft'),
            ('date', '<=', fields.Date.today()),
        ])

        _logger.info('Processing %d records', len(to_process))

        for record in to_process:
            try:
                record.action_confirm()
            except Exception as e:
                _logger.error('Failed to process record %s: %s', record.id, e)

        return True

    @api.model
    def _cleanup_old_records(self):
        """Archive records older than 1 year"""
        from dateutil.relativedelta import relativedelta

        cutoff_date = fields.Date.today() - relativedelta(years=1)
        old_records = self.search([
            ('create_date', '<', cutoff_date),
            ('active', '=', True),
        ])

        old_records.write({'active': False})
        _logger.info('Archived %d old records', len(old_records))

        return True
```

## Automated Action Rules

```xml
<!-- data/automation_data.xml -->
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data noupdate="1">
        <!-- On Create: Send welcome email -->
        <record id="automation_on_create" model="base.automation">
            <field name="name">Send Welcome Email</field>
            <field name="model_id" ref="model_my_model"/>
            <field name="trigger">on_create</field>
            <field name="action_server_id" ref="action_send_welcome_email"/>
            <field name="active">True</field>
        </record>

        <!-- On Write: Update status when amount changes -->
        <record id="automation_on_write" model="base.automation">
            <field name="name">Update Status on Amount Change</field>
            <field name="model_id" ref="model_my_model"/>
            <field name="trigger">on_write</field>
            <field name="filter_pre_domain">
                [('amount_total', '>', 1000)]
            </field>
            <field name="filter_domain">
                [('amount_total', '&lt;=', 1000)]
            </field>
            <field name="action_server_id" ref="action_downgrade_status"/>
            <field name="active">True</field>
        </record>

        <!-- On Unlink: Archive related records -->
        <record id="automation_on_unlink" model="base.automation">
            <field name="name">Archive Related on Delete</field>
            <field name="model_id" ref="model_my_model"/>
            <field name="trigger">on_unlink</field>
            <field name="action_server_id" ref="action_archive_related"/>
            <field name="active">True</field>
        </record>

        <!-- On Time: Process stale drafts -->
        <record id="automation_on_time" model="base.automation">
            <field name="name">Process Stale Drafts</field>
            <field name="model_id" ref="model_my_model"/>
            <field name="trigger">on_time</field>
            <field name="trg_date_id" ref="field_my_model_date"/>
            <field name="trg_date_range">7</field>
            <field name="trg_date_range_type">day</field>
            <field name="filter_domain">
                [('state', '=', 'draft')]
            </field>
            <field name="action_server_id" ref="action_cancel_stale"/>
            <field name="active">True</field>
        </record>

        <!-- On Change: Monitor field updates -->
        <record id="automation_on_change" model="base.automation">
            <field name="name">Alert on Priority Change</field>
            <field name="model_id" ref="model_my_model"/>
            <field name="trigger">on_change</field>
            <field name="on_change_field_ids">
                <field eval="[(6, 0, [ref('field_my_model_priority')])]" name="on_change_field_ids"/>
            </field>
            <field name="filter_pre_domain">
                [('priority', '=', 'normal')]
            </field>
            <field name="filter_domain">
                [('priority', '=', 'urgent')]
            </field>
            <field name="action_server_id" ref="action_send_urgent_alert"/>
            <field name="active">True</field>
        </record>
    </data>
</odoo>
```

## Workflow Automation

### State Transitions with Methods

```python
class MyModel(models.Model):
    _name = 'my.model'

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('approved', 'Approved'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], string='State', default='draft', tracking=True)

    def action_confirm(self):
        """Transition from draft to confirmed"""
        for record in self:
            if record.state != 'draft':
                raise UserError(_('Cannot confirm non-draft record'))
            # Validation
            if not record.line_ids:
                raise UserError(_('Cannot confirm without lines'))
        self.write({'state': 'confirmed'})
        return True

    def action_approve(self):
        """Transition from confirmed to approved"""
        for record in self:
            if record.state != 'confirmed':
                raise UserError(_('Only confirmed records can be approved'))
            # Business logic
            if record.amount_total > 10000:
                record._send_for_high_value_approval()
        self.write({'state': 'approved'})
        return True

    def action_done(self):
        """Transition from approved to done"""
        for record in self:
            if record.state != 'approved':
                raise UserError _('Only approved records can be marked done'))
            # Final processing
            record._process_final()
        self.write({'state': 'done'})
        return True

    def action_cancel(self):
        """Cancel from any state except done"""
        for record in self:
            if record.state == 'done':
                raise UserError(_('Cannot cancel completed records'))
            if record.state != 'draft':
                record._send_cancellation_notice()
        self.write({'state': 'cancel'})
        return True

    def action_back_to_draft(self):
        """Reset to draft"""
        self.write({'state': 'draft'})
        return True
```

### Chained Actions

```python
class SaleOrder(models.Model):
    _name = 'sale.order'

    def action_confirm(self):
        """Confirm order and trigger downstream actions"""
        for order in self:
            # Update state
            order.write({'state': 'sale'})

            # Create procurement
            order._action_launch_procurement_rule()

            # Send confirmation email
            order._send_order_confirmation()

            # Create invoice if configured
            if order.company_id.auto_invoice:
                order._create_invoices()

        return True

    def _send_order_confirmation(self):
        """Send confirmation email to customer"""
        for order in self:
            template = self.env.ref('sale.email_template_edi_sale', raise_if_not_found=False)
            if template:
                template.send_mail(order.id, force_send=True)

        return True
```

## Email Templates

```xml
<!-- data/email_template.xml -->
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data noupdate="1">
        <!-- Simple Email Template -->
        <record id="email_template_my_model" model="mail.template">
            <field name="name">My Model: Send Email</field>
            <field name="model_id" ref="model_my_model"/>
            <field name="subject">Your Record {{ object.name }}</field>
            <field name="email_from">{{ object.company_id.email or 'noreply@example.com' }}</field>
            <field name="email_to">{{ object.partner_id.email }}</field>
            <field name="body_html" type="html">
                <div style="margin: 0px; padding: 0px;">
                    <p>Dear <t t-esc="object.partner_id.name"/>,</p>
                    <p>Your record <strong><t t-esc="object.name"/></strong> has been processed.</p>
                    <p>
                        State: <t t-esc="object.state"/><br/>
                        Date: <t t-esc="object.date"/><br/>
                        Amount: <t t-esc="object.amount_total"/>
                    </p>
                    <p>Thank you for your business!</p>
                </div>
            </field>
            <field name="lang">{{ object.partner_id.lang }}</field>
            <field name="auto_delete">True</field>
            <field name="user_signature" eval="False"/>
        </record>

        <!-- Template with Report Attachment -->
        <record id="email_template_with_report" model="mail.template">
            <field name="name">Send Report</field>
            <field name="model_id" ref="model_my_model"/>
            <field name="subject">Report for {{ object.name }}</field>
            <field name="email_to">{{ object.partner_id.email }}</field>
            <field name="body_html" type="html">
                <p>Please find attached the report.</p>
            </field>
            <field name="report_template" ref="report_my_model"/>
            <field name="report_name">{{ object.name }}</field>
        </record>

        <!-- Multi-language Template -->
        <record id="email_template_multilang" model="mail.template">
            <field name="name">Multi-language Email</field>
            <field name="model_id" ref="model_my_model"/>
            <field name="subject">${object.subject or 'Notification'}</field>
            <field name="body_html" type="html">
                <div>
                    <p>${object.greeting_text or 'Hello'}</p>
                    <p>${object.message}</p>
                </div>
            </field>
            <field name="lang">${object.partner_id.lang}</field>
        </record>
    </data>
</odoo>
```

## Activity Rules

```xml
<!-- data/mail_activity_data.xml -->
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data noupdate="1">
        <!-- Schedule activity when record is created -->
        <record id="activity_on_create" model="mail.activity.type">
            <field name="name">Review New Record</field>
            <field name="sequence">10</field>
            <field name="icon">fa-check</field>
            <field name="delay_count">1</field>
            <field name="delay_unit">days</field>
            <field name="delay_from">current_date</field>
            <field name="summary">Review and approve this record</field>
            <field name="res_model">my.model</field>
            <field name="default_user_id" ref="base.user_admin"/>
        </record>

        <!-- Automatic activity scheduling -->
        <record id="automation_schedule_activity" model="base.automation">
            <field name="name">Schedule Review Activity</field>
            <field name="model_id" ref="model_my_model"/>
            <field name="trigger">on_create</field>
            <field name="last_run" eval="False"/>
            <field name="activity_type_id" ref="mail.mail_activity_data_todo"/>
            <field name="activity_summary">Please review</field>
            <field name="activity_note">Review this record and approve if correct</field>
            <field name="activity_user_type">specific</field>
            <field name="activity_user_id" ref="base.user_admin"/>
            <field name="activity_date_deadline_range">3</field>
            <field name="activity_date_deadline_range_type">days</field>
        </record>
    </data>
</odoo>
```

## References

- Automation: https://www.odoo.com/documentation/18.0/developer/reference/backend/automation.html
- Server actions: https://www.odoo.com/documentation/18.0/developer/reference/backend/actions.html
- Cron: https://www.odoo.com/documentation/18.0/developer/reference/backend/cron.html
