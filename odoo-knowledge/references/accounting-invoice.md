# Accounting and Invoice Reference

## Account Move (Invoice)

### Invoice Structure

```python
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class AccountMove(models.Model):
    _inherit = 'account.move'

    # Core fields
    name = fields.Char(string='Number', required=True, copy=False,
                       readonly=True, index=True, default=lambda self: _('New'))

    move_type = fields.Selection([
        ('entry', 'Journal Entry'),
        ('out_invoice', 'Customer Invoice'),
        ('out_refund', 'Customer Credit Note'),
        ('in_invoice', 'Vendor Bill'),
        ('in_refund', 'Vendor Credit Note'),
        ('out_receipt', 'Sales Receipt'),
        ('in_receipt', 'Purchase Receipt'),
    ], string='Type', required=True, index=True, default='entry',
       tracking=True)

    partner_id = fields.Many2one('res.partner', string='Partner',
                                 required=True, index=True, tracking=True)

    invoice_date = fields.Date(string='Invoice Date',
                              default=fields.Date.context_today,
                              tracking=True)

    invoice_date_due = fields.Date(string='Due Date',
                                  compute='_compute_invoice_date_due',
                                  store=True, readonly=True)

    invoice_payment_term_id = fields.Many2one('account.payment.term',
                                             string='Payment Terms')

    invoice_line_ids = fields.One2many('account.move.line',
                                      'move_id',
                                      string='Journal Items',
                                      copy=False)

    amount_total = fields.Monetary(string='Total',
                                  store=True,
                                  readonly=True,
                                  compute='_compute_amount',
                                  tracking=True)

    amount_residual = fields.Monetary(string='Amount Due',
                                     compute='_compute_amount',
                                     tracking=True)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('posted', 'Posted'),
        ('cancel', 'Cancelled'),
    ], string='Status', required=True, readonly=True, copy=False,
       tracking=True, default='draft')

    currency_id = fields.Many2one('res.currency',
                                  string='Currency',
                                  required=True,
                                  default=lambda self: self.env.company.currency_id)

    company_id = fields.Many2one('res.company',
                                string='Company',
                                default=lambda self: self.env.company,
                                required=True)

    journal_id = fields.Many2one('account.journal',
                                string='Journal',
                                required=True,
                                domain="[('company_id', '=', company_id)]")

    # For customer invoices
    invoice_origin = fields.Char(string='Source Document')
    payment_reference = fields.Char(string='Payment Reference')

    user_id = fields.Many2one('res.users',
                             string='Salesperson',
                             default=lambda self: self.env.user)

    fiscal_position_id = fields.Many2one('account.fiscal.position',
                                        string='Fiscal Position')

    narration = fields.Text(string='Notes')
```

### Invoice Line Structure

```python
class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    move_id = fields.Many2one('account.move', string='Journal Entry',
                             required=True, index=True, ondelete='cascade')

    product_id = fields.Many2one('product.product', string='Product')

    name = fields.Text(string='Label')

    quantity = fields.Float(string='Quantity',
                           default=1.0,
                           digits='Product Unit of Measure')

    product_uom_id = fields.Many2one('uom.uom', string='Unit of Measure')

    price_unit = fields.Float(string='Unit Price')

    discount = fields.Float(string='Discount (%)')

    price_subtotal = fields.Monetary(string='Subtotal',
                                    compute='_compute_totals',
                                    store=True)

    price_total = fields.Monetary(string='Total',
                                 compute='_compute_totals',
                                 store=True)

    account_id = fields.Many2one('account.account',
                                string='Account',
                                required=True,
                                domain="[('company_id', '=', company_id)]")

    tax_ids = fields.Many2many('account.tax', string='Taxes')

    tax_line_id = fields.Many2one('account.tax', string='Originator Tax',
                                 ondelete='restrict')

    # Reconciliation
    reconciled = fields.Boolean(string='Reconciled',
                               compute='_compute_reconciled',
                               store=True)

    amount_residual = fields.Monetary(string='Residual Amount',
                                     compute='_compute_amount_residual')

    amount_currency = fields.Monetary(string='Amount in Currency',
                                     help="The amount expressed in an optional other currency.")

    company_id = fields.Many2one('res.company',
                                string='Company',
                                default=lambda self: self.env.company)

    partner_id = fields.Many2one('res.partner', string='Partner')
```

## Invoice Operations

### Create Customer Invoice

