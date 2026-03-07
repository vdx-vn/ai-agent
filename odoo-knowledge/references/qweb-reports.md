# QWeb Reports Reference

## Report Basics

### Report Declaration

```xml
<!-- report/my_report.xml -->
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data>
        <!-- QWeb Report -->
        <report
            id="report_my_model"
            model="my.model"
            string="My Model Report"
            report_type="qweb-pdf"
            name="my_module.report_my_model_template"
            file="my_module.report_my_model_template"
            print_report_name="'My Model - %s' % (object.name or '')"
        />

        <!-- Excel Report (requires spreadsheet addon) -->
        <report
            id="report_my_model_xlsx"
            model="my.model"
            string="My Model Excel"
            report_type="xlsx"
            name="my_module.report_my_model_xlsx"
            file="my_module.report_my_model_xlsx"
        />
    </data>
</odoo>
```

### Report Attributes

| Attribute | Description | Example |
|-----------|-------------|---------|
| `id` | Unique identifier | `report_my_model` |
| `model` | Source model | `sale.order` |
| `string` | Display name | `Sales Order` |
| `report_type` | Output format | `qweb-pdf`, `qweb-html`, `xlsx` |
| `name` | Template ID | `module.template_name` |
| `print_report_name` | Dynamic filename | `object.name` |
| `attachment` | Save attachment | `True` or expression |
| `attachment_use` | Use saved attachment | `True/False` |
| `binding_model_id` | Show in More menu | model ref |
| `groups` | Restrict by groups | `base.group_user` |

## QWeb Report Templates

### Basic PDF Template

```xml
<!-- views/report_templates.xml -->
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <template id="report_my_model_template">
        <t t-call="web.external_layout">
            <div class="page">
                <!-- Header -->
                <div class="row mb32">
                    <div class="col-6">
                        <h2>My Model Report</h2>
                    </div>
                    <div class="col-6 text-right">
                        <span t-field="doc.date"/>
                    </div>
                </div>

                <!-- Content -->
                <div class="row mb16">
                    <div class="col-6">
                        <strong>Customer:</strong>
                        <span t-field="doc.partner_id.name"/>
                    </div>
                </div>

                <!-- Lines Table -->
                <table class="table table-sm">
                    <thead>
                        <tr>
                            <th>Description</th>
                            <th class="text-right">Quantity</th>
                            <th class="text-right">Price</th>
                            <th class="text-right">Total</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr t-foreach="doc.line_ids" t-as="line">
                            <td><span t-field="line.name"/></td>
                            <td class="text-right"><span t-field="line.quantity"/></td>
                            <td class="text-right"><span t-field="line.price_unit"/></td>
                            <td class="text-right"><span t-field="line.amount"/></td>
                        </tr>
                    </tbody>
                </table>

                <!-- Totals -->
                <div class="row">
                    <div class="col-8"></div>
                    <div class="col-4">
                        <table class="table table-sm">
                            <tr>
                                <td class="text-right"><strong>Total:</strong></td>
                                <td class="text-right">
                                    <span t-field="doc.amount_total" t-options='{"widget": "monetary"}'/>
                                </td>
                            </tr>
                        </table>
                    </div>
                </div>
            </div>
        </t>
    </template>
</odoo>
```

### External Layout Variants

```xml
<!-- Standard layout with header/footer -->
<template id="report_my_model">
    <t t-call="web.external_layout">
        <div class="page">
            <!-- Content here -->
        </div>
    </t>
</template>

<!-- Minimal layout (no header/footer) -->
<template id="report_my_model_minimal">
    <t t-call="web.external_layout_clean">
        <div class="page">
            <!-- Minimal content -->
        </div>
    </t>
</template>

<!-- Boxed layout (borders) -->
<template id="report_my_model_boxed">
    <t t-call="web.external_layout_boxed">
        <div class="page">
            <!-- Boxed content -->
        </div>
    </t>
</template>

<!-- Background with background image -->
<template id="report_my_model_background">
    <t t-call="web.external_layout_background">
        <div class="page">
            <!-- Content over background -->
        </div>
    </t>
</template>
```

## QWeb Directives

### t-field - Field Rendering

