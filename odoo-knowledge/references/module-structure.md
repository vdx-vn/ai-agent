# Module Structure Reference

## Standard Module Structure

```
my_module/
├── __init__.py                 # Module initialization, imports models
├── __manifest__.py             # Module metadata and configuration
│
├── models/                     # Python models (ORM)
│   ├── __init__.py
│   ├── my_model.py
│   └── my_model_line.py
│
├── views/                      # XML view definitions
│   ├── my_model_views.xml
│   ├── my_model_templates.xml
│   └── assets.xml
│
├── security/                   # Access control
│   ├── ir.model.access.csv     # ACL (access rights)
│   └── my_model_security.xml   # Record rules
│
├── data/                       # Data files loaded on install
│   ├── my_model_data.xml
│   └── ir.cron.xml
│
├── demo/                       # Demo data (only in demo mode)
│   └── my_model_demo.xml
│
├── static/                     # Web assets
│   ├── src/
│   │   ├── js/                # JavaScript files
│   │   │   └── my_widget.js
│   │   ├── xml/               # QWeb templates
│   │   │   └── my_templates.xml
│   │   └── css/               # Stylesheets
│   │       └── my_style.css
│   └── description/            # Module images
│       └── icon.png
│
├── report/                     # Reports (QWeb)
│   ├── my_report.xml
│   └── my_report_templates.xml
│
├── controllers/                # HTTP controllers
│   ├── __init__.py
│   └── my_controller.py
│
├── lib/                        # External libraries
│   └── my_lib.py
│
├── tests/                      # Test cases
│   ├── __init__.py
│   ├── test_my_model.py
│   └── test_ui.py
│
└── i18n/                       # Translation files
    ├── my_module.pot
    ├── fr.po
    └── vi.po
```

## __manifest__.py Structure

```python
# -*- coding: utf-8 -*-
{
    'name': 'My Custom Module',
    'version': '18.0.1.0.0',
    'category': 'Tools',
    'summary': 'Brief description of what the module does',
    'description': """
Longer description of the module.
Can span multiple lines.
    """,

    # Author information
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'license': 'LGPL-3',

    # Any external dependencies (Python packages)
    'external_dependencies': {
        'python': ['requests', 'openpyxl'],
        'bin': ['zip', 'unzip'],
    },

    # Odoo modules that must be installed first
    'depends': [
        'base',
        'sale_management',
        'stock',
    ],

    # Data files to load (in order)
    'data': [
        # Security first
        'security/my_module_security.xml',
        'security/ir.model.access.csv',

        # Views
        'views/my_model_views.xml',
        'views/assets.xml',

        # Data
        'data/ir_cron.xml',
        'data/mail_message_subtype.xml',

        # Reports
        'report/my_report.xml',
    ],

    # Demo data (only in demo mode)
    'demo': [
        'demo/my_module_demo.xml',
    ],

    # Assets (CSS/JS bundles)
    'assets': {
        'web.assets_frontend': [
            'my_module/static/src/css/my_style.css',
            'my_module/static/src/js/my_widget.js',
        ],
        'web.assets_backend': [
            'my_module/static/src/js/backend.js',
        ],
    },

    # QWeb templates
    'qweb': [
        ('static/src/xml/my_templates.xml', None),
    ],

    # Images for app store
    'images': [
        'static/description/banner.png',
        'static/description/icon.png',
    ],

    # Installation flags
    'application': True,          # Show as app, not just module
    'installable': True,
    'auto_install': False,        # Auto-install if deps are met
    'post_init_hook': 'post_init_hook',

    # Version compatibility
    'development_status': 'Beta',
    'maintainers': ['YourName'],
}
```

## __init__.py Files

### Root __init__.py
```python
# -*- coding: utf-8 -*-

from . import models
from . import controllers

def post_init_hook(env):
    """Called after module installation"""
    # Create default records
    # Run migrations
    pass
```

### models/__init__.py
```python
# -*- coding: utf-8 -*-

from . import my_model
from . import my_model_line
```

## Model File Structure

```python
# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class MyModel(models.Model):
    """Documentation string describing the model."""
    _name = 'my.model'               # Model identifier
    _description = 'My Model'        # Human readable name
    _inherit = ['mail.thread', 'mail.activity.mixin']  # Mixins
    _order = 'date desc, name'       # Default sort order

    # ======================================
    # Fields
    # ======================================

    name = fields.Char(
        string='Name',
        required=True,
        tracking=True,                # Track changes in chatter
        translate=True,
        copy=False
    )

    code = fields.Char(
        string='Code',
        readonly=True,
        copy=False,
        default=lambda self: _('New')
    )

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], string='State', default='draft', tracking=True)

    date = fields.Date(
        string='Date',
        default=fields.Date.context_today,
        tracking=True
    )

    # Relations
    partner_id = fields.Many2one(
        'res.partner',
        string='Customer',
        required=True,
        tracking=True
    )

    line_ids = fields.One2many(
        'my.model.line',
        'model_id',
        string='Lines'
    )

    # Computed
    amount_total = fields.Float(
        compute='_compute_amounts',
        store=True
    )

    # ======================================
    # Constraints and Onchange
    # ======================================

    @api.constrains('date')
    def _check_date(self):
        for record in self:
            if record.date and record.date > fields.Date.today():
                raise ValidationError(_('Date cannot be in the future'))

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        if self.partner_id:
            self.currency_id = self.partner_id.currency_id

    # ======================================
    # CRUD Methods
    # ======================================

    @api.model
    def create(self, vals):
        if vals.get('code', _('New')) == _('New'):
            vals['code'] = self.env['ir.sequence'].next_by_code('my.model') or _('New')
        return super().create(vals)

    def write(self, vals):
        result = super().write(vals)
        # Post-write logic
        return result

    def unlink(self):
        for record in self:
            if record.state != 'cancel':
                raise UserError(_('Cannot delete non-cancelled records'))
        return super().unlink()

    # ======================================
    # Business Methods
    # ======================================

    def action_confirm(self):
        """Transition from draft to confirmed"""
        for record in self:
            if record.state != 'draft':
                raise UserError(_('Cannot confirm non-draft record'))
        self.write({'state': 'confirmed'})
        return True

    def _compute_amounts(self):
        for record in self:
            record.amount_total = sum(line.amount for line in record.line_ids)


class MyModelLine(models.Model):
    """Documentation string."""
    _name = 'my.model.line'
    _description = 'My Model Line'

    model_id = fields.Many2one('my.model', required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Product')
    quantity = fields.Float('Quantity', default=1.0)
    price_unit = fields.Float('Unit Price')
    amount = fields.Float(compute='_compute_amount', store=True)

    @api.depends('quantity', 'price_unit')
    def _compute_amount(self):
        for line in self:
            line.amount = line.quantity * line.price_unit
```

