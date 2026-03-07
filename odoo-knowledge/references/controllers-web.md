# Controllers and Web Services Reference

## HTTP Controllers

### Basic Controller

```python
# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request


class MyController(http.Controller):

    @http.route('/my/page', type='http', auth='public', website=True)
    def my_page(self, **kwargs):
        """Render a simple web page"""
        return request.render('my_module.my_template', {
            'title': 'My Page',
            'data': {},
        })

    @http.route('/my/data', type='json', auth='user')
    def my_json_endpoint(self, **kwargs):
        """JSON endpoint for API calls"""
        return {
            'result': 'success',
            'data': []
        }
```

### Controller Route Parameters

```python
class MyController(http.Controller):

    # Route with parameters
    @http.route('/my/page/<int:page_id>', type='http', auth='public')
    def page_detail(self, page_id=0, **kwargs):
        record = request.env['my.model'].sudo().browse(page_id)
        if not record.exists():
            return request.not_found()
        return request.render('my_module.detail', {'record': record})

    # Route with multiple parameters
    @http.route('/my/model/<model_name>/<int:res_id>', type='http', auth='user')
    def model_record(self, model_name, res_id, **kwargs):
        # Validate model
        if model_name not in ['my.model', 'another.model']:
            return request.not_found()

        record = request.env[model_name].browse(res_id)
        return request.render('my_module.record', {'record': record})
```

### HTTP Request Methods

```python
class MyController(http.Controller):

    # GET only
    @http.route('/api/search', type='http', auth='user', methods=['GET'])
    def search_get(self, query='', **kwargs):
        results = request.env['my.model'].search([('name', 'ilike', query)])
        return request.make_json_response([{
            'id': r.id,
            'name': r.name
        } for r in results])

    # POST only
    @http.route('/api/create', type='http', auth='user', methods=['POST'])
    def create_post(self, **kwargs):
        data = request.get_json_data()
        record = request.env['my.model'].create(data)
        return request.make_json_response({
            'id': record.id,
            'success': True
        })

    # CSRF protected POST
    @http.route('/form/submit', type='http', auth='user', methods=['POST'], csrf=True)
    def form_submit(self, **post):
        # Form data is in post dict
        record = request.env['my.model'].create({
            'name': post.get('name'),
            'email': post.get('email'),
        })
        return request.redirect('/my/page/%d' % record.id)
```

## Authentication Types

| Type | Description | Use Case |
|------|-------------|----------|
| `auth='public'` | No authentication required | Public pages, website |
| `auth='user'` | Requires login (redirects to login) | Internal pages |
| `auth='none'` | No auth, no database | Multi-db selector, health checks |
| `auth='apikey'` | API key authentication | External API access |

```python
class AuthController(http.Controller):

    @http.route('/public/content', type='http', auth='public')
    def public_content(self):
        # Accessible without login
        return request.render('my_module.public')

    @http.route('/user/content', type='http', auth='user')
    def user_content(self):
        # Requires user login
        # request.env.user is available
        return request.render('my_module.private')

    @http.route('/api/external', type='json', auth='apikey')
    def api_endpoint(self, **kwargs):
        # For external API integration
        return {'user': request.env.user.login}
```

## Response Types

### HTML Response

```python
@http.route('/my/page', type='http', auth='public')
def html_page(self):
    return request.render('my_module.template', {
        'values': {
            'title': 'My Title',
            'items': [1, 2, 3],
        }
    })
```

### JSON Response

```python
@http.route('/api/data', type='http', auth='user')
def json_response(self):
    data = request.env['my.model'].search_read([], ['name', 'code'])
    return request.make_json_response(data)

# Or using type='json'
@http.route('/api/data2', type='json', auth='user')
def json_auto(self):
    # Automatically converts dict to JSON response
    return {'result': [{'name': 'Test'}]}
```

### Redirect Response

```python
@http.route('/action/process', type='http', auth='user')
def process_action(self):
    # Do something
    return request.redirect('/my/success')

# With status code
@http.route('/temporary', type='http', auth='user')
def temp_redirect(self):
    return request.redirect('/my/target', code=302)
```

### File Download

```python
@http.route('/download/report/<int:record_id>', type='http', auth='user')
def download_report(self, record_id):
    record = request.env['my.model'].browse(record_id)

    # Generate PDF
    pdf, _ = request.env.ref('my_module.report_template')._render_qweb_pdf([record.id])

    # Return as attachment
    pdfhttpheaders = [
        ('Content-Type', 'application/pdf'),
        ('Content-Length', len(pdf)),
        ('Content-Disposition', 'attachment; filename="report_%d.pdf";' % record_id)
    ]
    return request.make_response(pdf, headers=pdfhttpheaders)
```