```xml
<!-- Text field -->
<span t-field="doc.name"/>

<!-- Date with format -->
<span t-field="doc.date" t-options='{"format": "dd/MM/YYYY"}'/>

<!-- Monetary field with currency -->
<span t-field="doc.amount_total" t-options='{"widget": "monetary", "display_currency": "doc.currency_id"'}/>

<!-- Selection field (translatable) -->
<span t-field="doc.state"/>

<!-- Many2one relation -->
<span t-field="doc.partner_id.name"/>

<!-- Many2one with display_name fallback -->
<t t-if="doc.partner_id">
    <span t-field="doc.partner_id.display_name"/>
</t>
<t t-else="">
    <span class="text-muted">No Customer</span>
</t>
```

### t-esc - Escaped Content

```xml
<!-- Simple variable -->
<p t-esc="title"/>

<!-- Dictionary value -->
<p t-esc="my_dict['key']"/>

<!-- Computed value -->
<p t-esc="any_var * 100"/>

<!-- With raw option (no HTML escaping) -->
<p t-esc="html_content" t-options='{"widget": "html"}'/>
```

### t-if, t-elif, t-else - Conditionals

```xml
<!-- Simple condition -->
<div t-if="doc.state == 'draft'">
    This is a draft document
</div>

<!-- If/Else -->
<div t-if="doc.amount_total > 1000">
    High value order
</div>
<div t-else="">
    Regular order
</div>

<!-- Multiple conditions -->
<div t-if="doc.state == 'draft'">
    Draft
</div>
<div t-elif="doc.state == 'confirmed'">
    Confirmed
</div>
<div t-else="">
    Other
</div>

<!-- Negation -->
<div t-if="not doc.line_ids">
    No lines
</div>
```

### t-foreach, t-as - Loops

```xml
<!-- Basic loop -->
<ul>
    <li t-foreach="doc.line_ids" t-as="line">
        <span t-esc="line.name"/>
    </li>
</ul>

<!-- With index -->
<table>
    <tr t-foreach="doc.line_ids" t-as="line">
        <td><t t-esc="line_index + 1"/></td>  <!-- 0-based index -->
        <td><t t-esc="line.name"/></td>
    </tr>
</table>

<!-- With first/last -->
<div t-foreach="doc.line_ids" t-as="line">
    <span t-if="line_first">First line</span>
    <span t-esc="line.name"/>
    <span t-if="line_last">Last line</span>
</div>

<!-- Loop over dictionary -->
<dl t-foreach="doc.data" t-as="value">
    <dt><t t-esc="value_key"/></dt>
    <dd><t t-esc="value_value"/></dd>
</dl>

<!-- Loop with enumeration -->
<div t-foreach="range(5)" t-as="i">
    Number: <t t-esc="i"/>
</div>
```

### t-set - Set Variables

```xml
<!-- Set variable -->
<t t-set="total" t-value="0"/>

<!-- Set with computed value -->
<t t-set="company_name" t-value="doc.company_id.name"/>

<!-- Use variable -->
<span t-esc="company_name"/>

<!-- Set in loop -->
<t t-set="line_total" t-value="0"/>
<div t-foreach="doc.line_ids" t-as="line">
    <t t-set="line_total" t-value="line_total + line.amount"/>
</div>
Total: <span t-esc="line_total"/>

<!-- Safe rendering (won't escape) -->
<t t-set="html" t-value="'<b>Bold</b>'"/>
<div t-raw="html"/>
```

### t-call - Template Reuse

```xml
<!-- Define reusable template -->
<template id="report_address_block">
    <div class="address">
        <t t-if="partner">
            <span t-field="partner.name"/>
            <br/>
            <span t-field="partner.street"/>
            <br/>
            <span t-field="partner.city"/>
        </t>
    </div>
</template>

<!-- Call it -->
<div t-call="my_module.report_address_block">
    <t t-set="partner" t-value="doc.partner_id"/>
</div>

<!-- Or call with object -->
<t t-call="my_module.report_address_block">
    <t t-set="partner" t-value="doc.partner_id"/>
</t>

<!-- Built-in layouts -->
<t t-call="web.external_layout">
    <div class="page">
        Content
    </div>
</t>
```

### t-att - Attributes

```xml
<!-- Dynamic class -->
<div t-att-class="'bg-' + (doc.state == 'done' and 'success' or 'warning')">
    Content
</div>

<!-- Multiple classes -->
<div t-attf-class="card #{doc.state == 'done' ? 'bg-success' : 'bg-warning'}">
    Content
</div>

<!-- Dynamic style -->
<span t-att-style="'color:' + (doc.amount_total > 0 and 'green' or 'red')">
    Amount
</span>

<!-- Dynamic ID -->
<div t-att-id="'line_' + str(line.id)">
    Line content
</div>

<!-- Data attributes -->
<div t-att-data-id="doc.id" t-att-data-state="doc.state">
    Data
</div>

<!-- Formatted attributes (Python format style) -->
<a t-attf-href="/my/page/#{doc.id}">
    Link
</a>
```

