
# Mobile Maps (Python Toolbox)

The **Mobile Maps** toolbox provides utilities to validate and (re)package **ArcGIS Mobile Map Packages (.mmpk)** for robust offline usage.

---

## Tools

### Validate MMPK
**Purpose**  
Validates a `.mmpk` by unpacking and checking a minimal, runtime‑relevant structure. Optionally keeps the unpacked files and returns the folder as an output.

**How it works**
1. Unpacks the input `.mmpk` into a temp folder using **ArcPy / ExtractPackage**.
2. If needed, selectively **pulls `esriinfo/`** directly from the ZIP container (some ArcGIS unpack flows omit it).
3. Verifies a **minimal structure** in the unpacked folder:
   - `esriinfo/` at the root
   - **exactly one** `p..` folder (three characters, starts with `p`, e.g., `p14`)
   - at least **one** file with extension `.info` at the root
4. Reports success via `AddMessage`, problems via `AddWarning`.
5. If **Keep Unpacked Files = True**, exposes **UnpackDirectory (output)** and logs the path.

**Typical usage**
- Check if a package is structurally sound before distribution
- Keep the unpacked folder for manual inspection or further automation

---

### Pack MMPK
**Description**  
**Creates an MMPK file from a directory that is valid as an MMPK.**

**Purpose**  
Re‑zips a **valid MMPK folder** into a `.mmpk` file using **ZIP_STORED** (no compression) and **ZIP64** (supports large files).

**Features**
- **Auto‑output path**: once a source folder is selected, the tool auto‑fills the output to `<parent>/<foldername>.mmpk` so the user can see and adjust it.
- **Existence check**: warns/errors in the parameter UI when the output already exists.
  - **Allow Overwrite = False** → **Error** (blocking)
  - **Allow Overwrite = True** → **Warning** (will overwrite)
- **Optional cleanup**: **Delete Source After Packing** removes the source folder on success.

**Minimal source‑folder structure**
- `esriinfo/` at the root
- exactly one `p..` folder (e.g., `p14`)
- at least one `*.info` file at the root

**Notes**
- Packing is a **re‑zip** of the existing structure; functional correctness (runtime version, layer definitions, renderers, etc.) remains the responsibility of the source contents.
- Parameter tooltips in the Geoprocessing pane are managed via **Metadata (Item Description)**—not from `.pyt` code.

---

## Installation & usage (ArcGIS Pro)

1. Add `MobileMaps.pyt` via **Catalog** → **Toolboxes** → **Add Toolbox…**
2. Run **Validate MMPK** (optionally keep the unpacked folder).  
3. Run **Pack MMPK** on a valid source folder (optionally overwrite and/or delete the source after packing).

---

## Maintenance & extension

- Shared internals (unpack, selective `esriinfo/`, minimal validation, re‑zip) are implemented once and reused by both tools.
- Easy to add:
  - File count and size reporting
  - Stricter `p..` pattern (e.g., `^p\d{2}$`)
  - Additional JSON checks on `.mmap` if required
