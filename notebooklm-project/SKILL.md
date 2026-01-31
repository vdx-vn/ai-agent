---
name: notebooklm-project
description: Project-aware NotebookLM integration that manages notebooks for each project/workspace directory. Use when working with project-specific knowledge bases in NotebookLM - adding documents/URLs/Drive files to a project notebook, querying project notebook for information or context, generating summaries/reports/artifacts from project sources, or managing project notebooks (create, list, describe). Auto-detects project by current working directory.
---

# NotebookLM Project Integration

## Overview

This skill provides project-aware NotebookLM integration, automatically mapping each project directory to a dedicated NotebookLM notebook. The project is identified by the current working directory path, enabling context-aware knowledge management without manual notebook ID tracking.

## Quick Start

### First Time Setup

When first working with a project directory:
1. Skill checks for existing notebook mapping
2. If no mapping exists, auto-creates a NotebookLM notebook named after the directory
3. Stores the mapping locally for future sessions

### Common Operations

**Add a file to project notebook:**
```
"Add this README.md to the project notebook"
"Add this URL to tc_purchase_master project notebook"
```

**Query project notebook:**
```
"What have we discussed about purchase order promotions?"
"Summarize the project documentation"
"Find information about the approval workflow"
```

**Manage project notebooks:**
```
"List all my project notebooks"
"Describe the tc_purchase_master notebook"
"Create a briefing doc from this project's sources"
```

## Core Capabilities

### 1. Project Detection

Projects are identified by the **current working directory**. The project name is derived from the directory basename.

**Example mapping:**
- `/Users/dylantran/WORK/VDX/TierdCity/src/tierd-city/tc_purchase_master` → `tc_purchase_master` notebook
- `/Users/dylantran/WORK/VDX/TierdCity/src/tierd-city/tc_master` → `tc_master` notebook

### 2. Notebook Management

#### Auto-Create New Notebooks

When a project directory has no existing notebook mapping:
1. Extract project name from directory basename
2. Create new NotebookLM notebook with that name
3. Store mapping in `~/.claude/notebooklm-projects.json`

#### Mapping File Format

```json
{
  "/path/to/project": {
    "notebook_id": "notebook-uuid",
    "project_name": "project-name",
    "created_at": "2025-01-20T10:00:00Z"
  }
}
```

### 3. Adding Sources

Use the appropriate NotebookLM MCP tool based on source type:

| Source Type | Tool | Example |
|-------------|------|---------|
| Text/Pasted content | `mcp__notebooklm-mcp__notebook_add_text` | Code snippets, notes |
| URLs | `mcp__notebooklm-mcp__notebook_add_url` | Documentation, articles |
| Google Drive | `mcp__notebooklm-mcp__notebook_add_drive` | Docs, Slides, Sheets, PDFs |

**Important:** Always verify auth before operations. If auth fails, prompt user to run `notebooklm-mcp-auth`.

### 4. Querying Notebooks

#### For Existing Sources
Use `mcp__notebooklm-mcp__notebook_query` for:
- Q&A about existing project documentation
- Finding specific information within sources
- Exploring relationships between documents

#### For Deep Research
Use `mcp__notebooklm-mcp__research_start` for:
- Web research on specific topics
- Finding new sources
- Deep-dive investigations (~5min, ~40 sources)

#### Source Content
Use `mcp__notebooklm-mcp__source_get_content` for:
- Retrieving raw text from sources (faster than query)
- Exporting indexed content
- Processing without AI summarization

### 5. Generating Artifacts

NotebookLM can generate various artifacts from project sources:

| Artifact | Tool | Use Case |
|----------|------|----------|
| Audio overview | `mcp__notebooklm-mcp__audio_overview_create` | Project briefings, deep dives |
| Video overview | `mcp__notebooklm-mcp__video_overview_create` | Visual explanations |
| Report | `mcp__notebooklm-mcp__report_create` | Briefing docs, study guides |
| Slide deck | `mcp__notebooklm-mcp__slide_deck_create` | Presentations |
| Infographic | `mcp__notebooklm-mcp__infographic_create` | Visual summaries |
| Mind map | `mcp__notebooklm-mcp__mind_map_create` | Concept mapping |
| Timeline | `mcp__notebooklm-mcp__timeline_create` | Project history |
| Flashcards | `mcp__notebooklm-mcp__flashcards_create` | Study materials |
| Quiz | `mcp__notebooklm-mcp__quiz_create` | Knowledge testing |

**After artifact generation:** Poll `mcp__notebooklm-mcp__studio_status` to get completion status and URLs.

## Workflow Decision Tree

```
User requests NotebookLM operation
│
├─ Need to add content?
│  ├─ Text? → notebook_add_text
│  ├─ URL? → notebook_add_url
│  └─ Drive file? → notebook_add_drive
│
├─ Need to query/existing sources?
│  ├─ Q&A about existing docs? → notebook_query
│  ├─ Export raw content? → source_get_content
│  └─ Find new sources/research? → research_start
│
└─ Need to generate something?
   ├─ Briefing/summary? → report_create
   ├─ Presentation? → slide_deck_create
   ├─ Visual overview? → infographic_create or video_overview_create
   └─ Study materials? → flashcards_create or quiz_create
```

## Implementation Notes

### Getting Project Notebook ID

1. Get current working directory
2. Check `~/.claude/notebooklm-projects.json` for mapping
3. If not found, create new notebook and store mapping
4. Return notebook_id for subsequent operations

### Error Handling

- **Auth errors**: Prompt user to run `notebooklm-mcp-auth`
- **Notebook not found**: List notebooks and ask user to select, or create new
- **Invalid source type**: Validate before calling MCP tool

### Confirmation Requirements

Some tools require `confirm=True` after user approval:
- `audio_overview_create`
- `video_overview_create`
- `infographic_create`
- `slide_deck_create`
- `report_create`
- `flashcards_create`
- `quiz_create`
- `mind_map_create`
- `notebook_delete`
- `source_delete`

Always ask user before setting `confirm=True`.

## Available MCP Tools Reference

See [MCP_TOOLS.md](references/MCP_TOOLS.md) for complete list of NotebookLM MCP tools with parameters and usage examples.
