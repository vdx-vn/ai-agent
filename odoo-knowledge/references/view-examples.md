# View Examples Reference

## View Types

### Tree View (List)
```xml
<record id="view_order_list" model="ir.ui.view">
    <field name="name">sale.order.list</field>
    <field name="model">sale.order</field>
    <field name="arch" type="xml">
        <list string="Sales Orders" multi_edit="1">
            <field name="name" string="Order Number"/>
            <field name="date_order"/>
            <field name="partner_id"/>
            <field name="amount_total" sum="Total"/>
            <field name="state" widget="badge" decoration-success="state=='sale'"
                   decoration-info="state=='draft'" decoration-muted="state=='cancel'"/>
            <button name="action_confirm" string="Confirm" type="object"
                    icon="fa-check" attrs="{'invisible': [('state', '!=', 'draft')]}"/>
        </list>
    </field>
</record>
```

### Form View
```xml
<record id="view_order_form" model="ir.ui.view">
    <field name="name">sale.order.form</field>
    <field name="model">sale.order</field>
    <field name="arch" type="xml">
        <form string="Sales Order">
            <header>
                <button name="action_confirm" string="Confirm Sale" type="object"
                        class="btn-primary" attrs="{'invisible': [('state', '!=', 'draft')]}"/>
                <button name="action_cancel" string="Cancel" type="object"
                        attrs="{'invisible': [('state', 'in', ('done', 'cancel'))]}"/>
                <field name="state" widget="statusbar" statusbar_visible="draft,sent,sale,done"/>
            </header>
            <sheet>
                <div class="oe_title">
                    <h1>
                        <field name="name" readonly="1"/>
                    </h1>
                </div>
                <group>
                    <group>
                        <field name="partner_id" required="1"/>
                        <field name="date_order"/>
                    </group>
                    <group>
                        <field name="currency_id"/>
                        <field name="company_id" groups="base.group_multi_company"/>
                    </group>
                </group>
                <notebook>
                    <page string="Order Lines">
                        <field name="order_line">
                            <list editable="bottom">
                                <field name="product_id"/>
                                <field name="name"/>
                                <field name="product_uom_qty"/>
                                <field name="price_unit"/>
                                <field name="price_subtotal" readonly="1"/>
                            </list>
                        </field>
                    </page>
                    <page string="Other Info">
                        <group>
                            <field name="note"/>
                        </group>
                    </page>
                </notebook>
            </sheet>
            <div class="oe_chatter">
                <field name="message_follower_ids"/>
                <field name="activity_ids"/>
                <field name="message_ids"/>
            </div>
        </form>
    </field>
</record>
```

### Search View
```xml
<record id="view_order_search" model="ir.ui.view">
    <field name="name">sale.order.search</field>
    <field name="model">sale.order</field>
    <field name="arch" type="xml">
        <search string="Sales Orders">
            <field name="name" string="Order Number" filter_domain="['|', ('name', 'ilike', self), ('client_order_ref', 'ilike', self)]"/>
            <field name="partner_id"/>
            <field name="user_id"/>
            <field name="date_order"/>
            <filter name="draft" string="Draft" domain="[('state', '=', 'draft')]"/>
            <filter name="sales" string="Sales Order" domain="[('state', '=', 'sale')]"/>
            <separator/>
            <filter name="my_orders" string="My Orders" domain="[('user_id', '=', uid)]"/>
            <filter name="today" string="Today" domain="[('date_order', '>=', (context_today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d'))]"/>
            <group expand="0" string="Group By">
                <filter name="partner" string="Customer" context="{'group_by': 'partner_id'}"/>
                <filter name="state" string="State" context="{'group_by': 'state'}"/>
                <filter name="salesperson" string="Salesperson" context="{'group_by': 'user_id'}"/>
            </group>
        </search>
    </field>
</record>
```

### Kanban View
```xml
<record id="view_order_kanban" model="ir.ui.view">
    <field name="name">sale.order.kanban</field>
    <field name="model">sale.order</field>
    <field name="arch" type="xml">
        <kanban default_group_by="state" class="o_kanban_mobile">
            <field name="name"/>
            <field name="partner_id"/>
            <field name="amount_total"/>
            <templates>
                <t t-name="kanban-box">
                    <div class="oe_kanban_card">
                        <div class="oe_kanban_content">
                            <strong>
                                <field name="name"/>
                            </strong>
                            <div class="text-muted">
                                <field name="partner_id"/>
                            </div>
                            <div class="oe_kanban_footer">
                                <span class="text-right">
                                    <field name="amount_total" widget="monetary"/>
                                </span>
                            </div>
                        </div>
                    </div>
                </t>
            </templates>
        </kanban>
    </field>
</record>
```

