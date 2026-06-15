<div align="center">
  <img src="assets/logo.svg" alt="Bamboo (Vulgaris) logo" width="100"/>
  <h1>Bamboo (Vulgaris)</h1>
  <p>A dark color theme for Visual Studio, derived from the <a href="https://github.com/ribru17/bamboo.nvim">bamboo.nvim</a> vulgaris palette.</p>
</div>

---

Bamboo (Vulgaris) brings the earthy, carefully balanced tones of the bamboo.nvim color scheme to Visual Studio.

The theme covers the full surface area of the IDE: editor syntax and semantic tokens, environment chrome, panels and tool windows, the integrated terminal (including all 16 ANSI colors), IntelliSense completion, CodeLens, and the VS 2026 Fluent Design shell tokens.

## Color Palette

| Role | Token | Hex |
|---|---|---|
| Background | `bg0` | `#252623` |
| Panel background | `bg1` | `#2f312c` |
| Borders / inactive | `bg2` | `#383b35` |
| Selection | `bg3` | `#3a3d37` |
| Deep background | `bg_d` | `#1c1e1b` |
| Foreground | `fg` | `#f1e9d2` |
| Comments | `grey` | `#5b5e5a` |
| Keywords | `purple` | `#aaaaff` |
| Strings | `green` | `#8fb573` |
| Types / Classes / Structs | `yellow` | `#dbb651` |
| Functions / Methods | `blue` | `#57a5e5` |
| Properties / Events | `cyan` | `#70c2be` |
| Variables / Errors | `red` | `#e75a7c` |
| Constants / Numbers | `orange` | `#ff9966` |
| Namespaces | `light_blue` | `#96c7ef` |
| Type parameters | `bright_purple` | `#df73ff` |

## Installation

### Via Visual Studio Marketplace (recommended)

Open **Extensions → Manage Extensions** in Visual Studio, search for **Bamboo (Vulgaris)**, and click **Download**.

### Manual installation (from a built VSIX)

1. Download the `.vsix` — either from the [Releases](https://github.com/SpongeSoftware/bamboo-vulgaris-vstheme/releases) or by building it (see below).
2. Double-click the `.vsix` to install, or use **Extensions → Manage Extensions → Install from VSIX**.
3. Restart Visual Studio.
4. Go to **Tools → Options → Environment → General** and pick **Bamboo (Vulgaris)** from the **Color theme** dropdown.

> The loose `bamboo-vulgaris.vstheme` file cannot be installed on its own — Visual Studio reads colors from a *compiled* pkgdef that is produced when the `.vstheme` is built into a VSIX. Always install the `.vsix`.

## Development & testing

Edit colors by changing the palette mapping in [`tools/recolor.py`](tools/recolor.py), then regenerate the theme:

```bash
python3 tools/recolor.py      # rewrites bamboo-vulgaris.vstheme
```

The build compiles `bamboo-vulgaris.vstheme` into a registered pkgdef using
`Microsoft.VisualStudio.VsixColorCompiler`. **Always test a freshly built VSIX before publishing a new version** — there are two ways to get one:

### Option A — build in GitHub Actions (no Windows needed)

1. Push your change. The **Build VSIX** workflow builds on a Windows runner and the
   *Verify theme compiled into pkgdef* step fails the build if the colors didn't compile in.
2. Open the workflow run → **Artifacts** → download **bamboo-vulgaris-vsix** → unzip to get `BambooVulgaris.ColorTheme.vsix`.
3. (Optional sanity check, on any OS) unzip the `.vsix` and confirm the bundled `*.pkgdef`
   contains `"Data"=hex:` lines — that is the compiled color data VS actually paints with.
4. On a Windows machine, install the `.vsix`, restart VS, and select the theme.

### Option B — build from the solution in Visual Studio

1. Open `BambooVulgaris.sln` in Visual Studio 2022/2026.
2. Set the configuration to **Release** and **Build**. The VSIX lands at
   `bin/Release/BambooVulgaris.ColorTheme.vsix`.
3. Or press **F5** to launch the Visual Studio *Experimental Instance* with the theme
   already loaded — the fastest way to iterate on colors.

### Releasing a new version

The version is tracked in `CHANGELOG.md` (semantic versioning) and stamped into the VSIX
automatically — never hand-edit the version in `source.extension.vsixmanifest`.

1. Add a new entry at the top of `CHANGELOG.md`: `## [x.y.z] — YYYY-MM-DD`.
2. Commit and push. CI runs `tools/set_version.py`, which copies that version into the
   manifest before building, so the artifact (named `bamboo-vulgaris-<version>`) carries it.
3. Publish via **Actions → Build VSIX → Run workflow** with **publish = true** (requires the
   `VS_MARKETPLACE_PAT` repo secret), or upload the `.vsix` manually at the
   [Marketplace manage page](https://marketplace.visualstudio.com/manage).

Bumping the CHANGELOG each release also avoids the "version already exists" rejection from
the marketplace. For a local build, run `python3 tools/set_version.py` first so the `.sln`
build matches the CHANGELOG.

## Compatibility

| Product | Version |
|---|---|
| Visual Studio 2022 | 17.0 and later |
| Visual Studio 2026 | 18.0 and later |

## License

MIT
