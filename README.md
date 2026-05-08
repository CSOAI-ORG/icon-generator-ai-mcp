<div align="center">

# Icon Generator Ai MCP

**MCP server for icon generator ai mcp operations**

[![PyPI](https://img.shields.io/pypi/v/meok-icon-generator-ai-mcp)](https://pypi.org/project/meok-icon-generator-ai-mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![MEOK AI Labs](https://img.shields.io/badge/MEOK_AI_Labs-MCP_Server-purple)](https://meok.ai)

</div>

## Overview

Icon Generator Ai MCP provides AI-powered tools via the Model Context Protocol (MCP).

## Tools

| Tool | Description |
|------|-------------|
| `generate_icon_svg` | Generate an SVG icon by name. Supports outline style with configurable size, col |
| `list_icon_sets` | List all available icons, optionally filtered by category. |
| `search_icons` | Search for icons by keyword. Returns matching icon names and their categories. |
| `convert_format` | Convert an icon to different output formats: react (JSX), vue, css-class, data-u |

## Installation

```bash
pip install meok-icon-generator-ai-mcp
```

## Usage with Claude Desktop

Add to your Claude Desktop MCP config (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "icon-generator-ai": {
      "command": "python",
      "args": ["-m", "meok_icon_generator_ai_mcp.server"]
    }
  }
}
```

## Usage with FastMCP

```python
from mcp.server.fastmcp import FastMCP

# This server exposes 4 tool(s) via MCP
# See server.py for full implementation
```

## License

MIT © [MEOK AI Labs](https://meok.ai)
