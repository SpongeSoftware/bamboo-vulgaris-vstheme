# Changelog

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
