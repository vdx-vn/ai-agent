# ORM Patterns Reference

## Field Types

### Basic Fields
```python
from odoo import models, fields

class MyModel(models.Model):
    _name = 'my.model'
    _description = 'My Model'

    # String
    name = fields.Char(string="Name", required=True)
    description = fields.Text()

    # Numeric
    quantity = fields.Integer()
    price = fields.Float(digits='Product Price')
    weight = fields.Float(digits='Stock Weight')

    # Date/Time
    date_order = fields.Date()
    datetime_order = fields.Datetime()

    # Boolean
    active = fields.Boolean(default=True)

    # Selection
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
    ], string='State', default='draft')
```

### Relational Fields
```python
class OrderLine(models.Model):
    _name = 'order.line'

    # Many2one (foreign key)
    order_id = fields.Many2one('sale.order', string='Order', required=True)
    product_id = fields.Many2one('product.product', string='Product')

    # One2many (inverse of Many2one)
    line_ids = fields.One2many('order.line', 'order_id', string='Lines')

    # Many2many
    tag_ids = fields.Many2many('product.tag', string='Tags')

    # Related fields
    partner_name = fields.Char(related='partner_id.name', readonly=True)
```

### Computed Fields
```python
class SaleOrder(models.Model):
    _name = 'sale.order'

    amount_total = fields.Monetary(
        compute='_compute_amount_total',
        store=True,
        currency_field='currency_id'
    )

    @api.depends('line_ids.price_subtotal', 'currency_id')
    def _compute_amount_total(self):
        for order in self:
            order.amount_total = sum(line.price_subtotal for line in order.line_ids)
```

### Inverse Computed Fields
```python
class Product(models.Model):
    _name = 'product.product'

    weight = fields.Float('Weight')
    total_weight = fields.Float(
        compute='_compute_total',
        inverse='_inverse_total'
    )

    @api.depends('weight')
    def _compute_total(self):
        for rec in self:
            rec.total_weight = rec.weight * 2.205  # lb

    def _inverse_total(self):
        for rec in self:
            rec.weight = rec.total_weight / 2.205
```

## Model Methods

### CRUD Override Pattern
```python
class MyModel(models.Model):
    _name = 'my.model'

    @api.model
    def create(self, vals):
        # Add default values
        if 'code' not in vals:
            vals['code'] = self.env['ir.sequence'].next_by_code('my.model')
        # Call super
        record = super().create(vals)
        # Post-create logic
        record._compute_related()
        return record

    def write(self, vals):
        # Pre-write logic
        for record in self:
            if 'state' in vals and vals['state'] == 'done':
                record._validate_before_done()
        # Call super
        result = super().write(vals)
        # Post-write logic
        self._compute_dependencies()
        return result

    def unlink(self):
        # Validation before delete
        for record in self:
            if record.state == 'done':
                raise UserError(_('Cannot delete confirmed records'))
        return super().unlink()
```

### Search Methods
```python
class Product(models.Model):
    _name = 'product.product'

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('name', operator, name), ('default_code', operator, name)]
        products = self.search(domain + args, limit=limit)
        return products.name_get()

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        # Custom search with optimization
        return super().search_read(
            domain=domain,
            fields=fields,
            offset=offset,
            limit=limit,
            order=order
        )
```

## Common ORM Patterns

### Filter and Search
```python
# Simple search
records = self.env['sale.order'].search([('state', '=', 'draft')])

# Complex domain
domain = [
    '&',
    ('state', 'in', ['draft', 'sent']),
    '|',
    ('date_order', '>=', fields.Date.today()),
    ('partner_id.country_id.code', '=', 'US')
]
records = self.env['sale.order'].search(domain)

# Search with limit and order
records = self.env['sale.order'].search(
    domain,
    limit=10,
    order='date_order desc'
)

# Search one (returns first match or empty recordset)
record = self.env['sale.order'].search([('code', '=', 'SO001')], limit=1)

# Browse by IDs
records = self.env['sale.order'].browse([1, 2, 3])
```

### Recordset Operations
```python
# Iterate
for order in orders:
    print(order.name)

# Filtered
high_value = orders.filtered(lambda o: o.amount_total > 1000)

# Mapped
partners = orders.mapped('partner_id')
names = orders.mapped('name')

# Sorted
sorted_orders = orders.sorted(key=lambda o: o.amount_total, reverse=True)

# Concatenation
all_orders = draft_orders | confirmed_orders
```

### Parent/Child Relationship
```python
class Category(models.Model):
    _name = 'product.category'

    name = fields.Char(required=True)
    parent_id = fields.Many2one('product.category', string='Parent Category')
    child_ids = fields.One2many('product.category', 'parent_id')
    parent_path = fields.Char(index=True)

    @api.depends('name', 'parent_id')
    def name_get(self):
        result = []
        for category in self:
            if category.parent_id:
                name = f"{category.parent_id.name} / {category.name}"
            else:
                name = category.name
            result.append((category.id, name))
        return result
```

## References
- ORM: https://www.odoo.com/documentation/18.0/developer/reference/backend/orm.html
- Fields: https://github.com/odoo/odoo/blob/18.0/odoo/fields.py
- Models: https://github.com/odoo/odoo/blob/18.0/odoo/models.py
