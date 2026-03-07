# Stock and Inventory Reference

## Stock Picking

### Picking Structure

```python
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    name = fields.Char(string='Reference', default=lambda self: _('New'),
                       index=True, readonly=True)

    origin = fields.Char(string='Source Document',
                        help="Reference of the document that created this picking")

    move_type = fields.Selection([
        ('direct', 'As soon as possible'),
        ('one', 'When all products are ready'),
    ], string='Operation Type', default='direct', required=True)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('waiting', 'Waiting Another Operation'),
        ('confirmed', 'Waiting'),
        ('assigned', 'Ready'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], string='Status', default='draft', tracking=True)

    move_ids_without_package = fields.One2many('stock.move',
                                               'picking_id',
                                               string='Stock Moves',
                                               copy=True)

    location_id = fields.Many2one('stock.location', string='Source Location',
                                  required=True, readonly=True,
                                  states={'draft': [('readonly', False)]})

    location_dest_id = fields.Many2one('stock.location', string='Destination Location',
                                       required=True, readonly=True,
                                       states={'draft': [('readonly', False)]})

    picking_type_id = fields.Many2one('stock.picking.type', string='Operation Type',
                                      required=True, readonly=True,
                                      default=lambda self: self._default_picking_type())

    partner_id = fields.Many2one('res.partner', string='Partner')

    company_id = fields.Many2one('res.company', string='Company',
                                default=lambda self: self.env.company)

    date_done = fields.Datetime(string='Date of Transfer', readonly=True,
                               copy=False)

    # For backorders
    backorder_id = fields.Many2one('stock.picking', string='Back Order of',
                                  readonly=True)

    # For linked pickings
    backorder_ids = fields.One2many('stock.picking', 'backorder_id',
                                   string='Back Orders')

    # Priority
    priority = fields.Selection([
        ('0', 'Not urgent'),
        ('1', 'Normal'),
        ('2', 'Urgent'),
        ('3', 'Very Urgent'),
    ], string='Priority', default='1')
```

### Stock Move Structure

```python
class StockMove(models.Model):
    _inherit = 'stock.move'

    name = fields.Text(string='Description')

    reference = fields.Char(string='Reference')

    product_id = fields.Many2one('product.product', string='Product',
                                required=True)

    product_qty = fields.Float(string='Quantity',
                              default=0.0,
                              digits='Product Unit of Measure',
                              required=True)

    product_uom = fields.Many2one('uom.uom', string='Unit of Measure',
                                 required=True)

    product_uom_qty = fields.Float(string='Reserved',
                                   default=0.0,
                                   digits='Product Unit of Measure')

    location_id = fields.Many2one('stock.location', string='Source Location',
                                 required=True)

    location_dest_id = fields.Many2one('stock.location', string='Destination Location',
                                      required=True)

    picking_id = fields.Many2one('stock.picking', string='Transfer',
                                ondelete='cascade')

    state = fields.Selection([
        ('draft', 'New'),
        ('cancel', 'Cancelled'),
        ('confirmed', 'Waiting Availability'),
        ('partially_available', 'Partially Available'),
        ('assigned', 'Available'),
        ('done', 'Done'),
    ], string='Status')

    # Chain of moves
    move_orig_ids = fields.One2many('stock.move', 'move_dest_id',
                                   string='Original Moves')

    move_dest_ids = fields.One2many('stock.move', 'move_orig_ids',
                                   string='Destination Moves')

    # Quantity fields
    quantity_done = fields.Float(string='Done',
                                default=0.0,
                                digits='Product Unit of Measure')

    reserved_availability = fields.Float(string='Reserved',
                                        compute='_compute_reserved_availability')

    availability = fields.Float(string='Availability',
                               compute='_compute_availability')

    # Additional info
    note = fields.Text(string='Notes')

    origin = fields.Char(string='Source')
```

## Picking Operations

### Create Picking

