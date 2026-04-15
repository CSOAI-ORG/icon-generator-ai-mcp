#!/usr/bin/env python3
"""Generate SVG icons, search icon sets, and convert icon formats. — MEOK AI Labs."""

import sys, os
sys.path.insert(0, os.path.expanduser('~/clawd/meok-labs-engine/shared'))
from auth_middleware import check_access

import json, math, hashlib
from datetime import datetime, timezone
from collections import defaultdict
from mcp.server.fastmcp import FastMCP

FREE_DAILY_LIMIT = 30
_usage = defaultdict(list)
def _rl(c="anon"):
    now = datetime.now(timezone.utc)
    _usage[c] = [t for t in _usage[c] if (now - t).total_seconds() < 86400]
    if len(_usage[c]) >= FREE_DAILY_LIMIT:
        return json.dumps({"error": f"Limit {FREE_DAILY_LIMIT}/day. Upgrade: meok.ai"})
    _usage[c].append(now)
    return None

mcp = FastMCP("icon-generator-ai", instructions="Generate SVG icons, search icon sets, and convert icon formats. By MEOK AI Labs.")

ICON_SHAPES = {
    "home": '<path d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-4 0h4"/>',
    "user": '<path d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>',
    "search": '<path d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>',
    "settings": '<path d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.066 2.573c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.573 1.066c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.066-2.573c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/><path d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>',
    "mail": '<path d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>',
    "heart": '<path d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/>',
    "star": '<path d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z"/>',
    "check": '<path d="M5 13l4 4L19 7"/>',
    "close": '<path d="M6 18L18 6M6 6l12 12"/>',
    "plus": '<path d="M12 6v12M6 12h12"/>',
    "minus": '<path d="M6 12h12"/>',
    "arrow-right": '<path d="M14 5l7 7m0 0l-7 7m7-7H3"/>',
    "arrow-left": '<path d="M10 19l-7-7m0 0l7-7m-7 7h18"/>',
    "bell": '<path d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"/>',
    "lock": '<path d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>',
    "trash": '<path d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>',
    "download": '<path d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/>',
    "upload": '<path d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"/>',
    "folder": '<path d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"/>',
    "file": '<path d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z"/>',
    "code": '<path d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"/>',
    "database": '<ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 12c0 1.657-4.03 3-9 3s-9-1.343-9-3"/><path d="M3 5v14c0 1.657 4.03 3 9 3s9-1.343 9-3V5"/>',
    "globe": '<path d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9"/>',
}

ICON_CATEGORIES = {
    "navigation": ["home", "search", "arrow-right", "arrow-left", "globe"],
    "action": ["plus", "minus", "check", "close", "download", "upload", "trash"],
    "communication": ["mail", "bell"],
    "content": ["file", "folder", "code", "database"],
    "user": ["user", "lock", "settings"],
    "social": ["heart", "star"],
}


@mcp.tool()
def generate_icon_svg(name: str, size: int = 24, stroke_width: float = 2.0, color: str = "currentColor", style: str = "outline", api_key: str = "") -> str:
    """Generate an SVG icon by name. Supports outline style with configurable size, color, and stroke width."""
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return json.dumps({"error": msg, "upgrade_url": "https://meok.ai/pricing"})
    if err := _rl():
        return err

    name_lower = name.lower().strip()
    if name_lower not in ICON_SHAPES:
        matches = [k for k in ICON_SHAPES if name_lower in k or k in name_lower]
        if matches:
            return json.dumps({"error": f"Icon '{name}' not found. Did you mean: {', '.join(matches)}?", "available": list(ICON_SHAPES.keys())})
        return json.dumps({"error": f"Icon '{name}' not found.", "available": list(ICON_SHAPES.keys())})

    size = max(12, min(size, 512))
    stroke_width = max(0.5, min(stroke_width, 5.0))
    shape = ICON_SHAPES[name_lower]

    fill = "none"
    if style == "filled":
        fill = color

    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="{fill}" stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round">{shape}</svg>'

    return json.dumps({
        "name": name_lower,
        "svg": svg,
        "size": size,
        "color": color,
        "stroke_width": stroke_width,
        "style": style,
        "viewBox": "0 0 24 24",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })


@mcp.tool()
def list_icon_sets(category: str = "", api_key: str = "") -> str:
    """List all available icons, optionally filtered by category."""
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return json.dumps({"error": msg, "upgrade_url": "https://meok.ai/pricing"})
    if err := _rl():
        return err

    if category:
        cat_lower = category.lower().strip()
        if cat_lower in ICON_CATEGORIES:
            icons = ICON_CATEGORIES[cat_lower]
            return json.dumps({
                "category": cat_lower,
                "icons": icons,
                "count": len(icons),
                "all_categories": list(ICON_CATEGORIES.keys()),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })
        return json.dumps({"error": f"Category '{category}' not found.", "available_categories": list(ICON_CATEGORIES.keys())})

    return json.dumps({
        "total_icons": len(ICON_SHAPES),
        "categories": {cat: {"icons": icons, "count": len(icons)} for cat, icons in ICON_CATEGORIES.items()},
        "all_icons": sorted(ICON_SHAPES.keys()),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })


