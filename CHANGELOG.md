# Changelog

## [1.0.2] — 2026-06-16

- Fixed the theme not applying at all (editor and chrome stayed light). The build now
  compiles `bamboo-vulgaris.vstheme` into a registered pkgdef with
  `Microsoft.VisualStudio.VsixColorCompiler` and ships the assembly — previously it
  shipped a raw `.vstheme` plus a pkgdef that declared only the theme name with no
  color data, so Visual Studio had nothing to paint with.
- Rebuilt the palette on the Catppuccin theme structure, which includes the VS 2026
  `Shell` / `ShellInternal` Fluent chrome categories that were missing before.
- Added `BambooVulgaris.sln` for local builds and a CI step that fails if the compiled
  pkgdef contains no color data.

## [1.0.1] — 2026-06-16

- Rebuilt the theme on a verified Visual Studio theme structure so it actually
  applies. The hand-authored editor category used an unregistered GUID, which VS
  silently ignored — leaving the editor and chrome on the default light theme.
- Editor and IDE chrome now render with the bamboo vulgaris palette: warm dark
  backgrounds, purple keywords, green strings, yellow types, blue methods,
  orange numbers, grey comments.

## [1.0.0] — 2026-06-15

- Initial release of Bamboo (Vulgaris) Visual Studio color theme
- Full coverage of Environment, CommonControls, TreeView, text editor syntax, CodeLens, Search, Terminal (ANSI colors), and IntelliSense completion
- VS 2026 Fluent Design tokens (Shell / ShellInternal categories)
