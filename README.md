
# ArcGIS Pro — Additional Toolboxes

This repository collects **additional Python toolboxes (.pyt)** for ArcGIS Pro that streamline common tasks and standardize repeatable workflows. Each toolbox is designed to work natively in the **Geoprocessing** pane and depends only on **ArcPy** and the Python standard library.

> Each toolbox has **one** dedicated documentation page in `docs/`. This README is an entry point and overview.

---

## Included toolboxes

- **Mobile Maps**  
  Utilities for working with **ArcGIS Mobile Map Packages (.mmpk)**: validation, unpack, and repack (re‑zip).  
  → See: `docs/MobileMaps.md`

- **CopyTools**  
  Utilities for copying/consolidating layers and datasets (e.g., copy layers, consolidate to FileGDB, copy attachments).  
  → See: `docs/CopyTools.md`

---

## Installation (ArcGIS Pro)

1. **Clone** or **download** this repository.
2. In **ArcGIS Pro**, open the **Catalog** pane:
   - Right‑click **Toolboxes** → **Add Toolbox…**
   - Select the desired **`.pyt`** (e.g., `MobileMaps.pyt`, `CopyTools.pyt`).

The toolbox appears under **Toolboxes** and is ready to use in the **Geoprocessing** pane.

> Make sure you run these tools using the **ArcGIS Pro Python environment** (ArcPy).

---

## Requirements

- **ArcGIS Pro** (recommended: latest 3.x)
- **ArcPy** (installed with ArcGIS Pro)
- Read/write permissions on the involved locations
- Sufficient **disk space** for larger packages or datasets

---

## Automatic loading for all new projects

If you want these toolboxes to be available **by default in every new ArcGIS Pro project**, use one of the following options:

1. **Project Template (recommended)**  
   - Create a clean project, **Add Toolbox…** for each toolbox you want preloaded.  
   - Go to **Share** → **Project** → **Create Project Template** and save the template (`.aptx`).  
   - In **Options** → **General** → **Create projects**, set **“Use a default project template”** and browse to your template.  
   - New projects created from **New → Your Template** (or from the default template) will automatically include the toolboxes.

2. **Favorites + New Projects**  
   - In the **Catalog** pane, right‑click a toolbox → **Add To Favorites**.  
   - When you **clone** a favorite into a project (right‑click **Favorites** → **Add To Project**), it becomes part of that project.  
   - For truly automatic inclusion, prefer a **Project Template** as above.

> Using a **project template** ensures the toolboxes are already part of the project’s structure and appear instantly in the **Geoprocessing** pane without any manual steps.

---

## Contributing & support

- Please file **issues** or **feature requests** via the GitHub **Issues** tab.
- **Pull requests** are welcome. Please:
  - Keep code style consistent and well‑commented
  - Use only ArcPy and the Python standard library
  - Add or update the toolbox doc page under `docs/`

---

## License

See **LICENSE** in the repository (or propose a suitable one, e.g., MIT or Apache‑2.0).

---

## Maintainer

This repository is maintained by **Esri Deutschland**. For questions and ideas, please open an **Issue** in this repository.
