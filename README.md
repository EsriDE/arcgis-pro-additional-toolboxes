
# ArcGIS Pro Toolboxes

## Overview
This repository contains a collection of ArcGIS Pro Python toolboxes designed to streamline and automate common GIS workflows. The tools support tasks such as feature management, data validation, and operations across multiple maps or layers. They help reduce repetitive work, ensure consistent processing, and provide reusable components for teams and projects.  
A practical example is the *Copy Layer* tool, which copies features—including geometry and shared attributes—between layers located in different maps of an ArcGIS Pro project.

---

## Installation

### 1. Download or clone the repository
Clone the repository or download it as a ZIP and place it in any directory accessible to ArcGIS Pro, e.g.:
C:\Projects\ArcGISToolboxes\
Your toolbox file may look like:
C:\Projects\ArcGISToolboxes\DataCopyTools.pyt


### 2) Add the folder in ArcGIS Pro (one‑time per project)
1. Open **ArcGIS Pro**  
2. In the **Catalog** pane, right‑click **Folders**  
3. Select **Add Folder Connection**  
4. Choose the folder containing the toolbox  
→ The `.pyt` toolbox appears automatically in the Catalog under the folder connection.

---

## Automatic loading for all new projects (recommended)

To make the toolbox automatically available in **every new ArcGIS Pro project**, use **Favorites → Add To New Projects**:

1. In the **Catalog** pane, right‑click **Favorites**  
2. Click **Add Folder** and pick the folder that contains your toolbox  
3. Right‑click the newly added favorite and choose **Add To New Projects**

ArcGIS Pro will now:
- Automatically add a folder connection for that location to **every new project**
- Automatically show any `.pyt` / `.tbx` / `.atbx` toolboxes in that folder
- Require no manual setup per project

> Note: ArcGIS Pro supports setting a **default toolbox** per project, but only **`.tbx`** can be used as the default toolbox. Python toolboxes (`.pyt`) cannot be assigned as the project’s default toolbox. Use the Favorites method above to surface `.pyt` toolboxes consistently.

---

## Usage
1. Expand your folder connection in the **Catalog**
2. Open the toolbox, e.g. *Data Copy Tools*
![copytools](/assets/copytools-toolbox.png)
3. Run a tool, such as **Copy Layer**
4. Select the parameters:
   - **Source Map**
   - **Target Map**
   - **Source Layer**
   - **Target Layer**
   - **Clear target before copying** (optional)
![copylayer](/assets/copy-layer.png)

The tool reports progress with a progress bar and provides per‑row error handling (including the ObjectID of failed source rows), followed by a copy summary.
![copylayer](/assets/copy-layer-results.png)

---

## Team Workflow
These toolboxes are plain Python text files:
- Version control via **Git/GitHub** works seamlessly
- No installation is required on client machines
- Users automatically work with the latest version after pulling the repo
- Shared utility scripts (e.g., `layerutils.py`) can live next to the toolbox

This makes the toolset ideal for collaborative GIS development.

---

## Requirements
- **ArcGIS Pro** 2.x or 3.x  
- Python environment bundled with ArcGIS Pro (**ArcPy**)  
- Read/write access to the chosen maps, layers, or feature classes

---

## License
This project is licensed under the **MIT License**.  
See the `LICENSE` file for details.

---

## Contributing
Contributions are welcome! Please read `CONTRIBUTING.md` for guidelines.