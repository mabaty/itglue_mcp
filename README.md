# itglue_mcp

Python MCP server for IT Glue. Exposes organizations, configurations (assets), documents, and flexible assets to any MCP client (Claude Desktop, OpenClaw, etc.).

## Requirements

- Python 3.11+
- An IT Glue API key (generate in IT Glue: **Account → Settings → API Keys**)

## Installation

```bash
pip install -e .
```

Or with `uv`:

```bash
uv pip install -e .
```

## Configuration

Copy `.env.example` to `.env` and fill in your values:

```bash
ITGLUE_API_KEY=ITG.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
ITGLUE_REGION=us   # us | eu | au
```

## Running

```bash
ITGLUE_API_KEY=ITG.xxx ITGLUE_REGION=us itglue-mcp
```

Or load from a `.env` file and run:

```bash
export $(cat .env | xargs) && itglue-mcp
```

## OpenClaw / Claude Desktop setup

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "itglue": {
      "command": "itglue-mcp",
      "env": {
        "ITGLUE_API_KEY": "ITG.xxx",
        "ITGLUE_REGION": "us"
      }
    }
  }
}
```

If using `uvx` without a global install:

```json
{
  "mcpServers": {
    "itglue": {
      "command": "uvx",
      "args": ["--from", "/path/to/itglue_mcp", "itglue-mcp"],
      "env": {
        "ITGLUE_API_KEY": "ITG.xxx",
        "ITGLUE_REGION": "us"
      }
    }
  }
}
```

## Available tools

### Organizations
| Tool | Description |
|---|---|
| `list_organizations` | List organizations with optional name filter |
| `get_organization` | Get a single organization by ID |
| `create_organization` | Create a new organization |
| `update_organization` | Update an organization's name/description |

### Configurations (assets)
| Tool | Description |
|---|---|
| `list_configurations` | List configurations, filterable by org or name |
| `get_configuration` | Get a single configuration by ID |
| `create_configuration` | Create a new configuration |
| `update_configuration` | Update a configuration |
| `delete_configuration` | Delete a configuration |

### Documents
| Tool | Description |
|---|---|
| `list_documents` | List documents, filterable by org or name |
| `get_document` | Get a single document by ID |
| `create_document` | Create a document with optional body content |
| `update_document` | Update a document's title |
| `delete_document` | Delete a document |

### Flexible Assets
| Tool | Description |
|---|---|
| `list_flexible_asset_types` | List all flexible asset type definitions |
| `list_flexible_assets` | List flexible assets by type and org |
| `get_flexible_asset` | Get a single flexible asset by ID |
| `create_flexible_asset` | Create a new flexible asset with traits |
| `update_flexible_asset` | Update flexible asset traits |
| `delete_flexible_asset` | Delete a flexible asset |

## Rate limiting

IT Glue allows 3000 requests per 5-minute window. The client automatically retries `429` responses with exponential backoff (2 s, 4 s, 8 s).
