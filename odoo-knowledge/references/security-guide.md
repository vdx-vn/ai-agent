# Security Guide Reference

## Access Rights (ACL)

### ir.model.access.csv
```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_sale_order_user,sale.order.user,model_sale_order,base.group_user,1,0,0,0
access_sale_order_manager,sale.order.manager,model_sale_order,sales_team.group_sale_manager,1,1,1,1
access_sale_order_all,sale.order.all,model_sale_order,base.group_public,1,0,0,0
```

### XML Format
```xml
<odoo>
    <data noupdate="0">
        <!-- Full access for managers -->
        <record id="sale_order_manager_access" model="ir.model.access">
            <field name="name">sale.order.manager</field>
            <field name="model_id" ref="model_sale_order"/>
            <field name="group_id" ref="sales_team.group_sale_manager"/>
            <field name="perm_read" eval="True"/>
            <field name="perm_write" eval="True"/>
            <field name="perm_create" eval="True"/>
            <field name="perm_unlink" eval="True"/>
        </record>

        <!-- Read only for users -->
        <record id="sale_order_user_access" model="ir.model.access">
            <field name="name">sale.order.user</field>
            <field name="model_id" ref="model_sale_order"/>
            <field name="group_id" ref="base.group_user"/>
            <field name="perm_read" eval="True"/>
            <field name="perm_write" eval="False"/>
            <field name="perm_create" eval="False"/>
            <field name="perm_unlink" eval="False"/>
        </record>
    </data>
</odoo>
```

## Record Rules

### Basic Record Rule
```xml
<!-- Users can only see their own orders -->
<record id="sale_order_personal_rule" model="ir.rule">
    <field name="name">Personal Orders</field>
    <field name="model_id" ref="model_sale_order"/>
    <field name="domain_force">[('user_id', '=', user.id)]</field>
    <field name="groups" eval="[(4, ref('base.group_user'))]"/>
    <field name="perm_read" eval="True"/>
    <field name="perm_write" eval="True"/>
    <field name="perm_create" eval="True"/>
    <field name="perm_unlink" eval="True"/>
</record>
```

### Multi-Company Rule
```xml
<!-- Users can only see records of their company -->
<record id="sale_order_company_rule" model="ir.rule">
    <field name="name">Sale Order Company Rule</field>
    <field name="model_id" ref="model_sale_order"/>
    <field name="domain_force">['|', ('company_id', '=', False), ('company_id', 'in', company_ids)]</field>
    <field name="global" eval="True"/>
</record>
```

### Manager Override Rule
```xml
<!-- Managers can see all orders -->
<record id="sale_order_manager_rule" model="ir.rule">
    <field name="name">Sale Order Manager Rule</field>
    <field name="model_id" ref="model_sale_order"/>
    <field name="domain_force">[(1, '=', 1)]</field>
    <field name="groups" eval="[(4, ref('sales_team.group_sale_manager'))]"/>
    <field name="perm_read" eval="True"/>
    <field name="perm_write" eval="True"/>
    <field name="perm_create" eval="True"/>
    <field name="perm_unlink" eval="True"/>
</record>
```

### Complex Domain Rule
```xml
<!-- Sales can see their team's orders -->
<record id="sale_order_team_rule" model="ir.rule">
    <field name="name">Sale Order Team Rule</field>
    <field name="model_id" ref="model_sale_order"/>
    <field name="domain_force">
        ['|',
            ('user_id', '=', user.id),
            ('team_id.member_ids', 'in', user.id)]
    </field>
    <field name="groups" eval="[(4, ref('sales_team.group_sale_salesman'))]"/>
</record>
```

## Groups

### Create Custom Groups
```xml
<!-- Category -->
<record id="module_category_myapp" model="ir.module.category">
    <field name="name">My Application</field>
    <field name="description">Manage my application</field>
    <field name="sequence">20</field>
</record>

<!-- Group -->
<record id="group_myapp_user" model="res.groups">
    <field name="name">User</field>
    <field name="comment">Standard user for my application</field>
    <field name="category_id" ref="module_category_myapp"/>
    <field name="implied_ids" eval="[(4, ref('base.group_user'))]"/>
</record>

<record id="group_myapp_manager" model="res.groups">
    <field name="name">Manager</field>
    <field name="comment">Manager for my application</field>
    <field name="category_id" ref="module_category_myapp"/>
    <field name="implied_ids" eval="[(4, ref('group_myapp_user'))]"/>
    <field name="users" eval="[(4, ref('base.user_admin'))]"/>
</record>
```

## Model-Level Security

### Field-Level Access
```python
class SaleOrder(models.Model):
    _name = 'sale.order'

    # Public fields
    name = fields.Char()

    # Read-only field (cannot be written)
    create_date = fields.Datetime(readonly=True)

    # Sensitive field - only manager can write
    margin = fields.Float(groups='sales_team.group_sale_manager')

    # Computed field with access control
    @api.depends('order_line.price_subtotal')
    def _compute_amount_total(self):
        for order in self:
            order.amount_total = sum(line.price_subtotal for line in order.line_line)
```

### Sudo() - Superuser Mode
```python
class SaleOrder(models.Model):
    def action_confirm(self):
        # Bypass access rights for specific operations
        for order in self:
            # Write to partner which user may not have access to
            order.partner_id.sudo().write({
                'last_order_date': fields.Date.today()
            })

            # Create record in restricted model
            self.env['mail.message'].sudo().create({
                'res_id': order.id,
                'model': 'sale.order',
                'body': 'Order confirmed'
            })
        return True
```

**Warning**: Only use `sudo()` when absolutely necessary. Prefer proper access rights.

## Security Best Practices

### 1. Principle of Least Privilege
```xml
<!-- Bad: Everyone can delete -->
<record id="delete_all" model="ir.model.access">
    <field name="perm_unlink" eval="True"/>
</record>

<!-- Good: Only managers can delete -->
<record id="delete_managers_only" model="ir.model.access">
    <field name="perm_unlink" eval="False"/>
</record>
<record id="delete_managers" model="ir.model.access">
    <field name="name">model.manager</field>
    <field name="group_id" ref="group_manager"/>
    <field name="perm_unlink" eval="True"/>
</record>
```

### 2. Always Validate in Python
```python
def action_done(self):
    for order in self:
        # Check state transition
        if order.state != 'confirmed':
            raise UserError(_('Only confirmed orders can be done'))

        # Check access rights
        if not self.env.user.has_group('sales_team.group_sale_manager'):
            if order.user_id != self.env.user:
                raise UserError(_('You can only process your own orders'))

    self.write({'state': 'done'})
```

### 3. Use ORM Methods, Not SQL
```python
# Bad: Direct SQL bypasses security
self.env.cr.execute("UPDATE sale_order SET state='done' WHERE id=%s", (self.id,))

# Good: ORM respects record rules
self.write({'state': 'done'})
```

### 4. Safe Search in Loops
```python
# Bad: N+1 query problem
for partner in partners:
    orders = self.env['sale.order'].search([('partner_id', '=', partner.id)])

# Good: Search once, group by
all_orders = self.env['sale.order'].search([('partner_id', 'in', partners.ids)])
for partner in partners:
    partner_orders = all_orders.filtered(lambda o: o.partner_id == partner)
```

## References
- Security: https://www.odoo.com/documentation/18.0/developer/reference/backend/security.html
- Access rights: https://github.com/odoo/odoo/blob/18.0/addons/base/security/ir.model.access.csv
- Record rules: https://github.com/odoo/odoo/blob/18.0/addons/base/security/base_security.xml
