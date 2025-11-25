# Test Data for Overlap Clipper Plugin

This dataset contains sample overlapping polygons stored as shapefiles (`test_data.shp`).
It is provided to allow users and reviewers to quickly test the plugin functionality.

- CRS: EPSG:4326
- Features: 6 polygons with some intentional overlaps
- Size: <10 KB

Usage:
1. Load `test_data.shp` into QGIS.
2. Select overlaping polygons
3. Run the Overlap Clipper plugin.
4. Verify that overlapping areas are clipped as expected.