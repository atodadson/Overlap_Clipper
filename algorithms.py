from qgis.core import QgsGeometry


def clean_overlap(geom_to_be_clipped, geom_clipper):
    """
    Cleans the overlap between two geometries
    by performing a difference operation,

    This method avoids QgsGeometrySimplifier and QgsGeometryAnalyzer.

    Args:
        geom_to_be_clipped (QgsGeometry): The geometry from
        which the overlap will be removed.
        geom_clipper (QgsGeometry): The geometry that
        defines the area to be removed.

    Returns:
        QgsGeometry: The resulting geometry after
        the difference operation and cleaning.
    """
    # 1. Check for intersection first
    if not geom_to_be_clipped.intersects(geom_clipper):
        return geom_to_be_clipped

    # 2. Perform the primary difference operation (A - B)
    # This is the desired result, but may contain slivers.
    modified_geom = geom_to_be_clipped.difference(geom_clipper)

    # 3. Robust Post-Processing (MakeValid and RemoveDuplicateNodes only)
    # Ensure the result is valid
    # (fixes topological errors like self-intersections,
    # which are often the cause of slivers).
    if not modified_geom.isGeosValid():
        modified_geom = modified_geom.makeValid()

    # Remove any duplicate nodes that might
    # have been created near the cut boundary.
    modified_geom.removeDuplicateNodes()

    if modified_geom.isEmpty():
        return QgsGeometry()

    return modified_geom


def clean_geometry_artifacts(geometry):
    """
    Performs general cleaning on a QgsGeometry object to remove duplicate nodes
    and ensure validity.

    Args:
        geometry (QgsGeometry): The input geometry.

    Returns:
        QgsGeometry: The cleaned geometry.
    """
    if geometry.isEmpty():
        return geometry

    # 1. Remove duplicate nodes (coincident vertices)
    geometry.removeDuplicateNodes()

    # 2. Ensure the geometry is valid (fixes self-intersections, etc.)
    if not geometry.isGeosValid():
        geometry = geometry.makeValid()

    return geometry


def get_feature_area(feature):
    """
    Calculates the area of a QgsFeature's geometry.

    Args:
        feature (QgsFeature): The feature to calculate the area for.

    Returns:
        float: The area of the feature's geometry.
    """
    if feature.geometry():
        # Use the geometry's area method, which respects the layer's CRS
        return feature.geometry().area()
    return 0.0