```python
def create_picking(self, partner_id, picking_type, lines):
    """Create a stock picking"""
    picking_type = self.env['stock.picking.type'].search([
        ('code', '=', picking_type),
        ('company_id', '=', self.env.company.id),
    ], limit=1)

    if not picking_type:
        raise UserError(_('No picking type found for %s') % picking_type)

    picking = self.env['stock.picking'].create({
        'partner_id': partner_id,
        'picking_type_id': picking_type.id,
        'location_id': picking_type.default_location_src_id.id,
        'location_dest_id': picking_type.default_location_dest_id.id,
        'move_ids_without_package': [(0, 0, line) for line in lines],
    })

    return picking

# Example usage
picking = self.env['stock.picking'].create({
    'partner_id': customer.id,
    'picking_type_id': self.env.ref('stock.picking_type_out').id,
    'location_id': self.env.ref('stock.stock_location_stock').id,
    'location_dest_id': self.env.ref('stock.stock_location_customers').id,
    'move_ids_without_package': [
        (0, 0, {
            'name': product.name,
            'product_id': product.id,
            'product_uom_qty': 10,
            'product_uom': product.uom_id.id,
            'location_id': self.env.ref('stock.stock_location_stock').id,
            'location_dest_id': self.env.ref('stock.stock_location_customers').id,
        }),
    ],
})
```

### Validate Picking

```python
def action_validate(self):
    """Validate the picking"""
    for picking in self:
        # Check state
        if picking.state not in ['assigned', 'partially_available']:
            raise UserError(_('Picking must be ready to validate.'))

        # Check if all moves are done
        if any(move.state != 'done' for move in picking.move_ids_without_package):
            # Process remaining moves
            picking._action_done()

    return True

def button_validate(self):
    """Standard validate button"""
    # Check if backorder needed
    if any(move.quantity_done < move.product_uom_qty for move in self.move_ids_without_package):
        # Show backorder wizard
        return {
            'type': 'ir.actions.act_window',
            'name': _('Create Backorder'),
            'res_model': 'stock.backorder.confirmation',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'pick_ids': self.ids,
            },
        }

    # Validate directly
    self._action_done()
    return True
```

### Cancel Picking

```python
def action_cancel(self):
    """Cancel the picking"""
    for picking in self:
        if picking.state == 'done':
            raise UserError(_('Cannot cancel a done transfer.'))

        # Cancel moves
        picking.move_ids_without_package._action_cancel()

        picking.state = 'cancel'

    return True
```

## Stock Quant (Inventory)

### Quant Structure

```python
class StockQuant(models.Model):
    _inherit = 'stock.quant'

    product_id = fields.Many2one('product.product', string='Product',
                                required=True, ondelete='cascade')

    location_id = fields.Many2one('stock.location', string='Location',
                                 required=True, ondelete='cascade')

    quantity = fields.Float(string='Quantity',
                           help='Quantity of products in this quant',
                           default=0.0,
                           digits='Product Unit of Measure')

    reserved_quantity = fields.Float(string='Reserved Quantity',
                                    default=0.0,
                                    digits='Product Unit of Measure')

    available_quantity = fields.Float(string='Available',
                                     compute='_compute_available_quantity',
                                     store=True)

    lot_id = fields.Many2one('stock.lot', string='Lot')

    package_id = fields.Many2one('stock.quant.package', string='Package')

    owner_id = fields.Many2one('res.partner', string='Owner')

    company_id = fields.Many2one('res.company', string='Company')
```

### Get Current Stock

```python
def get_stock_quantity(self, product, location=None):
    """Get current stock quantity for a product"""
    domain = [
        ('product_id', '=', product.id),
    ]

    if location:
        domain.append(('location_id', 'child_of', location.id))

    quants = self.env['stock.quant'].search(domain)

    return sum(quant.quantity for quant in quants)

def get_virtual_quantity(self, product, location=None):
    """Get virtual available quantity (on hand - outgoing + incoming)"""
    # Get on hand
    on_hand = self.get_stock_quantity(product, location)

    # Get outgoing
    outgoing_domain = [
        ('product_id', '=', product.id),
        ('state', 'in', ['confirmed', 'assigned', 'partially_available']),
        ('picking_type_id.code', '=', 'outgoing'),
    ]
    if location:
        outgoing_domain.append(('location_id', 'child_of', location.id))

    outgoing = self.env['stock.move'].search(outgoing_domain)
    outgoing_qty = sum(move.product_uom_qty - move.quantity_done for move in outgoing)

    # Get incoming
    incoming_domain = [
        ('product_id', '=', product.id),
        ('state', 'in', ['confirmed', 'assigned', 'partially_available']),
        ('picking_type_id.code', '=', 'incoming'),
    ]
    if location:
        incoming_domain.append(('location_dest_id', 'child_of', location.id))

    incoming = self.env['stock.move'].search(incoming_domain)
    incoming_qty = sum(move.product_uom_qty - move.quantity_done for move in incoming)

    return on_hand - outgoing_qty + incoming_qty
```

## Stock Rules and Procurement

### Procurement Rule

