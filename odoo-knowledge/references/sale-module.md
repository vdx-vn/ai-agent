# Sale Module Reference

## Sale Order Model

### Core Sale Order Structure

```python
from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # Key fields
    name = fields.Char(string='Order Reference', required=True, copy=False,
                       readonly=True, index=True, default=lambda self: _('New'))

    partner_id = fields.Many2one('res.partner', string='Customer', readonly=True,
                                 states={'draft': [('readonly', False)]},
                                 required=True, change_default=True, index=True, tracking=1)

    date_order = fields.Datetime(string='Order Date', required=True, readonly=True,
                                 index=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
                                 copy=False, default=fields.Datetime.now)

    state = fields.Selection([
        ('draft', 'Quotation'),
        ('sent', 'Quotation Sent'),
        ('sale', 'Sales Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
    ], string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft')

    order_line = fields.One2many('sale.order.line', 'order_id', string='Order Lines',
                                 states={'cancel': [('readonly', True)], 'done': [('readonly', True)]},
                                 copy=True)

    amount_total = fields.Monetary(string='Total', store=True, readonly=True, compute='_amount_all',
                                   tracking=5)

    pricelist_id = fields.Many2one('product.pricelist', string='Pricelist', required=True,
                                  readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
                                  help="Pricelist for current sales order.")

    currency_id = fields.Many2one("res.currency", related="pricelist_id.currency_id",
                                  string="Currency", readonly=True)

    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company)

    user_id = fields.Many2one('res.users', string='Salesperson', index=True,
                             default=lambda self: self.env.user)

    team_id = fields.Many2one('crm.team', string='Sales Team', change_default=True,
                             default=lambda self: self.env['crm.team']._get_default_team_id())
```

### Sale Order Line Structure

```python
class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    order_id = fields.Many2one('sale.order', string='Order Reference', required=True,
                              ondelete='cascade', index=True, copy=False)

    product_id = fields.Many2one('product.product', string='Product',
                                domain=[('sale_ok', '=', True)],
                                change_default=True, ondelete='restrict')

    product_template_id = fields.Many2one('product.template',
                                         string='Product Template',
                                         related='product_id.product_tmpl_id',
                                         domain=[('sale_ok', '=', True)])

    name = fields.Text(string='Description', required=True)

    product_uom_qty = fields.Float(string='Quantity', digits='Product Unit of Measure',
                                  default=1.0, required=True)

    qty_delivered = fields.Float(string='Delivered', copy=False,
                                digits='Product Unit of Measure',
                                compute='_compute_qty_delivered', store=True)

    qty_to_invoice = fields.Float(string='To Invoice', copy=False,
                                 compute='_compute_qty_to_invoice', store=True)

    qty_invoiced = fields.Float(string='Invoiced', copy=False,
                               digits='Product Unit of Measure',
                               compute='_compute_qty_invoiced', store=True)

    price_unit = fields.Float('Unit Price', required=True, digits='Product Price',
                             default=0.0)

    price_subtotal = fields.Monetary(string='Subtotal', readonly=True, store=True)
    price_tax = fields.Float(string='Total Tax', readonly=True, store=True)
    price_total = fields.Monetary(string='Total', readonly=True, store=True)

    tax_id = fields.Many2many('account.tax', string='Taxes',
                              domain=['|', ('company_id', '=', False),
                                     ('company_id', '=', company_id)])

    discount = fields.Float(string='Discount (%)', digits='Discount',
                           default=0.0)

    state = fields.Selection([
        ('draft', 'Quotation'),
        ('sale', 'Sales Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
    ], related='order_id.state', string='Order Status', readonly=True, copy=False)

    invoice_status = fields.Selection([
        ('upselling', 'Upselling Opportunity'),
        ('invoiced', 'Fully Invoiced'),
        ('to invoice', 'To Invoice'),
        ('no', 'Nothing to Invoice'),
    ], string='Invoice Status', compute='_compute_invoice_status', store=True, readonly=True, default='no')
```

