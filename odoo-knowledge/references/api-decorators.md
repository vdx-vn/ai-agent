# API Decorators Reference

## Overview

Odoo uses the `odoo.api` module to decorate methods with specific behaviors regarding environments, recordsets, and computation dependencies.

## Common Decorators

### @api.model - Model-Level Methods

For methods that don't depend on specific records:

```python
class SaleOrder(models.Model):
    _name = 'sale.order'

    @api.model
    def create_quotation(self, partner_id, lines):
        """Create a new quotation - no recordset needed"""
        return self.create({
            'partner_id': partner_id,
            'order_line': lines,
            'state': 'draft',
        })

    @api.model
    def get_default_currency(self):
        """Get default company currency - no self context"""
        return self.env.company.currency_id
```

### @api.depends - Computed Fields

Declare dependencies for computed fields:

```python
class SaleOrderLine(models.Model):
    _name = 'sale.order.line'

    price_subtotal = fields.Float(compute='_compute_amount', store=True)

    @api.depends('price_unit', 'tax_id', 'discount', 'product_uom_qty', 'product_id')
    def _compute_amount(self):
        """Compute subtotal based on several fields"""
        for line in self:
            taxes = line.tax_id.compute_all(
                line.price_unit,
                line.order_id.currency_id,
                line.product_uom_qty,
                product=line.product_id,
                partner=line.order_id.partner_id
            )
            line.price_subtotal = taxes['total_excluded']
```

**With related fields (dot notation)**:
```python
@api.depends('order_id.partner_id', 'order_id.currency_id')
def _compute_partner_info(self):
    for line in self:
        line.partner_name = line.order_id.partner_id.name
        line.currency = line.order_id.currency_id
```

### @api.onchange - Onchange Methods

Trigger when field changes in form:

```python
class SaleOrderLine(models.Model):
    _name = 'sale.order.line'

    @api.onchange('product_id')
    def _onchange_product_id(self):
        """Update fields when product changes"""
        if self.product_id:
            self.name = self.product_id.description_sale
            self.price_unit = self.product_id.lst_price
            self.product_uom_id = self.product_id.uom_id.id
        else:
            self.name = False
            self.price_unit = 0.0
            self.product_uom_id = False

    @api.onchange('product_uom_qty', 'product_id', 'price_unit')
    def _onchange_amount(self):
        """Give warning about discount"""
        if self.product_id and self.discount > 50:
            return {
                'warning': {
                    'title': 'High Discount',
                    'message': 'Discount is greater than 50%'
                }
            }
```

### @api.constrains - Constraints

Validation that runs on create/write:

```python
class SaleOrder(models.Model):
    _name = 'sale.order'

    @api.constrains('date_order', 'validity_date')
    def _check_validity_date(self):
        """Ensure validity date is after order date"""
        for order in self:
            if order.validity_date and order.validity_date < order.date_order:
                raise ValidationError(_(
                    "Validity date (%s) must be after order date (%s)"
                ) % (order.validity_date, order.date_order))

    @api.constrains('order_line')
    def _check_lines(self):
        for order in self:
            if not order.order_line:
                raise ValidationError(_("An order must have at least one line."))
```

### @api.ondelete - Delete Validation

Validate before unlink (Odoo 15+):

```python
class SaleOrder(models.Model):
    _name = 'sale.order'

    @api.ondelete(at_install=False)
    def _unlink_except_confirmed(self):
        """Prevent deletion of confirmed orders"""
        if any(order.state in ('sale', 'done') for order in self):
            raise UserError(_(
                'You cannot delete a confirmed or done sales order.'
            ))
```

## CRUD Decorators

### @api.create - During Create Only

```python
@api.model
@api.create
def _compute_default_values(self):
    """Called only during create"""
    return {
        'state': 'draft',
        'date_order': fields.Datetime.now(),
    }
```

### @api.returns - Specify Return Type

```python
@api.returns('mail.message', lambda value: value.id)
def message_post(self, **kwargs):
    """Post a message, returns message record"""
    # ... implementation
    return super().message_post(**kwargs)
```

## Context and Environment Decorators

### @api.depends_context - Context Dependencies

For computed fields depending on context:

```python
class Product(models.Model):
    _name = 'product.product'

    price = fields.Float(compute='_compute_price')

    @api.depends_context('lang', 'company_id')
    def _compute_price(self):
        for product in self:
            # Different price per language/company
            lang = self.env.context.get('lang')
            company = self.env.context.get('company_id')
            product.price = self._get_price(product, lang, company)
```

### @api.model_create_multi - Bulk Create

Optimize for creating multiple records:

```python
@api.model_create_multi
def create(self, vals_list):
    """Create multiple records efficiently"""
    # Add default values to all records
    for vals in vals_list:
        vals.setdefault('state', 'draft')
        vals.setdefault('date_order', fields.Datetime.now())

    # Call super with all vals at once
    orders = super().create(vals_list)

    # Post-create processing (bulk)
    orders._compute_fiscal_position()

    return orders
```

## Autovacuum Decorators

### @api.autovacuum - Scheduled Cleanup

For cleanup methods called by cron:

```python
class MailMessage(models.Model):
    _name = 'mail.message'

    @api.autovacuum
    def _vacuum_clean_messages(self, *args, **kwargs):
        """Clean old messages - called by autovacuum cron"""
        # Delete messages older than 3 months
        deadline = fields.Datetime.now() - relativedelta(months=3)
        old_messages = self.search([('date', '<', deadline)])
        old_messages.unlink()
```

## Method Type Decorators

### Multi vs Single Record Handling

```python
# Old-style: Handle both single and multi
def old_method(self):
    if isinstance(self.ids, (int, str)):  # single ID
        self = self.browse([self.ids])

# New-style: Always iterate (recordset may have 0, 1, or many records)
def new_method(self):
    for record in self:
        # Process each record
        record.do_something()

# Return result based on recordset size
def compute_something(self):
    result = {}
    for record in self:
        result[record.id] = record.value * 2
    return result
```

## Decorator Combinations

### Computed + Stored + Depends
```python
amount_total = fields.Float(
    compute='_compute_amount',
    store=True,
    compute_sudo=False  # Run with user's rights, not sudo
)

@api.depends('order_line.price_subtotal', 'currency_id')
def _compute_amount(self):
    for order in self:
        order.amount_total = sum(line.price_subtotal for line in order.order_line)
```

### Constrains + Onchange Together
```python
# Validation happens on change and save
min_date = fields.Date('Minimum Date')

@api.onchange('min_date')
@api.constrains('min_date')
def _check_min_date(self):
    if self.min_date and self.min_date < fields.Date.today():
        warning = _('Date cannot be in the past')
        if self.env.context.get('onchange'):
            # From onchange - return warning
            return {'warning': {'title': 'Invalid Date', 'message': warning}}
        # From constrains - raise error
        raise ValidationError(warning)
```

## References
- API: https://www.odoo.com/documentation/18.0/developer/reference/backend/api.html
- Decorators source: https://github.com/odoo/odoo/blob/18.0/odoo/api.py
