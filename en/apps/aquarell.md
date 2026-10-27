---
layout: app
app_id: pastel
title: 'Aquarell: drawing and watercolour-style illustration on iPhone and iPad'
description: Explore Aquarell brushes, layers, palettes and export formats. Watch MCP draw the 19-layer Cloud Mountains,
  Evening Ferry and find setup details for MCP-enabled builds.
permalink: /en/apps/aquarell/
modified: 2026-10-27
lang: en
source_url: /apps/aquarell/
---

Aquarell is a **drawing and illustration app for iPhone and iPad**. It brings brushes, layers, palettes and custom canvases together for quick sketches and more developed pieces. Its English App Store title is “Aquarell: Drawing & Watercolor”.

## What you can make

- **A layered illustration.** Keep sketches, colour and details on separate layers. Adjust opacity and blend modes so each part can be edited independently.
- **Brush exercises.** Compare line work, colouring and overlapping marks by changing size, opacity and spacing.
- **A reusable palette.** Select colours, save a palette or sample from the canvas to keep a piece consistent.
- **Drawings with text.** Add text and import fonts for a title or a short explanation.
- **Files to share or keep editing.** Export PNG, JPEG, PDF, TIFF or a PSD with raster layers, and keep a native project as well.

## Begin with a small exercise

Try a plant or a still life with three layers: a sketch, colour and final details. That is enough to learn layers and export without changing every brush setting at once.

[Read the Aquarell getting-started guide: create a canvas, draw in layers and export a PNG]({{ '/en/guides/aquarell-getting-started/' | relative_url }}).

## Choose how to save

PNG and JPEG are useful for a blog, social post or message. To keep editing, save the native Aquarell project too. A PSD export preserves raster layers, but it is not a replacement for the native document: keep editable text and layer groups in the original project.

Aquarell is suited to painting built around brush marks and pixel layers. For SVG paths or a scalable logo, see [VectorPaint]({{ '/en/apps/vectorpaint/' | relative_url }}).

## Paint in layers through MCP

Aquarell MCP (Model Context Protocol) lets an AI client read canvas and brush information, then call native brush, layer, selection, text, save and export tools. Strokes are rendered in the app, with painted content retained on raster layers. A composition brief can become a sequence of washes and detailed adjustments.

[Cloud Mountains, Evening Ferry]({{ '/en/works/aquarell-cloud-mountains-evening-ferry-mcp/' | relative_url }}) follows an actual painting from pale distant mountains to a foreground pine, pavilion and small boat. The native project is 1600 × 1100 px with 19 layers, including native text inscriptions. Its project page provides a tutorial with the full app interface and a breakdown of the layers.

Getting started requires **an Apple silicon Mac that can run iPad apps, an MCP-enabled Aquarell build, Python 3.9+ and a client supporting local stdio MCP**. Follow the [Aquarell MCP installation instructions](https://github.com/SoBison/Aquarell-mcp/blob/main/README.md) to install the bridge and generate a personal configuration. Then check connection and editing permissions under **AI Control (MCP)** in the **gallery folder menu or canvas layer-tools menu**.

The [Aquarell MCP integration source and documentation](https://github.com/SoBison/Aquarell-mcp) are public. The integration is currently a preview; App Store and TestFlight release packages have not been validated. Check that your actual build provides the MCP entry point first.

## Common questions

### Can I export a PSD?

Yes, with raster layers. This does not mean every text object, layer group or editing property will remain editable in another app.

### Can I draw on an iPhone?

Yes. Aquarell is made for iPhone and iPad. The checked store version, 1.0.6, requires iOS or iPadOS 15.0 or later. Check the download page for current compatibility.

### Are these hands-on device reviews?

This introduction and the getting-started guide are based on public release information and the available feature entry points. Source-code checks are not presented as tests on a physical device. Layouts may vary by device and version; individual project articles explain their own recording setup.

## Version and sources

Checked on 27 October 2026: the China App Store listed version **1.0.6**. Feature information comes from the [Aquarell App Store page](https://apps.apple.com/cn/app/id1591340577); version and system requirements were checked with [Apple’s public lookup API](https://itunes.apple.com/lookup?id=1591340577&country=cn).
