# NotebookLM MCP Tools Reference

Complete reference for all NotebookLM MCP tools available in this skill.

## Authentication

### `refresh_auth`
Refresh auth tokens from disk or run headless re-authentication.

**Usage:**
```python
mcp__notebooklm-mcp__refresh_auth()
```

**When to use:** After running `notebooklm-mcp-auth` CLI or when getting auth errors.

---

## Notebook Management

### `notebook_create`
Create a new notebook.

**Parameters:**
- `title` (optional): Notebook title

**Usage:**
```python
mcp__notebooklm-mcp__notebook_create(title="My Project")
```

### `notebook_list`
List all notebooks.

**Parameters:**
- `max_results` (optional, default=100): Maximum number of notebooks to return

**Usage:**
```python
mcp__notebooklm-mcp__notebook_list(max_results=50)
```

### `notebook_get`
Get notebook details with sources.

**Parameters:**
- `notebook_id` (required): Notebook UUID

**Usage:**
```python
mcp__notebooklm-mcp__notebook_get(notebook_id="notebook-uuid")
```

### `notebook_describe`
Get AI-generated notebook summary with suggested topics.

**Parameters:**
- `notebook_id` (required): Notebook UUID

**Returns:** summary (markdown), suggested_topics list

**Usage:**
```python
mcp__notebooklm-mcp__notebook_describe(notebook_id="notebook-uuid")
```

### `notebook_rename`
Rename a notebook.

**Parameters:**
- `notebook_id` (required): Notebook UUID
- `new_title` (required): New title

**Usage:**
```python
mcp__notebooklm-mcp__notebook_rename(notebook_id="notebook-uuid", new_title="New Title")
```

### `notebook_delete`
Delete notebook permanently. **IRREVERSIBLE.**

**Parameters:**
- `notebook_id` (required): Notebook UUID
- `confirm` (required): Must be True after user approval

**Usage:**
```python
# First ask user for confirmation
mcp__notebooklm-mcp__notebook_delete(notebook_id="notebook-uuid", confirm=True)
```

---

## Adding Sources

### `notebook_add_text`
Add pasted text as source.

**Parameters:**
- `notebook_id` (required): Notebook UUID
- `text` (required): Text content to add
- `title` (optional, default="Pasted Text"): Display title

**Usage:**
```python
mcp__notebooklm-mcp__notebook_add_text(
    notebook_id="notebook-uuid",
    text="This is the text content to add",
    title="My Notes"
)
```

### `notebook_add_url`
Add URL (website or YouTube) as source.

**Parameters:**
- `notebook_id` (required): Notebook UUID
- `url` (required): URL to add

**Usage:**
```python
mcp__notebooklm-mcp__notebook_add_url(
    notebook_id="notebook-uuid",
    url="https://example.com/documentation"
)
```

### `notebook_add_drive`
Add Google Drive document as source.

**Parameters:**
- `notebook_id` (required): Notebook UUID
- `document_id` (required): Drive document ID (from URL)
- `title` (required): Display title
- `doc_type` (optional, default="doc"): `doc`|`slides`|`sheets`|`pdf`

**Usage:**
```python
# URL: https://docs.google.com/document/d/123abc/edit
mcp__notebooklm-mcp__notebook_add_drive(
    notebook_id="notebook-uuid",
    document_id="123abc",
    title="Project Documentation",
    doc_type="doc"
)
```

---

## Querying & Research

### `notebook_query`
Ask AI about EXISTING sources in notebook. **NOT for finding new sources.**

**Parameters:**
- `notebook_id` (required): Notebook UUID
- `query` (required): Question to ask
- `source_ids` (optional, default=all): Source IDs to query
- `conversation_id` (optional): For follow-up questions

**Usage:**
```python
# First question
mcp__notebooklm-mcp__notebook_query(
    notebook_id="notebook-uuid",
    query="What are the key features of the approval workflow?"
)

# Follow-up
mcp__notebooklm-mcp__notebook_query(
    notebook_id="notebook-uuid",
    query="Tell me more about the second feature",
    conversation_id="conversation-id-from-previous-response"
)
```

### `research_start`
Deep research / fast research: Search web or Google Drive to FIND NEW sources.

**Parameters:**
- `query` (required): What to search for
- `source` (optional, default="web"): `web`|`drive`
- `mode` (optional, default="fast"): `fast` (~30s, ~10 sources) | `deep` (~5min, ~40 sources, web only)
- `notebook_id` (optional): Existing notebook (creates new if not provided)
- `title` (optional): Title for new notebook

**Workflow:** research_start → poll research_status → research_import

**Usage:**
```python
mcp__notebooklm-mcp__research_start(
    query="Odoo 18 purchase order promotions",
    source="web",
    mode="deep",
    notebook_id="notebook-uuid"
)
```

### `research_status`
Poll research progress. Blocks until complete or timeout.

