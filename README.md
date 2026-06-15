<div align="center">
  <img src="assets/logo.svg" alt="Bamboo (Vulgaris) logo" width="100"/>
  <h1>Bamboo (Vulgaris)</h1>
  <p>A dark color theme for Visual Studio, derived from the <a href="https://github.com/ribru17/bamboo.nvim">bamboo.nvim</a> vulgaris palette.</p>
</div>

---

Bamboo (Vulgaris) brings the earthy, carefully balanced tones of the bamboo.nvim color scheme to Visual Studio. Designed for developers who use the same palette across their entire environment — Neovim, Wezterm, and now Visual Studio — with consistent syntax semantics across all three.

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

### Manual installation

1. Download `bamboo-vulgaris.vstheme` from this repository.
2. Copy it to the Visual Studio themes directory:
   ```
   %LOCALAPPDATA%\Microsoft\VisualStudio\<version>\Themes\
   ```
   Create the `Themes` folder if it does not exist.
3. Restart Visual Studio.
4. Navigate to **Tools → Options → Environment → General** and select **Bamboo (Vulgaris)** from the **Color theme** dropdown.

## Compatibility

| Product | Version |
|---|---|
| Visual Studio 2022 | 17.0 and later |
| Visual Studio 2026 | 18.0 and later |

## Screenshots

_Coming soon._

## License

MIT
