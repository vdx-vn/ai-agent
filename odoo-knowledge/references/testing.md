# Testing Reference

## Test Structure

### Test File Layout

```python
# tests/test_my_model.py
# -*- coding: utf-8 -*-

from odoo.tests import common, tagged
from odoo.exceptions import ValidationError, UserError


class TestMyModel(common.TransactionCase):
    """Standard transaction case - rollback after each test"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Setup shared data for all tests
        cls.partner = cls.env['res.partner'].create({
            'name': 'Test Partner',
        })

    def setUp(self):
        super().setUp()
        # Setup for each test
        self.model = self.env['my.model']

    def test_create_record(self):
        """Test basic record creation"""
        record = self.model.create({
            'name': 'Test Record',
            'partner_id': self.partner.id,
        })
        self.assertEqual(record.name, 'Test Record')

    def test_state_transition(self):
        """Test state transition"""
        record = self.model.create({'name': 'Test'})
        self.assertEqual(record.state, 'draft')

        record.action_confirm()
        self.assertEqual(record.state, 'confirmed')


@tagged('-standard', 'post_install')
class TestMyModelPostInstall(common.TransactionCase):
    """Tests that run after module installation"""
    pass


class TestMyModelHttp(common.HttpCase):
    """HTTP tests for web controllers"""

    def test_web_page_loads(self):
        """Test that a page loads correctly"""
        response = self.url_open('/my/page')
        self.assertEqual(response.status_code, 200)
```

## Common Test Patterns

### Test Record Creation

```python
def test_create_basic_record(self):
    """Test creating a basic record"""
    record = self.env['sale.order'].create({
        'partner_id': self.partner.id,
        'date_order': fields.Datetime.now(),
    })
    self.assertTrue(record.id)
    self.assertEqual(record.state, 'draft')

def test_create_with_lines(self):
    """Test creating record with lines"""
    product = self.env['product.product'].create({
        'name': 'Test Product',
        'list_price': 100,
    })

    order = self.env['sale.order'].create({
        'partner_id': self.partner.id,
        'order_line': [(0, 0, {
            'product_id': product.id,
            'product_uom_qty': 2,
            'price_unit': 100,
        })],
    })

    self.assertEqual(len(order.order_line), 1)
    self.assertEqual(order.amount_total, 200)
```

### Test Onchange

```python
def test_onchange_product(self):
    """Test onchange method for product"""
    order_line = self.env['sale.order.line'].new({
        'order_id': self.order.id,
    })

    product = self.env['product.product'].create({
        'name': 'Test Product',
        'list_price': 150,
    })

    # Trigger onchange
    order_line.product_id = product
    order_line._onchange_product_id()

    self.assertEqual(order_line.price_unit, 150)
```

### Test Constraints

```python
def test_constraint_date_validation(self):
    """Test that date constraint works"""
    with self.assertRaises(ValidationError):
        self.env['my.model'].create({
            'name': 'Test',
            'date': fields.Date.today() + timedelta(days=1),  # Future date
        })

def test_constraint_required_fields(self):
    """Test that required fields are enforced"""
    with self.assertRaises(Exception):
        self.env['my.model'].create({
            'name': '',  # Empty required field
        })
```

### Test Access Rights

```python
class TestAccessRights(common.TransactionCase):
    def test_user_can_read_own_records(self):
        """Test users can read their own records"""
        # Create user
        user = self.env['res.users'].create({
            'name': 'Test User',
            'login': 'testuser',
            'groups_id': [(4, self.env.ref('base.group_user').id)],
        })

        # Create record as that user
        record = self.env['my.model'].sudo(user.id).create({
            'name': 'My Record',
        })

        # User can read
        records = self.env['my.model'].sudo(user.id).search([])
        self.assertEqual(len(records), 1)

    def test_user_cannot_delete_others_records(self):
        """Test record rules prevent deletion"""
        # Create two users
        user1 = self.env['res.users'].create({'name': 'User 1', 'login': 'user1'})
        user2 = self.env['res.users'].create({'name': 'User 2', 'login': 'user2'})

        # Create record as user1
        record = self.env['my.model'].sudo(user1.id).create({'name': 'Record'})

        # User2 cannot delete
        with self.assertRaises(AccessError):
            record.sudo(user2.id).unlink()
```

### Test Business Logic

```python
def test_confirm_order_validates_lines(self):
    """Test that confirming order validates lines"""
    order = self.env['sale.order'].create({
        'partner_id': self.partner.id,
        'order_line': [(5, 0, 0)],  # Clear lines
    })

    with self.assertRaises(UserError):
        order.action_confirm()

def test_compute_field_updates(self):
    """Test that computed fields update correctly"""
    product = self.env['product.product'].create({
        'name': 'Product',
        'list_price': 100,
    })

    order = self.env['sale.order'].create({
        'partner_id': self.partner.id,
        'order_line': [(0, 0, {
            'product_id': product.id,
            'product_uom_qty': 2,
            'price_unit': 100,
        })],
    })

    # Trigger computation
    order._compute_amount_total()

    self.assertEqual(order.amount_total, 200)
```

## Test Data Setup

### Using Demo Data

```python
@tagged('post_install')
class TestWithDemoData(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Use demo data from other modules
        cls.product_product = cls.env.ref('product.product_product_1')
        cls.pricelist = cls.env.ref('product.list0')
        cls.warehouse = cls.env.ref('stock.warehouse0')
```

### Creating Test Fixtures

