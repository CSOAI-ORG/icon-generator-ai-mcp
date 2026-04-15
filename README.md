# Icon Generator AI

> By [MEOK AI Labs](https://meok.ai) — Generate SVG icon data and descriptions

## Installation

```bash
pip install icon-generator-ai-mcp
```

## Usage

```bash
# Run standalone
python server.py

# Or via MCP
mcp install icon-generator-ai-mcp
```

## Tools

### `generate_icon_svg`
Generate SVG icon data from a text description.

**Parameters:**
- `description` (str): Description of the desired icon
- `style` (str): Icon style, e.g. "outline" (default: "outline")

### `suggest_icons`
Suggest icon ideas for a given context.

**Parameters:**
- `context` (str): Context or use-case for icon suggestions
- `count` (int): Number of suggestions to return (default: 5)

### `convert_icon_format`
Convert SVG icon data to a different format.

**Parameters:**
- `svg_data` (str): SVG icon data to convert
- `format` (str): Target format, e.g. "path" (default: "path")

### `search_icon_names`
Search for icon names matching a query.

**Parameters:**
- `query` (str): Search query for icon names

## Authentication

Free tier: 30 calls/day. Upgrade at [meok.ai/pricing](https://meok.ai/pricing) for unlimited access.

## License

MIT — MEOK AI Labs