## Dynamic Reports

### Conditional Attachment

```xml
<report
    id="report_my_model"
    model="my.model"
    string="My Model Report"
    report_type="qweb-pdf"
    name="my_module.report_my_model_template"
    attachment="(object.state == 'done') and ('MyModel-%s.pdf' % object.id) or None"
    attachment_use="True"
/>
```

### Multi-language Reports

```python
# In model
class MyModel(models.Model):
    _name = 'my.model'

    def action_report(self):
        """Print report in specific language"""
        self.ensure_one()

        # Force language for report
        lang = self.partner_id.lang or 'en_US'
        return self.with_context(lang=lang).env.ref('my_module.report_my_model').report_action(self)
```

### Custom Paper Format

```xml
<record id="paperformat_my_custom" model="report.paperformat">
    <field name="name">My Custom Paper</field>
    <field name="default" eval="True"/>
    <field name="format">custom</field>
    <field name="page_height">297</field>
    <field name="page_width">210</field>
    <field name="orientation">Portrait</field>
    <field name="margin_top">40</field>
    <field name="margin_bottom">20</field>
    <field name="margin_left">7</field>
    <field name="margin_right">7</field>
    <field name="header_line" eval="False"/>
    <field name="header_spacing">35</field>
    <field name="dpi">90</field>
</record>

<!-- Link report to paper format -->
<record id="report_my_model_paperformat" model="ir.actions.report">
    <field name="paperformat_id" ref="paperformat_my_custom"/>
</record>
```

## Barcode in Reports

```xml
<!-- QR Code -->
<img t-att-src="'/report/barcode/QR/%s?width=100&amp;height=100' % doc.code"/>

<!-- Code128 -->
<img t-att-src="'/report/barcode/Code128/%s?width=200&amp;height=50' % doc.code"/>

<!-- EAN13 -->
<img t-att-src="'/report/barcode/EAN13/%s?width=200&amp;height=100' % doc.ean13"/>

<!-- Custom barcode -->
<img t-att-src="'/report/barcode/?type=%s&amp;value=%s&amp;width=%s&amp;height=%s' % ('QR', doc.code, 100, 100)"/>
```

## Images in Reports

```xml
<!-- From URL -->
<img src="/my_module/static/src/img/logo.png" style="height: 50px;"/>

<!-- From binary field -->
<img t-att-src="'data:image/png;base64,' + doc.image.decode('utf-8')"/>

<!-- From company logo -->
<img t-att-src="'data:image/png;base64,' + doc.company_id.logo"/>
```

## Best Practices

### 1. Use external_layout for consistency

```xml
<!-- Good -->
<template id="my_report">
    <t t-call="web.external_layout">
        <div class="page">
            Content
        </div>
    </t>
</template>

<!-- Not recommended (no header/footer) -->
<template id="my_report_bad">
    <div class="page">
        Content
    </div>
</template>
```

### 2. Use Bootstrap classes for styling

```xml
<!-- Odoo includes Bootstrap -->
<div class="row">
    <div class="col-6">Left</div>
    <div class="col-6">Right</div>
</div>

<!-- Table styles -->
<table class="table table-sm table-bordered">
    <!-- Table content -->
</table>

<!-- Utility classes -->
<div class="text-right">Right aligned</div>
<div class="text-center">Center</div>
<div class="mt-4">Top margin</div>
```

### 3. Handle empty values gracefully

```xml
<!-- Good -->
<t t-if="doc.partner_id">
    <span t-field="doc.partner_id.name"/>
</t>
<t t-else="">
    <span class="text-muted">No customer</span>
</t>

<!-- Or with default -->
<span t-field="doc.partner_id.name" t-esc="doc.partner_id.name or '-'"/>
```

### 4. Use monetary widget for amounts

```xml
<!-- Good -->
<span t-field="doc.amount_total" t-options='{"widget": "monetary", "display_currency": "doc.currency_id"'}/>

<!-- Less ideal -->
<span t-esc="doc.amount_total"/>  <!-- No currency symbol, no formatting -->
```

## References

- QWeb: https://www.odoo.com/documentation/18.0/developer/reference/backend/qweb.html
- Reports: https://www.odoo.com/documentation/18.0/developer/reference/backend/reports.html
- Base reports: https://github.com/odoo/odoo/blob/18.0/addons/base/report/
