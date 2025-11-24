# ClipTool QGIS Plugin

## Overview

The **ClipTool** is a powerful QGIS plugin designed to automatically clean overlaps between polygon features within a single layer. It provides a robust, customizable, and efficient solution for maintaining topological integrity in your vector data, eliminating common issues like slivers and unwanted overlaps.

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

The ClipTool is available directly through the official QGIS Plugin Manager.

1.  Open QGIS.
2.  Go to **Plugins** > **Manage and Install Plugins...**
3.  Search for `ClipTool`.
4.  Select the plugin and click **Install plugin**.

### Manual Installation (For Developers)

1.  Download the plugin source code (e.g., from the GitHub repository).
2.  Locate your QGIS plugins folder:
    *   **Windows:** `C:\Users\YOUR_USERNAME\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins`
    *   **Linux:** `~/.local/share/QGIS/QGIS3/profiles/default/python/plugins`
    *   **macOS:** `~/Library/Application Support/QGIS/QGIS3/profiles/default/python/plugins`
3.  Unzip the downloaded source code into a folder named `clip_tool` inside the plugins directory.
4.  Restart QGIS.

## Usage

### 1. Activate the Plugin

After installation, the ClipTool can be accessed via:

*   **Toolbar Icon:** [LEAVE SPACE FOR ICON DESCRIPTION/IMAGE]
*   **Menu:** **Plugins** > **Clip Tool** > [LEAVE SPACE FOR MENU ITEM NAME]

This will open the ClipTool DockWidget.

### 2. Prepare Your Data

1.  Ensure the polygon layer you wish to clean is the **Active Layer** in QGIS.
2.  **Start an editing session** on the layer (the plugin will prompt you to do this if necessary).
3.  Select the polygon features that you want to check for overlaps.

### 3. Configure and Run

The DockWidget provides the following controls:

| Control | Description |
| :--- | :--- |
| **Clip Button** | The main button to execute the overlap cleaning process. |
| **First Selected** | Sets the priority: The feature selected first will clip the feature selected second. |
| **Largest Area** | Sets the priority: The feature with the largest area will clip the smaller feature. |
| **Smallest Area** | Sets the priority: The feature with the smallest area will clip the larger feature. |
| **Edit all intersecting features** (Checkbox) | **Unchecked (Default):** Only processes overlaps between selected features. **Checked:** Processes overlaps between selected features and any other intersecting feature in the layer. |
| **Tree Widget** | Displays the selected features and their attributes. This is only active when a valid polygon layer is selected. |

**Steps to Clean Overlaps:**

1.  Select your desired **Clipping Priority** (First Selected, Largest, or Smallest).
2.  (Optional) Check the **Edit all intersecting features** box for a wider cleanup scope.
3.  Click the **Clip Button** (usually labeled `pushButton` in the UI).

The plugin will process the pairs, remove the overlapping areas from the lower-priority feature, and commit the changes to the layer. Progress and results will be shown in the QGIS Message Bar.

## Development and Contribution

*   **Author:** [LEAVE SPACE FOR AUTHOR NAME]
*   **Email:** [LEAVE SPACE FOR AUTHOR EMAIL]
*   **Repository:** [LEAVE SPACE FOR REPOSITORY URL]

### License

This project is licensed under the **GNU General Public License v3.0 (GPLv3)**. See the LICENSE file for details.

---
*Generated on: [LEAVE SPACE FOR DATE]*
*QGIS Version Compatibility: [LEAVE SPACE FOR COMPATIBLE QGIS VERSIONS]*
*Plugin Version: [LEAVE SPACE FOR PLUGIN VERSION]*