```python
def create_customer_invoice(self, partner_id, lines):
    """Create a customer invoice"""
    return self.env['account.move'].create({
        'move_type': 'out_invoice',
        'partner_id': partner_id,
        'invoice_date': fields.Date.today(),
        'invoice_line_ids': [(0, 0, line) for line in lines],
    })

# Example usage
invoice = self.env['account.move'].create({
    'move_type': 'out_invoice',
    'partner_id': customer_id,
    'invoice_date': fields.Date.today(),
    'invoice_payment_term_id': self.env.ref('account.payment_term_15_days').id,
    'invoice_line_ids': [
        (0, 0, {
            'name': 'Consulting Services',
            'product_id': self.env.ref('product.product_product_1').id,
            'quantity': 10,
            'price_unit': 100,
            'account_id': self.env['account.account'].search([
                ('account_type', '=', 'income'),
                ('company_id', '=', self.env.company.id)
            ], limit=1).id,
            'tax_ids': [(6, 0, self.env['account.tax'].search([
                ('type_tax_use', '=', 'sale')
            ]).ids)],
        }),
    ],
})
```

### Post Invoice

```python
def action_post(self):
    """Post the invoice"""
    for move in self:
        # Validate before posting
        if move.state != 'draft':
            raise UserError(_('Only draft invoices can be posted'))

        # Validate invoice lines
        if not move.invoice_line_ids:
            raise UserError(_('An invoice must have at least one line.'))

        # Check if amount is zero
        if move.amount_total == 0:
            raise UserError(_('Cannot post an invoice with zero total.'))

        # Call super to post
        move._post(soft=False)

    return True
```

### Cancel Invoice

```python
def button_cancel(self):
    """Cancel the invoice"""
    for move in self:
        # Check if payments exist
        if move.payment_state != 'not_paid':
            raise UserError(_('You cannot cancel an invoice that is paid.'))

        # Check if attached to a payment
        if move.line_ids.mapped('payment_id'):
            raise UserError(_('You cannot cancel an invoice that is attached to a payment.'))

        # Cancel
        move.state = 'cancel'

    return True

def button_draft(self):
    """Reset to draft"""
    for move in self:
        # Only cancelled invoices can be reset
        if move.state != 'cancel':
            raise UserError(_('Only cancelled invoices can be reset to draft.'))

        move.state = 'draft'

    return True
```

## Payment Management

### Register Payment

```python
def action_register_payment(self):
    """Open payment registration wizard"""
    return {
        'type': 'ir.actions.act_window',
        'name': _('Register Payment'),
        'res_model': 'account.payment.register',
        'view_mode': 'form',
        'target': 'new',
        'context': {
            'active_model': 'account.move',
            'active_ids': self.ids,
        },
    }

def _create_payment(self, journal, amount, payment_date=None, communication=None):
    """Create payment for invoice"""
    return self.env['account.payment'].create({
        'payment_type': 'inbound' if self.move_type == 'out_invoice' else 'outbound',
        'partner_type': 'customer' if self.move_type in ['out_invoice', 'out_refund'] else 'vendor',
        'partner_id': self.partner_id.id,
        'journal_id': journal.id,
        'amount': amount,
        'payment_date': payment_date or fields.Date.context_today(self),
        'communication': communication or self.payment_reference or self.name,
        'invoice_ids': [(6, 0, self.ids)],
    })
```

### Payment Reconciliation

```python
class AccountPayment(models.Model):
    _inherit = 'account.payment'

    def action_post(self):
        """Post payment and reconcile"""
        for payment in self:
            # Validate
            if payment.state != 'draft':
                continue

            if not payment.partner_id:
                raise UserError(_('The payment must be linked to a partner.'))

            # Post the payment
            payment._check_payment_id()
            payment.move_id._post(soft=False)

            # Reconcile
            payment._seek_for_lines()

        return True

    def _seek_for_lines(self):
        """Reconcile payment with invoice"""
        for payment in self:
            # Get counterpart lines
            lines = payment.move_id.line_ids.filtered(
                lambda l: l.account_id == payment.destination_account_id
            )

            # Get invoice lines to reconcile
            if payment.invoice_ids:
                invoice_lines = payment.invoice_ids.line_ids.filtered(
                    lambda l: l.account_id.account_type in ('asset_receivable', 'liability_payable')
                )

                # Reconcile
                (lines + invoice_lines).reconcile()
```

## Tax Management