@mcp.tool()
def search_icons(query: str, api_key: str = "") -> str:
    """Search for icons by keyword. Returns matching icon names and their categories."""
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return json.dumps({"error": msg, "upgrade_url": "https://meok.ai/pricing"})
    if err := _rl():
        return err

    query_lower = query.lower().strip()
    keyword_map = {
        "email": ["mail"], "envelope": ["mail"], "message": ["mail"],
        "notification": ["bell"], "alert": ["bell"],
        "delete": ["trash", "close"], "remove": ["trash", "close", "minus"],
        "add": ["plus"], "create": ["plus"],
        "save": ["download"], "export": ["download"],
        "edit": ["code"], "write": ["code"],
        "security": ["lock"], "password": ["lock"],
        "love": ["heart"], "favorite": ["heart", "star"],
        "rate": ["star"], "bookmark": ["star"],
        "back": ["arrow-left"], "forward": ["arrow-right"], "next": ["arrow-right"], "previous": ["arrow-left"],
        "confirm": ["check"], "ok": ["check"], "yes": ["check"],
        "cancel": ["close"], "no": ["close"],
        "storage": ["database"], "data": ["database"],
        "document": ["file"], "directory": ["folder"],
        "web": ["globe"], "internet": ["globe"], "world": ["globe"],
        "profile": ["user"], "account": ["user"], "person": ["user"],
        "gear": ["settings"], "config": ["settings"], "preferences": ["settings"],
    }

    matches = set()
    for name in ICON_SHAPES:
        if query_lower in name:
            matches.add(name)
    for kw, icons in keyword_map.items():
        if query_lower in kw or kw in query_lower:
            matches.update(icons)

    results = []
    for name in sorted(matches):
        cats = [cat for cat, icons in ICON_CATEGORIES.items() if name in icons]
        results.append({"name": name, "categories": cats})

    return json.dumps({
        "query": query,
        "result_count": len(results),
        "results": results,
        "total_available": len(ICON_SHAPES),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })


@mcp.tool()
def convert_format(icon_name: str, target_format: str = "react", size: int = 24, color: str = "currentColor", api_key: str = "") -> str:
    """Convert an icon to different output formats: react (JSX), vue, css-class, data-uri, path-only."""
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return json.dumps({"error": msg, "upgrade_url": "https://meok.ai/pricing"})
    if err := _rl():
        return err

    name_lower = icon_name.lower().strip()
    if name_lower not in ICON_SHAPES:
        return json.dumps({"error": f"Icon '{icon_name}' not found.", "available": list(ICON_SHAPES.keys())})

    shape = ICON_SHAPES[name_lower]
    target = target_format.lower().strip()
    component_name = "".join(word.capitalize() for word in name_lower.split("-")) + "Icon"

    if target == "react":
        output = f'const {component_name} = ({{ size = {size}, color = "{color}", ...props }}) => (\n  <svg xmlns="http://www.w3.org/2000/svg" width={{size}} height={{size}} viewBox="0 0 24 24" fill="none" stroke={{color}} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" {{...props}}>\n    {shape}\n  </svg>\n);\nexport default {component_name};'
    elif target == "vue":
        output = f'<template>\n  <svg xmlns="http://www.w3.org/2000/svg" :width="size" :height="size" viewBox="0 0 24 24" fill="none" :stroke="color" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">\n    {shape}\n  </svg>\n</template>\n<script setup>\ndefineProps({{ size: {{ type: Number, default: {size} }}, color: {{ type: String, default: "{color}" }} }})\n</script>'
    elif target == "css-class":
        import base64
        svg_raw = f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{shape}</svg>'
        encoded = base64.b64encode(svg_raw.encode()).decode()
        output = f'.icon-{name_lower} {{\n  display: inline-block;\n  width: {size}px;\n  height: {size}px;\n  background-image: url("data:image/svg+xml;base64,{encoded}");\n  background-size: contain;\n  background-repeat: no-repeat;\n}}'
    elif target == "data-uri":
        from urllib.parse import quote as url_quote
        svg_raw = f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{shape}</svg>'
        output = f"data:image/svg+xml,{url_quote(svg_raw)}"
    elif target == "path-only":
        output = shape
    else:
        return json.dumps({"error": f"Unsupported format '{target}'. Use: react, vue, css-class, data-uri, path-only"})

    return json.dumps({
        "icon": name_lower,
        "format": target,
        "component_name": component_name,
        "output": output,
        "size": size,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })


if __name__ == "__main__":
    mcp.run()
