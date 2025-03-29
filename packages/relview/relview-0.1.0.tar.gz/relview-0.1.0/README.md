# OpenUSD Relationship Viewer

`relview` is a visualizer for relationships between OpenUSD prims and attributes.


## Installation

    pip install relview


## usdview plugin

A `plugInfo.json` file that provides a `usdview` plugin is installed into the
`share/usd/plugins/` area.

Extend the OpenUSD plugins environment variable (e.g. `PXR_PLUGINPATH_NAME`)
to activate the plugin.