**Parameters:**
- `notebook_id` (required): Notebook UUID
- `task_id` (optional): Research task ID to poll
- `poll_interval` (optional, default=30): Seconds between polls
- `max_wait` (optional, default=300): Max seconds to wait (0=single poll)
- `compact` (optional, default=True): Truncate report and limit sources

**Usage:**
```python
mcp__notebooklm-mcp__research_status(
    notebook_id="notebook-uuid",
    poll_interval=30,
    max_wait=300
)
```

### `research_import`
Import discovered sources into notebook. Call after research_status shows completed.

**Parameters:**
- `notebook_id` (required): Notebook UUID
- `task_id` (required): Research task ID
- `source_indices` (optional, default=all): Source indices to import

**Usage:**
```python
mcp__notebooklm-mcp__research_import(
    notebook_id="notebook-uuid",
    task_id="task-id-from-research"
)
```

---

## Source Management

### `source_list_drive`
List sources with types and Drive freshness status. Use before source_sync_drive.

**Parameters:**
- `notebook_id` (required): Notebook UUID

**Usage:**
```python
mcp__notebooklm-mcp__source_list_drive(notebook_id="notebook-uuid")
```

### `source_sync_drive`
Sync Drive sources with latest content. Call source_list_drive first.

**Parameters:**
- `source_ids` (required): Source UUIDs to sync
- `confirm` (required): Must be True after user approval

**Usage:**
```python
mcp__notebooklm-mcp__source_sync_drive(
    source_ids=["source-uuid-1", "source-uuid-2"],
    confirm=True
)
```

### `source_describe`
Get AI-generated source summary with keyword chips.

**Parameters:**
- `source_id` (required): Source UUID

**Returns:** summary (markdown with **bold** keywords), keywords list

**Usage:**
```python
mcp__notebooklm-mcp__source_describe(source_id="source-uuid")
```

### `source_get_content`
Get raw text content of a source (no AI processing). Faster than query.

**Parameters:**
- `source_id` (required): Source UUID

**Returns:** content (str), title (str), source_type (str), char_count (int)

**Usage:**
```python
mcp__notebooklm-mcp__source_get_content(source_id="source-uuid")
```

### `source_delete`
Delete source permanently. **IRREVERSIBLE.**

**Parameters:**
- `source_id` (required): Source UUID
- `confirm` (required): Must be True after user approval

**Usage:**
```python
mcp__notebooklm-mcp__source_delete(source_id="source-uuid", confirm=True)
```

---

## Chat Configuration

### `chat_configure`
Configure notebook chat settings.

**Parameters:**
- `notebook_id` (required): Notebook UUID
- `goal` (optional, default="default"): `default`|`learning_guide`|`custom`
- `custom_prompt` (optional): Required when goal=custom (max 10000 chars)
- `response_length` (optional, default="default"): `default`|`longer`|`shorter`

**Usage:**
```python
mcp__notebooklm-mcp__chat_configure(
    notebook_id="notebook-uuid",
    goal="learning_guide",
    response_length="longer"
)
```

---

## Artifact Generation (Require confirm=True)

All artifact tools require `confirm=True` after user approval.

### `audio_overview_create`
Generate audio overview.

**Parameters:**
- `notebook_id` (required): Notebook UUID
- `source_ids` (optional, default=all): Source IDs
- `format` (optional, default="deep_dive"): `deep_dive`|`brief`|`critique`|`debate`
- `length` (optional, default="default"): `short`|`default`|`long`
- `language` (optional, default="en"): BCP-47 code (en, es, fr, de, ja)
- `focus_prompt` (optional, default=""): Optional focus text
- `confirm` (required): Must be True

**Usage:**
```python
mcp__notebooklm-mcp__audio_overview_create(
    notebook_id="notebook-uuid",
    format="deep_dive",
    length="default",
    confirm=True
)
```

### `video_overview_create`
Generate video overview.

**Parameters:**
- `notebook_id` (required): Notebook UUID
- `source_ids` (optional, default=all): Source IDs
- `format` (optional, default="explainer"): `explainer`|`brief`
- `visual_style` (optional, default="auto_select"): `auto_select`|`classic`|`whiteboard`|`kawaii`|`anime`|`watercolor`|`retro_print`|`heritage`|`paper_craft`
- `language` (optional, default="en"): BCP-47 code
- `focus_prompt` (optional): Optional focus text
- `confirm` (required): Must be True

**Usage:**
```python
mcp__notebooklm-mcp__video_overview_create(
    notebook_id="notebook-uuid",
    visual_style="whiteboard",
    confirm=True
)
```

### `report_create`
Generate report.