```python
class ProcurementRule(models.Model):
    _inherit = 'stock.rule'

    name = fields.Char(required=True)
    action = fields.Selection([
        ('pull', 'Pull From'),
        ('push', 'Push To'),
        ('pull_push', 'Pull & Push'),
    ], required=True, default='pull')

    procure_method = fields.Selection([
        ('make_to_stock', 'Take From Stock'),
        ('make_to_order', 'Trigger Another Operation'),
        ('mts_else_mto', 'Take From Stock, If Not Available, Trigger Another Operation'),
    ], string='Move Supply Method')

    location_id = fields.Many2one('stock.location', string='Supply Location')

    location_src_id = fields.Many2one('stock.location', string='Source Location')

    route_id = fields.Many2one('stock.location.route', string='Route')

    picking_type_id = fields.Many2one('stock.picking.type', string='Operation Type')
```

### Create Procurement

```python
def run_procurement(self, product, qty, location, company=None):
    """Run procurement for a product"""
    values = {
        'company_id': company or self.env.company,
        'date_planned': fields.Datetime.now(),
        'move_dest_ids': False,
        'warehouse_id': location.warehouse_id,
    }

    # Run procurement
    self.env['procurement.group'].run(
        product,
        qty,
        location.uom_id,
        location,
        False,
        values
    )
```

## Inventory Adjustment

### Create Inventory Adjustment

```python
def create_inventory_adjustment(self, product_id, location_id, qty):
    """Create inventory adjustment"""
    return self.env['stock.quant'].create({
        'product_id': product_id,
        'location_id': location_id,
        'inventory_quantity': qty,
    })

def start_inventory(self, location, products=None):
    """Start a new inventory"""
    inventory = self.env['stock.inventory'].create({
        'name': 'Inventory %s' % fields.Date.today(),
        'location_ids': [(6, 0, location.ids)],
    })

    if products:
        # Pre-fill with products
        inventory.action_start()
        for product in products:
            self.env['stock.inventory.line'].create({
                'inventory_id': inventory.id,
                'product_id': product.id,
                'product_qty': 0,
                'location_id': location.id,
            })

    return inventory
```

## Lot and Serial Number

### Lot/Serial Management

```python
class StockLot(models.Model):
    _inherit = 'stock.lot'

    name = fields.Char(string='Lot/Serial Number', required=True)

    product_id = fields.Many2one('product.product', string='Product',
                                required=True)

    ref = fields.Char(string='Internal Reference')

    create_date = fields.Datetime(string='Creation Date')

    use_date = fields.Datetime(string='Best before Date')

    life_date = fields.Datetime(string='End of Life Date')

    removal_date = fields.Datetime(string='Removal Date')

    expiry_date = fields.Datetime(string='Expiration Date')

    company_id = fields.Many2one('res.company', string='Company')
```

### Track Serial Numbers

```python
def generate_serial_numbers(self, product, start_number, count):
    """Generate serial numbers for product"""
    serials = []
    for i in range(count):
        serial = self.env['stock.lot'].create({
            'name': '%s-%06d' % (start_number, i + 1),
            'product_id': product.id,
            'company_id': self.env.company.id,
        })
        serials.append(serial.id)

    return serials
```

## Stock Scanning (Barcode)

### Barcode Scanning

```python
def on_barcode_scanned(self, barcode):
    """Handle barcode scan"""
    # Search product
    product = self.env['product.product'].search([
        '|', ('barcode', '=', barcode), ('default_code', '=', barcode)
    ], limit=1)

    if product:
        self._add_product(product)
    else:
        # Search lot
        lot = self.env['stock.lot'].search([('name', '=', barcode)], limit=1)
        if lot:
            self._add_lot(lot)
        else:
            raise UserError(_('No product or lot found for barcode: %s') % barcode)

def _add_product(self, product):
    """Add product to picking lines"""
    for move in self.move_ids_without_package:
        if move.product_id == product:
            move.quantity_done += 1
            return True

    # Create new move
    self.env['stock.move'].create({
        'picking_id': self.id,
        'name': product.name,
        'product_id': product.id,
        'product_uom_qty': 1,
        'product_uom': product.uom_id.id,
        'location_id': self.location_id.id,
        'location_dest_id': self.location_dest_id.id,
        'quantity_done': 1,
    })
    return True
```

## References

- Stock module: https://github.com/odoo/odoo/tree/18.0/addons/stock
- Stock models: https://github.com/odoo/odoo/blob/18.0/addons/stock/models/stock_picking.py
- Documentation: https://www.odoo.com/documentation/18.0/applications/inventory.html
