#!/usr/bin/env python3
"""
Stamp the extension version from CHANGELOG.md into source.extension.vsixmanifest.

The CHANGELOG is the single source of truth for the version (semver). Its first
`## [x.y.z]` heading is the current release. This script copies that into the
manifest's <Identity Version="..."> so the compiled VSIX always carries the tracked
version — preventing duplicate-version collisions on the marketplace.

Run it before building, locally or in CI:
  python3 tools/set_version.py     # updates the manifest, prints the version
"""

import re
import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
changelog = root / "CHANGELOG.md"
manifest = root / "source.extension.vsixmanifest"

m = re.search(r'^##\s*\[(\d+\.\d+\.\d+)\]', changelog.read_text(encoding="utf-8"),
              flags=re.MULTILINE)
if not m:
    sys.exit("error: no '## [x.y.z]' version heading found in CHANGELOG.md")
version = m.group(1)

text = manifest.read_text(encoding="utf-8")
# Only the <Identity> element's Version — never PackageManifest's schema version
# ("2.0.0") or the bracketed [17.0,) install-target / prerequisite versions.
new_text, n = re.subn(r'(<Identity\b[^>]*?\bVersion=")[^"]*(")',
                      rf'\g<1>{version}\g<2>', text, count=1, flags=re.DOTALL)
if n != 1:
    sys.exit("error: could not find <Identity Version=\"...\"> in the manifest")

if new_text != text:
    manifest.write_text(new_text, encoding="utf-8")

print(version)