### Pivot and Graph Views
```xml
<!-- Pivot View -->
<record id="view_sale_order_pivot" model="ir.ui.view">
    <field name="name">sale.order.pivot</field>
    <field name="model">sale.order</field>
    <field name="arch" type="xml">
        <pivot string="Sales Analysis">
            <field name="partner_id" type="row"/>
            <field name="date_order" interval="month" type="col"/>
            <field name="amount_total" type="measure"/>
        </pivot>
    </field>
</record>

<!-- Graph View -->
<record id="view_sale_order_graph" model="ir.ui.view">
    <field name="name">sale.order.graph</field>
    <field name="model">sale.order</field>
    <field name="arch" type="xml">
        <graph string="Sales Analysis" type="bar">
            <field name="date_order" interval="month" type="row"/>
            <field name="amount_total" type="measure"/>
        </graph>
    </field>
</record>
```

### Calendar View
```xml
<record id="view_event_calendar" model="ir.ui.view">
    <field name="name">event.calendar</field>
    <field name="model">event.event</field>
    <field name="arch" type="xml">
        <calendar string="Events" date_start="date_begin" date_end="date_end"
                  color="user_id" mode="month">
            <field name="name"/>
            <field name="user_id"/>
        </calendar>
    </field>
</record>
```

## View Inheritance (XPath)

### Replace Element
```xml
<record id="view_order_form_inherit" model="ir.ui.view">
    <field name="name">sale.order.form.inherit</field>
    <field name="model">sale.order</field>
    <field name="inherit_id" ref="sale.view_order_form"/>
    <field name="arch" type="xml">
        <!-- Replace field -->
        <xpath expr="//field[@name='client_order_ref']" position="replace">
            <field name="client_order_ref" required="1"/>
        </xpath>
    </field>
</record>
```

### Insert After/Before
```xml
<record id="view_order_form_inherit" model="ir.ui.view">
    <field name="name">sale.order.form.inherit</field>
    <field name="model">sale.order</field>
    <field name="inherit_id" ref="sale.view_order_form"/>
    <field name="arch" type="xml">
        <!-- Insert after -->
        <xpath expr="//field[@name='partner_id']" position="after">
            <field name="delivery_address_id"/>
        </xpath>
        <!-- Or use shorthand -->
        <field name="delivery_address_id" position="after">
            <field name="warehouse_id"/>
        </field>
    </field>
</record>
```

### Insert Inside
```xml
<record id="view_order_form_inherit" model="ir.ui.view">
    <field name="inherit_id" ref="sale.view_order_form"/>
    <field name="arch" type="xml">
        <xpath expr="//sheet" position="inside">
            <div class="oe_edit_only">
                <field name="note" placeholder="Internal notes..."/>
            </div>
        </xpath>
    </field>
</record>
```

### Add Page to Notebook
```xml
<record id="view_order_form_inherit" model="ir.ui.view">
    <field name="inherit_id" ref="sale.view_order_form"/>
    <field name="arch" type="xml">
        <xpath expr="//notebook/page[1]" position="after">
            <page string="Extra Info">
                <group>
                    <field name="custom_field"/>
                </group>
            </page>
        </xpath>
    </field>
</record>
```

### Add Button to Header
```xml
<record id="view_order_form_inherit" model="ir.ui.view">
    <field name="inherit_id" ref="sale.view_order_form"/>
    <field name="arch" type="xml">
        <xpath expr="//header" position="inside">
            <button name="action_custom" string="Custom Action" type="object"
                    class="btn-secondary" attrs="{'invisible': [('state', '!=', 'draft')]}"/>
        </xpath>
    </field>
</record>
```

## Actions and Menus

### Window Action
```xml
<record id="action_sale_order" model="ir.actions.act_window">
    <field name="name">Sales Orders</field>
    <field name="type">ir.actions.act_window</field>
    <field name="res_model">sale.order</field>
    <field name="view_mode">tree,form,kanban,pivot,graph</field>
    <field name="domain">[]</field>
    <field name="context">{'default_state': 'draft'}</field>
    <field name="search_view_id" ref="view_order_search"/>
    <field name="help" type="html">
        <p class="o_view_nocontent_smiling_face">
            Create your first sales order!
        </p>
    </field>
</record>
```

### Menu Items
```xml
<!-- Top Level Menu -->
<menuitem id="menu_sale_root" name="Sales" sequence="10"/>

<!-- Sub Menu -->
<menuitem id="menu_sale_order" name="Orders"
          parent="menu_sale_root" action="action_sale_order"
          sequence="1"/>

<!-- Deep Sub Menu -->
<menuitem id="menu_sale_order_report" name="Reports"
          parent="menu_sale_root" action="action_sale_report"
          sequence="10"/>
```

### Server Action
```xml
<record id="action_mark_done" model="ir.actions.server">
    <field name="name">Mark as Done</field>
    <field name="model_id" ref="model_sale_order"/>
    <field name="binding_model_id" ref="model_sale_order"/>
    <field name="state">code</field>
    <field name="code">
for record in records:
    record.action_done()
    </field>
</record>
```

## References
- Views: https://www.odoo.com/documentation/18.0/developer/reference/backend/views.html
- Actions: https://www.odoo.com/documentation/18.0/developer/reference/backend/actions.html
- Base views: https://github.com/odoo/odoo/blob/18.0/addons/base/views/base_views.xml
