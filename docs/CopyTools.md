
# CopyTools (Python Toolbox)

The **CopyTools** toolbox bundles helper utilities for **copying and consolidating** ArcGIS Pro data. It focuses on everyday operations like copying layers with their properties, consolidating distributed sources, or moving content into a **File Geodatabase**.

> The exact set of tools may differ by version. This page describes the general intent and typical parameter patterns so users know what to expect.

---

## Common workflows

- **Copy Layer**  
  Copy one or more layers (optionally with definition queries/symbology) into a target project or FileGDB.

- **Consolidate to FileGDB**  
  Gather distributed data sources referenced by a map or project into a single File Geodatabase—useful for archiving, exchange, or packaging.

- **Copy Attachments**  
  Move attachments between supported feature classes/geodatabases when needed.

---

## Parameters (typical)

- **Input Layer / Workspace**  
  Source layer(s) or workspace to read from.

- **Output Workspace**  
  Target FileGDB or folder where results will be written.

- **Extent / Filter (optional)**  
  Spatial/attribute scoping to limit what is copied.

- **Include Symbology / Attachments (optional)**  
  Switches to retain symbology or attachments (when applicable).

Validation and user feedback (errors/warnings) are handled in `updateParameters` / `updateMessages` so issues are visible **before** the tool runs.

---

## Installation & usage (ArcGIS Pro)

1. Add `CopyTools.pyt` via **Catalog** → **Toolboxes** → **Add Toolbox…**  
2. Open the desired tool, set **Input**/**Output** and optional filters/switches.  
3. Run the tool and check messages in the **Geoprocessing** pane.

---

## Automatic loading for all new projects

To make CopyTools available **by default** in new projects:

- **Use a Project Template** (recommended):  
  Create a project, **Add Toolbox…** → include `CopyTools.pyt`.  
  Then go to **Share** → **Project** → **Create Project Template** (`.aptx`) and set it as the default in **Options** → **General** → **Create projects** → **Use a default project template**.  
  All new projects created from that template will include CopyTools by default.

- **Favorites approach**:  
  Right‑click the toolbox in the **Catalog** pane → **Add To Favorites**.  
  You can clone favorites into individual projects later (right‑click **Favorites** → **Add To Project**).  
  For zero clicks in new projects, prefer the **Project Template** method.

---

## Notes

- Tools are implemented with **ArcPy** (no extra dependencies).
- For large data copies/consolidations, ensure sufficient space and permissions.
