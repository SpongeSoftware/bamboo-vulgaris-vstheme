#!/usr/bin/env python3
import re
import zipfile
from pathlib import Path

manifest = Path("source.extension.vsixmanifest").read_text()
version = re.search(r'^\s*Version="([^"]+)"\s*$', manifest, re.MULTILINE).group(1)
out = f"bamboo-vulgaris-{version}.vsix"

entries = [
    ("[Content_Types].xml",     "[Content_Types].xml"),
    ("extension.vsixmanifest",  "source.extension.vsixmanifest"),
    ("bamboo-vulgaris.pkgdef",  "bamboo-vulgaris.pkgdef"),
    ("bamboo-vulgaris.vstheme", "bamboo-vulgaris.vstheme"),
    ("README.md",               "README.md"),
]

with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
    for arcname, src in entries:
        zf.write(src, arcname)

print(f"Built: {out}")