### Error Responses

```python
@http.route('/api/check', type='http', auth='user')
def check_endpoint(self, **kwargs):
    record_id = kwargs.get('id')
    record = request.env['my.model'].browse(record_id)

    if not record.exists():
        return request.not_found()

    if not record.check_access():
        return request.forbidden()

    return request.make_json_response({'valid': True})
```

## Context and Environment

```python
class ContextController(http.Controller):

    @http.route('/context/info', type='json', auth='user')
    def context_info(self):
        return {
            # Current user
            'user_id': request.env.user.id,
            'user_name': request.env.user.name,

            # Current company
            'company_id': request.env.company.id,
            'company_name': request.env.company.name,

            # Database
            'db': request.env.cr.dbname,

            # Language
            'lang': request.env.context.get('lang'),

            # timezone
            'tz': request.env.context.get('tz'),
        }

    @http.route('/context/switch', type='json', auth='user')
    def switch_company(self, company_id):
        """Switch to different company"""
        company = request.env['res.company'].browse(company_id)
        if not company.exists():
            return {'error': 'Company not found'}

        # Switch company for this request
        request.env = request.env(context=dict(
            request.env.context,
            allowed_company_ids=[company_id]
        ))

        return {'success': True, 'company': company.name}
```

## Website Controller

```python
class WebsiteController(http.Controller):

    @http.route('/custom-page', type='http', auth='public', website=True)
    def custom_page(self, **kwargs):
        # Website=True enables website features
        # qweb context includes website, current user, etc.

        values = {
            'user': request.env.user,
            'is_public': request.env.user.has_group('base.group_public'),
            'products': request.env['product.product'].search([]),
        }

        # qcontext automatically gets website context
        qcontext = request.website.get_template('my_module.page')._get_values(values)

        return request.render('my_module.page', qcontext)
```

## QWeb Templates for Controllers

### Template Definition

```xml
<!-- views/my_templates.xml -->
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <template id="my_template" name="My Template">
        <t t-call="website.layout">
            <div id="wrap" class="oe_structure oe_empty">
                <div class="container">
                    <h1><t t-esc="title"/></h1>
                    <div t-if="data">
                        <t t-foreach="data" t-as="item">
                            <p><t t-esc="item"/></p>
                        </t>
                    </div>
                </div>
            </div>
        </t>
    </template>

    <!-- QWeb for backend -->
    <template id="my_backend_template">
        <div class="o_my_controller_content">
            <h2>My Backend Page</h2>
            <table class="table table-sm">
                <tr t-foreach="records" t-as="record">
                    <td><t t-esc="record.name"/></td>
                </tr>
            </table>
        </div>
    </template>
</odoo>
```

## Best Practices

### 1. Use sudo() carefully in controllers

```python
@http.route('/public/data', type='http', auth='public')
def public_data(self):
    # Use sudo() for public routes that need to access models
    records = request.env['my.model'].sudo().search([('public', '=', True)])
    return request.render('my_module.public', {'records': records})
```

### 2. Validate access rights

```python
@http.route('/sensitive/action', type='http', auth='user')
def sensitive_action(self, record_id):
    record = request.env['my.model'].browse(record_id)

    # Check if user can access this record
    if not record.exists():
        return request.not_found()

    # Check access rights explicitly
    try:
        record.check_access_rule('read')
    except AccessError:
        return request.forbidden()
```

### 3. Use proper HTTP methods

```python
# Query data: GET
@http.route('/api/search', type='http', auth='user', methods=['GET'])
def search(self, query):
    return request.make_json_response(
        request.env['my.model'].search_read([('name', 'ilike', query)])
    )

# Create data: POST
@http.route('/api/create', type='http', auth='user', methods=['POST'], csrf=False)
def create(self, **kwargs):
    record = request.env['my.model'].create(kwargs)
    return request.make_json_response({'id': record.id})
```

### 4. Handle errors gracefully

```python
@http.route('/api/process', type='json', auth='user')
def process(self, **kwargs):
    try:
        result = self._do_something(kwargs)
        return {'success': True, 'result': result}
    except ValidationError as e:
        return {'success': False, 'error': str(e)}
    except Exception as e:
        return {'success': False, 'error': 'Internal error'}
```

## References

- Controllers: https://www.odoo.com/documentation/18.0/developer/reference/backend/http.html
- Web controllers: https://github.com/odoo/odoo/blob/18.0/addons/web/controllers/main.py
- Website controllers: https://github.com/odoo/odoo/blob/18.0/addons/website/controllers/main.py