## Common Sale Order Methods

### Confirm Sale Order

```python
def action_confirm(self):
    """Confirm the sale order and create procurement"""
    for order in self:
        # Validate
        if order.state != 'draft' and order.state != 'sent':
            continue
        order._action_confirm()

    return True

def _action_confirm(self):
    """Internal confirmation logic"""
    for order in self:
        # Set to sale state
        order.state = 'sale'

        # Check if order needs to be invoiced
        if not order.order_line:
            raise UserError(_('Cannot confirm empty sales order.'))

        # Create procurement for products
        order.order_line._action_launch_stock_rule()

        # Send confirmation email
        if not order.partner_id.opt_out:
            order._send_order_confirmation_mail()

    return True
```

### Create Invoice

```python
def _create_invoices(self, grouped=False, final=False, date=None):
    """Create invoices from sale order"""
    moves = self.env['account.move']

    for order in self:
        if order.state != 'sale':
            continue

        # Create invoice via wizard logic
        moves |= order._create_invoice(
            grouped=grouped, final=final, date=date
        )

    return moves

def _create_invoice(self, grouped=False, final=False, date=None):
    """Internal invoice creation"""
    return self.env['account.move'].create({
        'move_type': 'out_invoice',
        'partner_id': self.partner_id.id,
        'invoice_date': date or fields.Date.today(),
        'currency_id': self.currency_id.id,
        'invoice_origin': self.name,
        'invoice_line_ids': [(0, 0, line._prepare_invoice_line()) for line in self.order_line],
    })
```

### Cancel Sale Order

```python
def action_cancel(self):
    """Cancel the sales order"""
    return self.write({'state': 'cancel'})

def _action_cancel(self):
    """Internal cancel with cleanup"""
    for order in self:
        # Cancel existing invoices
        order.invoice_ids.button_cancel()

        # Cancel stock moves
        order.picking_ids.action_cancel()

    return True
```

## Picking and Delivery

### Create Picking from Sale Order

```python
def _prepare_picking(self):
    """Prepare values for stock picking"""
    return {
        'picking_type_id': self.warehouse_id.out_type_id.id,
        'partner_id': self.partner_id.id,
        'origin': self.name,
        'location_id': self.warehouse_id.lot_stock_id.id,
        'location_dest_id': self.partner_id.property_stock_customer.id,
    }

def _create_picking(self):
    """Create stock picking for delivery"""
    for order in self:
        if not order.order_line:
            continue

        # Check if product requires delivery
        lines = order.order_line.filtered(lambda l: l.product_id.type in ['consu', 'product'])

        if not lines:
            continue

        # Create picking
        picking = self.env['stock.picking'].create(order._prepare_picking())

        # Create moves
        moves = lines._create_stock_moves(picking)
        moves._action_confirm()
        moves._action_assign()
```

## Sale Order Line Computation

### Compute Amounts

```python
@api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id')
def _compute_amount(self):
    """Compute amounts for sale order line"""
    for line in self:
        price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)

        taxes = line.tax_id.compute_all(
            price,
            line.order_id.currency_id,
            line.product_uom_qty,
            product=line.product_id,
            partner=line.order_id.partner_id
        )

        line.update({
            'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
            'price_total': taxes['total_included'],
            'price_subtotal': taxes['total_excluded'],
        })
```

### Onchange Methods