**Parameters:**
- `notebook_id` (required): Notebook UUID
- `source_ids` (optional, default=all): Source IDs
- `report_format` (optional, default="Briefing Doc"): `Briefing Doc`|`Study Guide`|`Blog Post`|`Create Your Own`
- `custom_prompt` (optional): Required for "Create Your Own"
- `language` (optional, default="en"): BCP-47 code
- `confirm` (required): Must be True

**Usage:**
```python
mcp__notebooklm-mcp__report_create(
    notebook_id="notebook-uuid",
    report_format="Briefing Doc",
    confirm=True
)
```

### `slide_deck_create`
Generate slide deck.

**Parameters:**
- `notebook_id` (required): Notebook UUID
- `source_ids` (optional, default=all): Source IDs
- `format` (optional, default="detailed_deck"): `detailed_deck`|`presenter_slides`
- `length` (optional, default="default"): `short`|`default`
- `language` (optional, default="en"): BCP-47 code
- `focus_prompt` (optional): Optional focus text
- `confirm` (required): Must be True

**Usage:**
```python
mcp__notebooklm-mcp__slide_deck_create(
    notebook_id="notebook-uuid",
    format="detailed_deck",
    confirm=True
)
```

### `infographic_create`
Generate infographic.

**Parameters:**
- `notebook_id` (required): Notebook UUID
- `source_ids` (optional, default=all): Source IDs
- `orientation` (optional, default="landscape"): `landscape`|`portrait`|`square`
- `detail_level` (optional, default="standard"): `concise`|`standard`|`detailed`
- `language` (optional, default="en"): BCP-47 code
- `focus_prompt` (optional): Optional focus text
- `confirm` (required): Must be True

**Usage:**
```python
mcp__notebooklm-mcp__infographic_create(
    notebook_id="notebook-uuid",
    orientation="landscape",
    detail_level="standard",
    confirm=True
)
```

### `mind_map_create`
Generate and save mind map.

**Parameters:**
- `notebook_id` (required): Notebook UUID
- `source_ids` (optional, default=all): Source IDs
- `title` (optional, default="Mind Map"): Display title
- `confirm` (required): Must be True

**Usage:**
```python
mcp__notebooklm-mcp__mind_map_create(
    notebook_id="notebook-uuid",
    title="Project Mind Map",
    confirm=True
)
```

### `flashcards_create`
Generate flashcards.

**Parameters:**
- `notebook_id` (required): Notebook UUID
- `source_ids` (optional, default=all): Source IDs
- `difficulty` (optional, default="medium"): `easy`|`medium`|`hard`
- `confirm` (required): Must be True

**Usage:**
```python
mcp__notebooklm-mcp__flashcards_create(
    notebook_id="notebook-uuid",
    difficulty="medium",
    confirm=True
)
```

### `quiz_create`
Generate quiz.

**Parameters:**
- `notebook_id` (required): Notebook UUID
- `source_ids` (optional, default=all): Source IDs
- `question_count` (optional, default=2): Number of questions
- `difficulty` (optional, default="medium"): Difficulty level
- `confirm` (required): Must be True

**Usage:**
```python
mcp__notebooklm-mcp__quiz_create(
    notebook_id="notebook-uuid",
    question_count=5,
    difficulty="medium",
    confirm=True
)
```

### `data_table_create`
Generate data table.

**Parameters:**
- `notebook_id` (required): Notebook UUID
- `description` (required): Description of the data table to create
- `source_ids` (optional, default=all): Source IDs
- `language` (optional, default="en"): Language code
- `confirm` (required): Must be True

**Usage:**
```python
mcp__notebooklm-mcp__data_table_create(
    notebook_id="notebook-uuid",
    description="Comparison of promotion types",
    confirm=True
)
```

---

## Studio Status

### `studio_status`
Check studio content generation status and get URLs.

**Parameters:**
- `notebook_id` (required): Notebook UUID

**Usage:**
```python
mcp__notebooklm-mcp__studio_status(notebook_id="notebook-uuid")
```

**When to use:** After creating audio/video/infographic/slides to check completion and get artifact URLs.

### `studio_delete`
Delete studio artifact. **IRREVERSIBLE.**

**Parameters:**
- `notebook_id` (required): Notebook UUID
- `artifact_id` (required): Artifact UUID (from studio_status)
- `confirm` (required): Must be True after user approval

**Usage:**
```python
mcp__notebooklm-mcp__studio_delete(
    notebook_id="notebook-uuid",
    artifact_id="artifact-uuid",
    confirm=True
)
```

---

## Common Tool Patterns

### Add a local file to notebook
1. Read file content
2. Use `notebook_add_text` with file content and filename as title

### Web research workflow
1. `research_start` - Begin research
2. `research_status` - Poll until complete
3. `research_import` - Import sources into notebook
4. `notebook_query` - Query the new sources

### Artifact generation workflow
1. `audio_overview_create`/`video_overview_create`/etc. with `confirm=True`
2. `studio_status` - Poll for completion and get URLs
