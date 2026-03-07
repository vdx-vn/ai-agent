# OWL Framework and Frontend Reference

## OWL Components (Odoo 15+)

### Basic Component Structure

```javascript
// static/src/js/my_widget.js
/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class MyWidget extends Component {
    static template = "my_module.MyWidget";

    setup() {
        this.state = useState({
            counter: 0,
            message: "Hello",
        });
    }

    increment() {
        this.state.counter++;
    }

    get displayMessage() {
        return `${this.state.message} (${this.state.counter})`;
    }
}
```

### Component Registration

```javascript
// static/src/js/my_component_registry.js
/** @odoo-module **/

import { registry } from "@web/core/registry";
import { MyWidget } from "./my_widget";

export const myWidgetService = {
    dependencies: ["action"],
    start(env, { action }) {
        return {
            // Register as action
            name: "my_widget_action",
            action: (context) => {
                action.doAction({
                    type: "ir.actions.client",
                    tag: "my_widget",
                });
            },
        };
    },
};

registry.category("actions").add("my_widget", MyWidget);
```

### Templates (QWeb in OWL)

```xml
<!-- static/src/xml/my_widget.xml -->
<?xml version="1.0" encoding="UTF-8"?>
<templates xml:space="preserve">
    <t t-name="my_module.MyWidget" owl="1">
        <div class="o_my_widget">
            <h1 t-esc="props.title"/>
            <p t-esc="state.displayMessage"/>
            <button t-on-click="increment">
                Increment
            </button>
            <t t-if="state.counter > 10">
                <span class="badge bg-danger">High count!</span>
            </t>
        </div>
    </t>
</templates>
```

## Fields and Widgets

### Custom Field Widget

```javascript
// static/src/js/field_custom_widget.js
/** @odoo-module **/

import { registry } from "@web/core/registry";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { useService } from "@web/core/utils/hooks";

const { Component } = owl;

export class CustomFieldWidget extends Component {
    static template = "my_module.CustomFieldWidget";
    static props = {
        ...standardFieldProps,
    };

    setup() {
        this.notification = useService("notification");
    }

    get value() {
        return this.props.value;
    }

    get readonly() {
        return this.props.readonly;
    }

    onClick() {
        this.notification.add("Clicked!", { type: "success" });
    }
}

registry.category("fields").add("custom_field", CustomFieldWidget);
```

```xml
<!-- static/src/xml/field_widget.xml -->
<?xml version="1.0" encoding="UTF-8"?>
<templates xml:space="preserve">
    <t t-name="my_module.CustomFieldWidget" owl="1">
        <span class="o_custom_field" t-on-click="onClick">
            <t t-if="props.value">
                <i class="fa fa-check text-success"/>
            </t>
            <t t-else="">
                <i class="fa fa-times text-danger"/>
            </t>
        </span>
    </t>
</templates>
```

### Using Custom Widget in Views

```xml
<field name="active" widget="custom_field"/>
```

## Views

### Custom View Definition

```javascript
// static/src/js/custom_view.js
/** @odoo-module **/

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Layout } from "@web/search/layout";
import { useModelWithSampleData } from "@web/model/model";

const { Component, useState } = owl;

export class CustomViewController extends Component {
    static template = "my_module.CustomView";
    static components = { Layout };

    setup() {
        this.orm = useService("orm");
        this.actionService = useService("action");
        this.state = useState({
            records: [],
        });

        this.model = useModelWithSampleData(...);
        this.loadRecords();
    }

    async loadRecords() {
        const records = await this.orm.searchRead(
            "my.model",
            [],
            ["name", "date", "state"],
            { limit: 80 }
        );
        this.state.records = records;
    }

    openRecord(record) {
        this.actionService.doAction({
            type: "ir.actions.act_window",
            res_model: "my.model",
            res_id: record.id,
            views: [[false, "form"]],
        });
    }
}

registry.category("views").add("custom_view", {
    Controller: CustomViewController,
    display_name: "Custom View",
    icon: "fa-list",
    isCompatible: ( viewType, viewInfo ) => {
        return viewInfo.type === "custom_view";
    },
});
```

### Kanban View

```javascript
// static/src/js/kanban_renderer.js
/** @odoo-module **/

import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";

export class KanbanRenderer extends Component {
    static template = "my_module.KanbanView";
    static props = ["records", "archInfo"];

    get groupedRecords() {
        const groups = {};
        for (const record of this.props.records) {
            const group = record.group_value || "Uncategorized";
            if (!groups[group]) {
                groups[group] = [];
            }
            groups[group].push(record);
        }
        return groups;
    }

    onRecordClick(record) {
        this.trigger("record-selected", { record });
    }
}

registry.category("kanban_renderers").add("custom_kanban", KanbanRenderer);
```

## Actions

### Client Actions

```javascript
// static/src/js/client_action.js
/** @odoo-module **/

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

const { Component, useState } = owl;

export class ClientAction extends Component {
    static template = "my_module.ClientAction";

    setup() {
        this.orm = useService("orm");
        this.dialog = useService("dialog");
        this.action = useService("action");

        this.state = useState({
            data: [],
        });

        this.loadData();
    }

    async loadData() {
        this.state.data = await this.orm.searchRead(
            "my.model",
            [],
            ["name", "value"]
        );
    }

    openDialog() {
        this.dialog.add(MyDialog, {
            confirm: () => this.loadData(),
        });
    }
}

// Register the client action
registry.category("actions").add("my_client_action_tag", ClientAction);
```