## Security Files

### ir.model.access.csv
```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_my_model_user,my.model.user,model_my_model,base.group_user,1,0,0,0
access_my_model_manager,my.model.manager,model_my_model,base.group_system,1,1,1,1
access_my_model_line_user,my.model.line.user,model_my_model_line,base.group_user,1,1,1,0
```

### my_model_security.xml
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data noupdate="0">
        <!-- Record Rule: Users see own records -->
        <record id="my_model_personal_rule" model="ir.rule">
            <field name="name">My Model: Personal</field>
            <field name="model_id" ref="model_my_model"/>
            <field name="domain_force">[('create_uid', '=', user.id)]</field>
            <field name="groups" eval="[(4, ref('base.group_user'))]"/>
        </record>

        <!-- Record Rule: Managers see all -->
        <record id="my_model_manager_rule" model="ir.rule">
            <field name="name">My Model: Manager</field>
            <field name="model_id" ref="model_my_model"/>
            <field name="domain_force">[(1, '=', 1)]</field>
            <field name="groups" eval="[(4, ref('base.group_system'))]"/>
        </record>
    </data>
</odoo>
```

## View File Structure

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data>
        <!-- Tree View -->
        <record id="view_my_model_tree" model="ir.ui.view">
            <field name="name">my.model.tree</field>
            <field name="model">my.model</field>
            <field name="arch" type="xml">
                <tree>
                    <field name="name"/>
                    <field name="code"/>
                    <field name="date"/>
                    <field name="state" widget="badge"/>
                </tree>
            </field>
        </record>

        <!-- Form View -->
        <record id="view_my_model_form" model="ir.ui.view">
            <field name="name">my.model.form</field>
            <field name="model">my.model</field>
            <field name="arch" type="xml">
                <form string="My Model">
                    <header>
                        <button name="action_confirm" string="Confirm" type="object"/>
                        <field name="state" widget="statusbar"/>
                    </header>
                    <sheet>
                        <group>
                            <field name="name"/>
                            <field name="code"/>
                            <field name="date"/>
                        </group>
                    </sheet>
                    <div class="oe_chatter">
                        <field name="message_follower_ids"/>
                        <field name="activity_ids"/>
                        <field name="message_ids"/>
                    </div>
                </form>
            </field>
        </record>

        <!-- Search View -->
        <record id="view_my_model_search" model="ir.ui.view">
            <field name="name">my.model.search</field>
            <field name="model">my.model</field>
            <field name="arch" type="xml">
                <search string="My Model">
                    <field name="name"/>
                    <filter name="draft" string="Draft" domain="[('state', '=', 'draft')]"/>
                    <separator/>
                    <group expand="0" string="Group By">
                        <filter name="state" string="State" context="{'group_by': 'state'}"/>
                    </group>
                </search>
            </field>
        </record>

        <!-- Action -->
        <record id="action_my_model" model="ir.actions.act_window">
            <field name="name">My Model</field>
            <field name="res_model">my.model</field>
            <field name="view_mode">tree,form</field>
        </record>

        <!-- Menu -->
        <menuitem id="menu_my_model_root" name="My Module" sequence="10"/>
        <menuitem id="menu_my_model" name="My Model"
                  parent="menu_my_model_root" action="action_my_model"/>
    </data>
</odoo>
```

## Best Practices

1. **File Organization**
   - One model per file (unless models are closely related)
   - Group related views in same file
   - Keep views for each model separate

2. **Naming Conventions**
   - Model: `my.model` (lowercase with dots)
   - Class: `MyModel` (CamelCase)
   - Fields: `snake_case`
   - Many2one: `<related>_id`
   - One2many: `<related>_ids`

3. **Load Order**
   - Security first (access.csv, security.xml)
   - Then data (sequence, mail templates)
   - Then views
   - Reports last

4. **Translation**
   - Always wrap user-facing strings in `_(...)`
   - Import `_` from `odoo`

## References
- Module structure: https://www.odoo.com/documentation/18.0/developer/reference/backend/module.html
- Base module: https://github.com/odoo/odoo/tree/18.0/addons/base