```python
@api.onchange('product_id', 'price_unit', 'product_uom_qty', 'product_uom', 'tax_id')
def _onchange_discount(self):
    """Apply pricelist discount"""
    if not self.product_id:
        return {}

    # Get discount from pricelist
    self.discount = self.order_id.pricelist_id.get_product_price(
        self.product_id,
        self.product_uom_qty or 1.0,
        self.order_id.partner_id,
        self.order_id.date_order
    )

    return {}

@api.onchange('product_id')
def onchange_product_id(self):
    """Update fields when product changes"""
    if not self.product_id:
        return {}

    # Get description from product
    self.name = self.product_id.get_product_multiline_description_sale()

    # Get uom from product
    self.product_uom = self.product_id.uom_id.id

    # Get price from pricelist
    self.price_unit = self.order_id.pricelist_id.get_product_price(
        self.product_id,
        self.product_uom_qty or 1.0,
        self.order_id.partner_id,
        self.order_id.date_order
    )

    # Get taxes from product
    self.tax_id = self.product_id.taxes_id.filtered(
        lambda t: t.company_id == self.order_id.company_id
    )

    return {}
```

## Pricing and Discounts

### Pricelist Computation

```python
def _compute_price_rule(self, products, qty, date=None):
    """Compute price from pricelist"""
    self.ensure_one()

    products = products.with_context(**self._context)

    results = {}
    for product in products:
        # Get price rule
        rule = self.item_ids._compute_price_rule(
            product,
            qty,
            date or fields.Date.today()
        )

        results[product.id] = rule

    return results
```

### Global Discount on Order

```python
class SaleOrder(models.Model):
    _inherit = 'sale.order'

    global_discount_type = fields.Selection([
        ('percent', 'Percentage'),
        ('fixed', 'Fixed Amount'),
    ], string='Discount Type', default='percent')

    global_discount = fields.Float(string='Global Discount')

    def _amount_all(self):
        """Compute total with global discount"""
        super()._amount_all()

        for order in self:
            if order.global_discount_type == 'percent':
                discount = order.amount_untaxed * (order.global_discount / 100)
            else:
                discount = order.global_discount

            order.update({
                'global_discount_amount': discount,
                'amount_total': order.amount_untaxed + order.amount_tax - discount,
            })
```

## Invoicing Integration

### Invoiceable Lines

```python
def _get_invoiceable_lines(self):
    """Get lines that can be invoiced"""
    down_payment_lines = self.env['sale.order.line']

    invoiceable_lines = self.order_line.filtered(
        lambda l: not l.is_down_payment
    )

    # Filter based on invoice policy
    for line in invoiceable_lines:
        if line.product_id.invoice_policy == 'order':
            # Invoice based on ordered qty
            if line.qty_to_invoice > 0:
                yield line
        elif line.product_id.invoice_policy == 'delivery':
            # Invoice based on delivered qty
            if line.qty_to_invoice > 0:
                yield line
```

### Journal Selection

```python
def _get_journal(self):
    """Get sales journal for invoice"""
    return self.env['account.journal'].search([
        ('type', '=', 'sale'),
        ('company_id', '=', self.company_id.id),
    ], limit=1)
```

## Common Extends

### Add Custom Field to Sale Order

```python
# models/sale_order.py
class SaleOrder(models.Model):
    _inherit = 'sale.order'

    delivery_date = fields.Date(string='Delivery Date')
    internal_notes = fields.Text(string='Internal Notes')
    customer_reference = fields.Char(string='Customer Ref')

# views/sale_order_views.xml
<record id="view_order_form_inherit" model="ir.ui.view">
    <field name="name">sale.order.form.inherit</field>
    <field name="model">sale.order</field>
    <field name="inherit_id" ref="sale.view_order_form"/>
    <field name="arch" type="xml">
        <xpath expr="//field[@name='date_order']" position="after">
            <field name="delivery_date"/>
            <field name="customer_reference"/>
        </xpath>
        <xpath expr="//notebook" position="inside">
            <page string="Internal Notes">
                <field name="internal_notes"/>
            </page>
        </xpath>
    </field>
</record>
```

## References

- Sale module: https://github.com/odoo/odoo/tree/18.0/addons/sale
- Sale models: https://github.com/odoo/odoo/blob/18.0/addons/sale/models/sale_order.py
- Documentation: https://www.odoo.com/documentation/18.0/applications/sales.html