```xml
<!-- Define the action in Python/XML -->
<record id="action_my_client" model="ir.actions.client">
    <field name="name">My Client Action</field>
    <field name="tag">my_client_action_tag</field>
</record>
```

## Services

### Custom Service

```javascript
// static/src/js/my_service.js
/** @odoo-module **/

import { registry } from "@web/core/registry";

export const myService = {
    dependencies: ["orm", "notification"],

    start(env, { orm, notification }) {
        let data = null;

        return {
            async loadData() {
                data = await orm.searchRead("my.model", [], ["name"]);
                return data;
            },

            notify(message) {
                notification.add(message, { type: "success" });
            },

            getData() {
                return data;
            },
        };
    },
};

registry.category("services").add("myService", myService);
```

### Using Service in Component

```javascript
/** @odoo-module **/

import { Component } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export class MyComponent extends Component {
    setup() {
        this.myService = useService("myService");
        this.orm = useService("orm");
        this.rpc = useService("rpc");
        this.dialog = useService("dialog");
        this.notification = useService("notification");
        this.action = useService("action");
        this.router = useService("router");
    }

    async onClick() {
        const data = await this.myService.loadData();
        this.myService.notify("Data loaded!");
    }
}
```

## Assets

### Asset Bundle Definition

```xml
<!-- views/assets.xml -->
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data>
        <!-- Backend assets -->
        <template id="assets_backend" inherit_id="web.assets_backend" name="My Module Assets">
            <xpath expr="." position="inside">
                <!-- JavaScript -->
                <script type="text/javascript" src="/my_module/static/src/js/my_widget.js"/>
                <script type="text/javascript" src="/my_module/static/src/js/custom_view.js"/>

                <!-- CSS -->
                <link rel="stylesheet" href="/my_module/static/src/css/my_style.css"/>
            </xpath>
        </template>

        <!-- Frontend assets -->
        <template id="assets_frontend" inherit_id="web.assets_frontend" name="My Module Frontend">
            <xpath expr="." position="inside">
                <script type="text/javascript" src="/my_module/static/src/js/frontend.js"/>
                <link rel="stylesheet" href="/my_module/static/src/css/frontend.css"/>
            </xpath>
        </template>

        <!-- QWeb templates -->
        <template id="qweb_assets" inherit_id="web.assets_qweb" name="My Module QWeb">
            <xpath expr="." position="inside">
                <script type="text/javascript" src="/my_module/static/src/xml/my_templates.xml"/>
            </xpath>
        </template>
    </data>
</odoo>
```

### Loading Assets in Manifest

```python
# __manifest__.py
'assets': {
    'web.assets_backend': [
        'my_module/static/src/js/*.js',
        'my_module/static/src/xml/*.xml',
        'my_module/static/src/css/*.css',
    ],
    'web.assets_frontend': [
        'my_module/static/src/js/frontend.js',
    ],
},
'qweb': [
    'my_module/static/src/xml/*.xml',
],
```

## Common Frontend Patterns

### Dialog/Modal

```javascript
/** @odoo-module **/

import { Component } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { _t } from "@web/core/l10n/translation";

export class MyDialog extends Component {
    static template = "my_module.MyDialog";
    static components = { Dialog };

    static props = {
        confirm: { type: Function, optional: true },
        cancel: { type: Function, optional: true },
    };

    setup() {
        this.state = {
            value: "",
        };
    }

    save() {
        if (this.props.confirm) {
            this.props.confirm(this.state.value);
        }
        this.props.close();
    }
}

// Usage
// In component:
this.dialog.add(MyDialog, {
    confirm: (value) => console.log("Got:", value),
});
```

### Notification

```javascript
// Using notification service
setup() {
    this.notification = useService("notification");
}

showNotification() {
    // Success
    this.notification.add("Success!", { type: "success" });

    // Warning
    this.notification.add("Warning!", { type: "warning" });

    // Danger
    this.notification.add("Error!", { type: "danger" });

    // With sticky
    this.notification.add("Important!", { sticky: true });
}
```

### RPC Calls

```javascript
setup() {
    this.orm = useService("orm");
    this.rpc = useService("rpc");
}

// ORM methods
async loadData() {
    // Search read
    const records = await this.orm.searchRead(
        "my.model",
        [["state", "=", "draft"]],
        ["name", "date"]
    );

    // Call method
    const result = await this.orm.call(
        "my.model",
        "my_method",
        [[1, 2, 3]],  // ids
        { context: {} }
    );

    // Create
    const id = await this.orm.create("my.model", [{
        name: "Test",
        value: 100,
    }]);

    // Write
    await this.orm.write("my.model", [id], { value: 200 });

    // Unlink
    await this.orm.unlink("my.model", [id]);
}

// Generic RPC
async callCustomEndpoint() {
    const result = await this.rpc(
        "/my/custom/endpoint",
        { params: "value" }
    );
}
```

### Reactive State

```javascript
import { Component, useState, useRef } from "@odoo/owl";

export class ReactiveComponent extends Component {
    setup() {
        // Reactive state
        this.state = useState({
            count: 0,
            items: [],
        });

        // Template refs
        this.inputRef = useRef("input");
    }

    increment() {
        this.state.count++;
    }

    addItem() {
        this.state.items.push({
            id: Date.now(),
            name: this.inputRef.el.value,
        });
        this.state.count = this.state.items.length;
    }

    get hasItems() {
        return this.state.items.length > 0;
    }
}
```

## References

- OWL Framework: https://github.com/odoo/owl
- Odoo JS Docs: https://www.odoo.com/documentation/18.0/developer/reference/frontend.html
- Web Client: https://github.com/odoo/odoo/tree/18.0/addons/web/static/src
