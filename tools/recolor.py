#!/usr/bin/env python3
"""
Regenerate bamboo-vulgaris.vstheme from a verified VS theme skeleton.

A working Visual Studio theme must use the exact category GUIDs and color names VS
registers internally, and (for VS 2026) include the Shell / ShellInternal Fluent
chrome categories. Rather than hand-author these, we start from the Catppuccin Mocha
theme — which is known to load and apply in VS 2022 and VS 2026 — and remap only its
palette to the bamboo.nvim "vulgaris" colors. The verified structure (categories,
GUIDs, color names) is preserved; only CT_RAW color values change. The build then
compiles this .vstheme into a real pkgdef via Microsoft.VisualStudio.VsixColorCompiler.

Skeleton source:
  github.com/catppuccin/visual-studio :: "Catppuccin VS Themes/Catppuccin Mocha.vstheme"
  saved here as tools/CatppuccinMocha.skeleton.xml (the .xml extension keeps the build's
  VsixColorCompiler — which globs **/*.vstheme — from compiling the skeleton itself).

Usage:
  python3 tools/recolor.py
"""

import re
from pathlib import Path

THEME_NAME = "Bamboo (Vulgaris)"
THEME_GUID = "{b4e2f173-a8c5-4d6e-9f02-1b3c5d7e9f01}"
FALLBACK_DARK = "{1ded0138-47ce-435e-84ef-9ec1f439b749}"

# bamboo.nvim vulgaris palette (RRGGBB)
BG_D = "1C1E1B"; BG0 = "252623"; BG1 = "2F312C"; BG2 = "383B35"; BG3 = "3A3D37"
FG = "F1E9D2"; GREY = "5B5E5A"; LGRY = "838781"
RED = "E75A7C"; GREEN = "8FB573"; YELL = "DBB651"; BLUE = "57A5E5"
PURP = "AAAAFF"; LPUR = "C5C2EE"; CYAN = "70C2BE"; ORNG = "FF9966"
LBLU = "96C7EF"; BPUR = "DF73FF"

# Catppuccin Mocha RRGGBB -> bamboo RRGGBB (alpha is preserved separately).
MAP = {
    # text
    "CDD6F4": FG,      # text
    "BAC2DE": LGRY,    # subtext1
    "939AB7": LGRY,    # overlay2
    "7F849C": GREY,    # overlay1 (comments)
    "6E738D": GREY,    # overlay0
    # backgrounds
    "1E1E2E": BG0,     # base
    "181825": BG_D,    # mantle
    "11111B": BG_D,    # crust
    "313244": BG1,     # surface0
    "45475A": BG2,     # surface1
    "586078": BG3,     # surface2
    # accents (by role)
    "CBA6F7": PURP,    # mauve   -> keywords
    "CA9EE6": PURP,    # mauve variant
    "F5C2E7": BPUR,    # pink    -> type params
    "B4BEFE": LBLU,    # lavender-> namespaces
    "F38BA8": RED,     # red     -> errors / fields
    "EBA0AC": RED,     # maroon
    "A6E3A1": GREEN,   # green   -> strings / interfaces
    "F9E2AF": YELL,    # yellow  -> types
    "FAB387": ORNG,    # peach   -> numbers / constants
    "89B4FA": BLUE,    # blue    -> methods
    "74C7EC": BLUE,    # sapphire
    "8AADF4": BLUE,    # (alt blue)
    "94E2D5": CYAN,    # teal    -> properties
    "89DCEB": CYAN,    # sky
}

# Extra Roslyn semantic classifications to enrich C# coloring, injected into the
# "Text Editor MEF Items" category (where VS reads editor semantic colors).
SEMANTIC = {
    "class name": YELL, "struct name": YELL, "enum name": YELL, "delegate name": YELL,
    "record class name": YELL, "record struct name": YELL, "module name": YELL,
    "interface name": GREEN, "type parameter name": BPUR,
    "method name": BLUE, "extension method name": BLUE,
    "property name": CYAN, "event name": CYAN,
    "field name": RED, "constant name": ORNG, "enum member name": ORNG,
    "local name": FG, "parameter name": FG,
    "namespace name": LBLU, "label name": RED,
    "keyword - control": PURP, "operator - overloaded": LPUR, "punctuation": LGRY,
    "preprocessor text": LGRY,
}

MEF_CATEGORY = "Text Editor MEF Items"


def remap_color(argb: str) -> str:
    alpha, rgb = argb[:2], argb[2:].upper()
    return alpha + MAP.get(rgb, rgb)


def add_semantic(xml: str) -> str:
    cat_re = re.compile(
        r'(<Category Name="' + re.escape(MEF_CATEGORY) + r'"[^>]*>)(.*?)(</Category>)',
        re.DOTALL)
    m = cat_re.search(xml)
    if not m:
        return xml
    head, body, tail = m.groups()
    additions = []
    for name, rgb in SEMANTIC.items():
        if f'Name="{name}"' in body:
            continue
        additions.append(
            f'      <Color Name="{name}">\n'
            f'        <Background Type="CT_AUTOMATIC" Source="00000000" />\n'
            f'        <Foreground Type="CT_RAW" Source="FF{rgb}" />\n'
            f'      </Color>\n')
    return xml[:m.start()] + head + body + "".join(additions) + tail + xml[m.end():]


def main():
    here = Path(__file__).resolve().parent
    skeleton = here / "CatppuccinMocha.skeleton.xml"
    xml = skeleton.read_text(encoding="utf-8")

    xml = re.sub(r'Source="([0-9A-Fa-f]{8})"',
                 lambda m: f'Source="{remap_color(m.group(1))}"', xml)

    # Editor body text should be the warm cream fg, not the dimmer subtext Mocha uses.
    xml = re.sub(
        r'(<Color Name="Plain Text">.*?<Foreground Type="CT_RAW" Source=")[0-9A-Fa-f]{8}(")',
        r'\g<1>FF' + FG + r'\g<2>', xml, flags=re.DOTALL)

    xml = add_semantic(xml)
    xml = re.sub(
        r'<Theme\b[^>]*>',
        f'<Theme Name="{THEME_NAME}" GUID="{THEME_GUID}" FallbackId="{FALLBACK_DARK}">',
        xml, count=1)

    out = here.parent / "bamboo-vulgaris.vstheme"
    out.write_text(xml, encoding="utf-8")
    print(f"Wrote {out} ({len(xml.splitlines())} lines)")


if __name__ == "__main__":
    main()
