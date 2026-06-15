#!/usr/bin/env bash
set -euo pipefail

VERSION=$(sed -n 's/^[[:space:]]*Version="\([^"]*\)"[[:space:]]*$/\1/p' source.extension.vsixmanifest)
OUT="bamboo-vulgaris-${VERSION}.vsix"

cp source.extension.vsixmanifest extension.vsixmanifest
zip -X "$OUT" "[Content_Types].xml" extension.vsixmanifest bamboo-vulgaris.pkgdef bamboo-vulgaris.vstheme README.md
rm extension.vsixmanifest

echo "Built: $OUT"