### Tax Computation

```python
def _compute_tax_totals(self):
    """Compute tax totals for invoice"""
    for move in self:
        tax_lines = move.line_ids.filtered('tax_line_id')

        tax_totals = self.env['account.tax']._compute_tax_totals([
            {
                'price_unit': line.price_unit,
                'quantity': line.quantity,
                'discount': line.discount,
                'tax_ids': line.tax_ids,
                'product_id': line.product_id,
                'partner_id': move.partner_id,
            }
            for line in move.invoice_line_ids
        ])

        move.invoice_totals = tax_totals
```

### Tax Configuration

```python
# Create tax
tax = self.env['account.tax'].create({
    'name': 'VAT 10%',
    'type_tax_use': 'sale',
    'amount_type': 'percent',
    'amount': 10,
    'account_id': self.env['account.account'].search([
        ('account_type', '=', 'liability_current')
    ], limit=1).id,
    'invoice_repartition_line_ids': [
        (0, 0, {
            'factor_percent': 100,
            'repartition_type': 'base',
        }),
        (0, 0, {
            'factor_percent': 100,
            'repartition_type': 'tax',
            'account_id': tax_account_id,
        }),
    ],
})
```

## Financial Reports

### Balance Sheet

```python
def get_balance_sheet(self, date_from, date_to):
    """Generate balance sheet data"""
    # Get accounts
    asset_accounts = self.env['account.account'].search([
        ('account_type', 'in', ['asset_current', 'asset_non_current', 'asset_cash']),
        ('company_id', '=', self.env.company.id),
    ])

    liability_accounts = self.env['account.account'].search([
        ('account_type', 'in', ['liability_current', 'liability_non_current']),
        ('company_id', '=', self.env.company.id),
    ])

    equity_accounts = self.env['account.account'].search([
        ('account_type', '=', 'equity'),
        ('company_id', '=', self.env.company.id),
    ])

    # Compute balances
    return {
        'assets': sum(acc.balance for acc in asset_accounts),
        'liabilities': sum(acc.balance for acc in liability_accounts),
        'equity': sum(acc.balance for acc in equity_accounts),
    }
```

### Profit & Loss

```python
def get_profit_loss(self, date_from, date_to):
    """Generate profit and loss data"""
    # Get income and expense accounts
    income_accounts = self.env['account.account'].search([
        ('account_type', '=', 'income'),
        ('company_id', '=', self.env.company.id),
    ])

    expense_accounts = self.env['account.account'].search([
        ('account_type', '=', 'expense'),
        ('company_id', '=', self.env.company.id),
    ])

    # Compute balances for period
    return {
        'revenue': sum(acc.balance for acc in income_accounts),
        'expenses': sum(acc.balance for acc in expense_accounts),
        'profit': sum(acc.balance for acc in income_accounts) - sum(acc.balance for acc in expense_accounts),
    }
```

## Fiscal Position

### Apply Fiscal Position

```python
def _compute_fiscal_position_id(self):
    """Compute fiscal position based on partner"""
    for move in self:
        if move.partner_id:
            move.fiscal_position_id = move.partner_id.property_account_position_id
        else:
            move.fiscal_position_id = False

@api.onchange('partner_id')
def _onchange_partner_id(self):
    """Update fiscal position when partner changes"""
    for move in self:
        if move.partner_id:
            move.fiscal_position_id = move.partner_id.property_account_position_id
            # Update payment term
            if move.partner_id.property_payment_term_id:
                move.invoice_payment_term_id = move.partner_id.property_payment_term_id

@api.onchange('fiscal_position_id')
def _onchange_fiscal_position_id(self):
    """Apply fiscal position to invoice lines"""
    for move in self:
        if not move.fiscal_position_id:
            continue

        for line in move.invoice_line_ids:
            # Map taxes
            if line.product_id:
                line._onchange_product_id()
                # Apply fiscal position
                line.tax_ids = move.fiscal_position_id.map_tax(
                    line.product_id.taxes_id,
                    line.product_id,
                    move.partner_id
                )

            # Map account
            line.account_id = move.fiscal_position_id.map_account(line.account_id)
```

## References

- Accounting: https://github.com/odoo/odoo/tree/18.0/addons/account
- Account move: https://github.com/odoo/odoo/blob/18.0/addons/account/models/account_move.py
- Documentation: https://www.odoo.com/documentation/18.0/applications/accounting.html