```python
class TestFixtures(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Create test partner
        cls.partner = cls.env['res.partner'].create({
            'name': 'Test Partner',
            'email': 'test@example.com',
        })

        # Create test product
        cls.product = cls.env['product.product'].create({
            'name': 'Test Product',
            'list_price': 100,
            'standard_price': 50,
            'type': 'product',
            'categ_id': cls.env.ref('product.product_category_all').id,
        })

        # Create test pricelist
        cls.pricelist = cls.env['product.pricelist'].create({
            'name': 'Test Pricelist',
            'currency_id': cls.env.company.currency_id.id,
        })
```

## Test Tags and Categories

### Running Specific Tests

```python
# Run only fast tests
# odoo -d test_db --test-enable --test-tags=+fast --stop-after-init

# Run only post_install tests
# odoo -d test_db --test-enable --test-tags=+post_install --stop-after-init

# Run everything except standard tests
# odoo -d test_db --test-enable --test-tags=-standard --stop-after-init
```

### Tagging Tests

```python
@tagged('fast')
class TestFastCalculations(common.TransactionCase):
    """Tests that run quickly (no external calls)"""
    def test_computation(self):
        pass


@tagged('slow')
class TestSlowOperations(common.TransactionCase):
    """Tests that take longer (external API, etc)"""
    pass


@tagged('external')
class TestExternalServices(common.TransactionCase):
    """Tests that depend on external services"""
    pass
```

## Test Assertions

### Common Assertions

```python
# Equality
self.assertEqual(record.state, 'draft')
self.assertNotEqual(record.amount, 0)

# Boolean
self.assertTrue(record.active)
self.assertFalse(record.archived)

# None
self.assertIsNone(record.parent_id)
self.assertIsNotNone(record.partner_id)

# In
self.assertIn(record.state, ['draft', 'sent'])

# Count
self.assertEqual(len(records), 5)

# Float comparison
self.assertAlmostEqual(record.amount, 100.5, places=2)

# Exception
with self.assertRaises(UserError):
    record.action_cancel()

with self.assertRaisesRegex(ValidationError, 'Invalid date'):
    record.validate()
```

## Performance Testing

### Query Count Testing

```python
@tagged('post_install', '-standard')
class TestPerformance(common.TransactionCase):
    def test_query_count(self):
        """Test that queries are optimized"""
        # Enable query counting
        self.env.cr.execute("SELECT 1")  # Warm up

        with self.assertQueryCount(__import=3):  # Max 3 queries
            records = self.env['my.model'].search_read([], ['name', 'date'])

    def test_n_plus_one(self):
        """Test for N+1 query problem"""
        partners = self.env['res.partner'].search([], limit=10)

        # Bad: N+1 queries
        # for partner in partners:
        #     orders = self.env['sale.order'].search([('partner_id', '=', partner.id)])

        # Good: 1 query
        orders = self.env['sale.order'].search([('partner_id', 'in', partners.ids)])
        for partner in partners:
            partner_orders = orders.filtered(lambda o: o.partner_id == partner)
```

## Testing Wizards

```python
def test_wizard(self):
    """Test wizard functionality"""
    # Create wizard
    wizard = self.env['my.wizard'].with_context({
        'active_id': self.record.id,
        'active_model': 'my.model',
    }).create({
        'field1': 'value1',
    })

    # Execute wizard action
    wizard.action_execute()

    # Check result
    self.record.refresh()
    self.assertEqual(self.record.state, 'done')
```

## Testing PDF Reports

```python
def test_report_generation(self):
    """Test that report generates without errors"""
    report = self.env.ref('my_module.report_my_model')

    # Generate report
    pdf_content, _ = report._render_qweb_pdf([self.record.id])

    # Check content
    self.assertTrue(len(pdf_content) > 0)
    self.assertTrue(pdf_content.startswith(b'%PDF'))  # PDF header
```

## Debugging Tests

### Print Debugging

```python
def test_debug(self):
    record = self.env['my.model'].create({'name': 'Test'})

    # Print for debugging
    print("\nRecord state:", record.state)
    print("Record values:", record.read()[0])

    # Or use pdb
    # import pdb; pdb.set_trace()
```

### Browser Tests

```python
class TestBrowser(common.HttpCase):
    def test_browser_interaction(self):
        """Test user interaction in browser"""
        # Start tour
        self.browser_js(
            url_path='/web',
            code="odoo.__DEBUG__.services['web_tour.tour'].run('my_tour_name')",
            ready="odoo.__DEBUG__.services['web_tour.tour'].tours.my_tour_name.ready",
        )
```

## Best Practices

1. **Use descriptive test names**
   ```python
   # Good
   def test_confirm_order_without_lines_raises_error(self):

   # Bad
   def test_error(self):
   ```

2. **Use setUpClass for shared data**
   ```python
   @classmethod
   def setUpClass(cls):
       super().setUpClass()
       cls.shared_data = cls.env['my.model'].create({})
   ```

3. **Make tests independent**
   ```python
   # Bad - tests depend on order
   def test_1_create(self):
       self.record = self.env['my.model'].create({})

   def test_2_update(self):
       self.record.write({})  # Depends on test_1
   ```

4. **Use appropriate test tags**
   ```python
   @tagged('post_install', '-standard')  # Runs after module install
   class TestMyFeature(common.TransactionCase):
       pass
   ```

## References

- Testing: https://www.odoo.com/documentation/18.0/developer/reference/backend/testing.html
- Test modules: https://github.com/odoo/odoo/tree/18.0/addons/base/tests
