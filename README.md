# Overlap Clipper QGIS Plugin
![Overlap Clipper](icon.png)


## Overview

The **Overlap Clipper** is a powerful QGIS plugin designed to detect and clean overlaps between polygon features within a single layer. It provides a robust, customizable, and efficient solution for maintaining topological integrity in your vector data, eliminating common issues like slivers and unwanted overlaps.

## Features

*   **Automatic Overlap Cleaning:** Uses a robust geometric difference operation combined with topological cleaning (`makeValid`, `removeDuplicateNodes`) to ensure clean boundaries and eliminate slivers.
*   **Flexible Clipping Priority:** Allows users to define which feature maintains its geometry (the "clipper") based on three criteria:
    *   **First Selected:** The feature selected first in the map view.
    *   **Largest Area:** The feature with the greater area.
    *   **Smallest Area:** The feature with the smaller area.
*   **Smart Feature Selection:** A toggleable option to expand the processing scope:
    *   **Selected Only (Default):** Only processes overlaps between the currently selected features.
    *   **All Intersecting:** Processes overlaps between selected features and *any* other feature in the active layer that intersects them, ensuring comprehensive cleaning across the project area.
*   **Layer Validation:** Automatically disables the tool's functionality (clip button, selection display) when the active layer is not a polygon layer, preventing errors and guiding the user.
*   **Logging:** Provides real-time feedback and error messages via the QGIS message bar.

## Installation

### From the QGIS Plugin Repository

The Overlap Clipper is available directly through the official QGIS Plugin Manager.

1.  Open QGIS.
2.  Go to **Plugins** > **Manage and Install Plugins...**
3.  Search for `Overlap Clipper`.
4.  Select the plugin and click **Install plugin**.

### Manual Installation (For Developers)

1.  Download the plugin source code (e.g., from the GitHub repository).
2.  Locate your QGIS plugins folder:
    *   **Windows:** `C:\Users\YOUR_USERNAME\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins`
    *   **Linux:** `~/.local/share/QGIS/QGIS3/profiles/default/python/plugins`
    *   **macOS:** `~/Library/Application Support/QGIS/QGIS3/profiles/default/python/plugins`
3.  Unzip the downloaded source code into a folder named `Overlap Clipper` inside the plugins directory.
4.  Restart QGIS.

## Usage

### 1. Activate the Plugin

After installation, the Overlap Clipper can be accessed via:

*   **Toolbar Icon**
*   **Menu:** **Plugins** > **Overlap Clipper**

This will open the Overlap Clipper DockWidget.

### 2. Prepare Your Data

1.  Ensure the polygon layer you wish to clean is the **Active Layer** in QGIS.
2.  **Start an editing session** on the layer (This is optional as the plugin automatically starts the edit session if a clip operation is initiated).
3.  Select the polygon features with overlaps that you want to clip.

### 3. Configure and Run

The DockWidget provides the following controls:

| Control | Description |
| :--- | :--- |
| **Clip Button** | The main button to execute the overlap cleaning process. |
| **Generate Overlap Table** | The main button for generating overlap Table (It provides information on all the polygon pairs which are overlapping. The area and percentage overlap are also provided in the table). |
| **First Selected** | Sets the priority: The feature selected first will clip the feature selected second. |
| **Largest Area** | Sets the priority: The feature with the largest area will clip the smaller feature. |
| **Smallest Area** | Sets the priority: The feature with the smallest area will clip the larger feature. |
| **Edit selection only** (Checkbox) | **Checked (Default):** Only processes overlaps between selected features. **Unchecked:** Processes overlaps between selected features and any other feature intersecting with the selected features in the layer. |
| **Enable Undo** (Checkbox) | **Checked (Default):** Undo command is enabled after clipping overlaps. **Unchecked:** All edits made to the layer are committed, hence undo is disabled. |
| **Tree Widget** | Displays the selected features and their attributes. This is only active when a valid polygon layer is selected. |

**Steps to Clean Overlaps:**

1.  Select your desired **Clipping Priority** (First Selected, Largest, or Smallest).
2.  (Optional) Check the **Edit selection only** box to have control over the features which are edited (clipped).
3.  Click the **Clip Button** to clean overlaps according to the criteria selected().

The plugin will process the pairs and remove the overlapping areas from the lower-priority feature. 

**Generating Overlap Table:**

1.  Click the **Generate Overlap Table** button on the dockwidget to create and overlap table which gives information on overlapping feature pairs.
2.  The **Generate Overlap Table** functionality is also available in processing toolbox under the provider name **Overlap Clipper** and group name **Vector Analysis**.

## Development and Contribution

*   **Author:** *Benjamin Dadson*
*   **Email:** *benjamindadson32@gmail.com*

### License

This project is licensed under the **GNU General Public License v3.0 (GPLv3)**. See the LICENSE file for details.

### Requirement

QGIS Version: *3.0 - 3.99*
Input Layer: *Polygon layer*
