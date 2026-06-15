#!/usr/bin/env python3
"""
Regenerate bamboo-vulgaris.vstheme from a verified Microsoft VS theme skeleton.

A working VS color theme requires every Fonts-and-Colors category to use the
exact GUID and color names that Visual Studio registers internally. Hand-authoring
these is error-prone (an invented category GUID makes VS silently drop the whole
category). Instead we start from Microsoft's shipping SolarizedDark theme — which
is known to load and apply correctly — and remap only its palette to the
bamboo.nvim "vulgaris" colors. The verified structure (categories, GUIDs, color
names) is preserved byte-for-byte; only CT_RAW colour values change.

Skeleton source:
  microsoft/VS-ColorThemes :: VSColorThemes/Themes/SolarizedDark.xml
  fetched via: gh api repos/microsoft/VS-ColorThemes/contents/VSColorThemes/Themes/SolarizedDark.xml

Usage:
  python3 tools/recolor.py            # reads tools/SolarizedDark.xml, writes bamboo-vulgaris.vstheme
"""

import re
import sys
from pathlib import Path

THEME_NAME = "Bamboo (Vulgaris)"
THEME_GUID = "{b4e2f173-a8c5-4d6e-9f02-1b3c5d7e9f01}"
FALLBACK_DARK = "{1ded0138-47ce-435e-84ef-9ec1f439b749}"

# bamboo.nvim vulgaris palette (RRGGBB)
BG_D = "1C1E1B"   # deepest background / title bar
BG0  = "252623"   # main background
BG1  = "2F312C"   # panels / cursor line
BG2  = "383B35"   # borders / inactive
BG3  = "3A3D37"   # selection / raised
FG   = "F1E9D2"   # normal text
GREY = "5B5E5A"   # comments / line numbers
LGRY = "838781"   # dimmed text
RED  = "E75A7C"
GREEN= "8FB573"
YELL = "DBB651"
BLUE = "57A5E5"
PURP = "AAAAFF"
CYAN = "70C2BE"
ORNG = "FF9966"
BPUR = "DF73FF"   # bright purple / type params

# Solarized skeleton RRGGBB  ->  bamboo RRGGBB. Alpha is matched separately so
# translucent variants (e.g. 72RRGGBB) remap too.
MAP = {}

def add(targets, dest):
    for t in targets:
        MAP[t.upper()] = dest

# backgrounds: collapse Solarized's dark ramp onto bamboo's
add(["001419", "000E11", "001726", "000E11"], BG_D)
add(["001E26", "002731", "002B36", "05323C", "0B353E", "00333E", "001188", "002D2D30"], BG0)
add(["073642", "003542", "003C49", "003F4F", "004654", "05323C"], BG1)
add(["20454F", "223744", "2D535B", "284151", "074957", "335B66", "0F202D", "1B293E"], BG2)
add(["3A555A", "44646A", "4A6184", "427094", "477786", "335B66", "434E5E"], BG3)
# text / muted
add(["839496", "93A1A1"], FG)
add(["586E75", "657B83"], GREY)
add(["716F64", "709194", "73828C", "7CA5A0", "89ABBD"], LGRY)
# accents by hue
add(["268BD2", "0097FB", "007ACC", "1C97EA", "52B0EF", "569CD6", "0E70C0",
     "0E639C", "0E6198", "117AD1", "1382CE", "0573EE", "43A6E0", "56AFE3",
     "65A6E7", "5F95FA"], BLUE)
add(["2AA198", "1D89A0", "4EB3BF", "2B91AF", "1A9BB5", "10828E", "4EB543"], CYAN)
add(["719A07", "859900", "95DB7D", "75BF5B", "B5CEA8", "76923C", "57A64A",
     "5D8039", "71B252", "9FB861", "8ABB2E"], GREEN)
add(["B58900", "C59E00", "E5C365", "EDC865", "D7BA7D", "D7BA7C", "F1CA5D",
     "CAB22D", "A79432", "B18110"], YELL)
add(["CB4B16", "E86222", "BF3F00", "CA5100", "9B4601", "B0764F"], ORNG)
add(["DC322F", "E51400", "D85050", "FF0000", "F30506", "F22930", "E61E27",
     "DF2424", "DF2020", "FC3E36", "F05033", "F20A0A"], RED)
add(["D33682", "E122DF", "AE3CBA", "8631C7", "8A2BE2"], BPUR)
add(["6C71C4", "7B81CE", "7E6693", "7B81CE", "536699"], PURP)


LPUR = "C5C2EE"   # operators (light purple)

# bamboo assigns different hues per syntax role than Solarized does, so a flat
# palette swap isn't enough — override token foregrounds by role. Keyed by the
# VS classification (Color Name) inside the editor language-service category.
SYNTAX_ROLES = {
    "Keyword":       PURP,
    "Comment":       GREY,
    "Identifier":    FG,
    "String":        GREEN,
    "Number":        ORNG,
    # XML
    "XML Keyword":   PURP,
    "XML Comment":   GREY,
    "XML Name":      RED,
    "XML Attribute": GREEN,
    "XML Attribute Value": GREEN,
    "XML Attribute Quotes": LGRY,
    "XML Delimiter": LGRY,
    "XML Text":      FG,
    "XML CData Section": FG,
    "XSLT Keyword":  PURP,
    # XAML
    "XAML Keyword":   PURP,
    "XAML Comment":   GREY,
    "XAML Name":      BLUE,
    "XAML Attribute": GREEN,
    "XAML Attribute Value": GREEN,
    "XAML Attribute Quotes": LGRY,
    "XAML Delimiter": LGRY,
    "XAML Text":      FG,
    "XAML Markup Extension Class": YELL,
    "XAML Markup Extension Parameter Name": CYAN,
    "XAML Markup Extension Parameter Value": GREEN,
}

LANG_SERVICE_GUID = "{e0187991-b458-4f7e-8ca9-42c9a573b56c}"


def apply_syntax_roles(xml: str) -> str:
    """Override token Foreground colours by role inside the language-service category."""
    cat_re = re.compile(
        r'(<Category Name="Text Editor Language Service Items"[^>]*>)(.*?)(</Category>)',
        re.DOTALL)
    m = cat_re.search(xml)
    if not m:
        return xml
    head, body, tail = m.group(1), m.group(2), m.group(3)

    def set_fg(body: str, name: str, rgb: str) -> str:
        # Within this color's block, replace the Foreground Source (preserve alpha FF).
        color_re = re.compile(
            r'(<Color Name="' + re.escape(name) + r'">.*?<Foreground Type="CT_RAW" Source=")[0-9A-Fa-f]{8}(")',
            re.DOTALL)
        if color_re.search(body):
            return color_re.sub(r'\g<1>FF' + rgb + r'\g<2>', body)
        # Foreground may be CT_AUTOMATIC (e.g. Identifier) — leave those alone.
        return body

    for name, rgb in SYNTAX_ROLES.items():
        body = set_fg(body, name, rgb)

    return xml[:m.start()] + head + body + tail + xml[m.end():]


def remap_color(argb: str) -> str:
    """argb is 8 hex chars AARRGGBB. Remap the RGB part if in MAP, keep alpha."""
    alpha = argb[:2]
    rgb = argb[2:].upper()
    if rgb in MAP:
        return alpha + MAP[rgb]
    return argb


def main():
    here = Path(__file__).resolve().parent
    skeleton = here / "SolarizedDark.xml"
    if not skeleton.exists():
        sys.exit(f"Skeleton not found: {skeleton}\n"
                 "Fetch it with:\n"
                 "  gh api repos/microsoft/VS-ColorThemes/contents/VSColorThemes/Themes/SolarizedDark.xml "
                 "--jq .content | base64 -d > tools/SolarizedDark.xml")

    xml = skeleton.read_text(encoding="utf-8")

    # Remap every CT_RAW Source value.
    def repl(m):
        return f'Source="{remap_color(m.group(1))}"'
    xml = re.sub(r'Source="([0-9A-Fa-f]{8})"', repl, xml)

    # Override syntax token foregrounds by bamboo role.
    xml = apply_syntax_roles(xml)

    # Rewrite the Theme element: name, GUID, dark fallback.
    xml = re.sub(
        r'<Theme\b[^>]*>',
        f'<Theme Name="{THEME_NAME}" GUID="{THEME_GUID}" FallbackId="{FALLBACK_DARK}">',
        xml, count=1)

    out = here.parent / "bamboo-vulgaris.vstheme"
    out.write_text(xml, encoding="utf-8")
    print(f"Wrote {out} ({len(xml.splitlines())} lines)")


if __name__ == "__main__":
    main()
