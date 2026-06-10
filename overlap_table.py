"""
Overlap Table Algorithm for QGIS
---------------------------------
Generates a table of overlapping polygon pairs from a polygon layer.
Uses spatial indexing (QgsSpatialIndex) for efficient candidate lookup,
then performs precise geometric intersection only on candidates.
 
Output fields per row:
  - Feature A ID
  - Feature B ID
  - Any user-selected fields from Feature A (prefixed with 'a_')
  - Any user-selected fields from Feature B (prefixed with 'b_')
  - Overlap Area (in layer CRS units²)
  - Overlap Area % of Feature A
  - Overlap Area % of Feature B
"""
 
from qgis.PyQt.QtCore import QCoreApplication, QVariant, QMetaType
from qgis.core import (
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingParameterVectorLayer,
    QgsProcessingParameterField,
    QgsProcessingParameterFeatureSink,
    QgsProcessingException,
    QgsFeatureSink,
    QgsFeature,
    QgsField,
    QgsFields,
    QgsSpatialIndex,
    QgsFeatureRequest,
    QgsWkbTypes,
    QgsVectorLayer,
    QgsProcessingOutputVectorLayer,
)
 
 
class OverlapTableAlgorithm(QgsProcessingAlgorithm):
    INPUT = "INPUT"
    FIELDS = "FIELDS"
    OUTPUT = "OUTPUT"
 
    # ------------------------------------------------------------------
    # Boilerplate
    # ------------------------------------------------------------------
 
    def name(self):
        return "generateoverlaptable"
 
    def displayName(self):
        return "Generate Overlap Table"
 
    def group(self):
        return "Vector Analysis"
 
    def groupId(self):
        return "vectoranalysis"
 
    def shortHelpString(self):
        return (
            "Scans a polygon layer for overlapping feature pairs and produces "
            "a table describing each overlap.\n\n"
            "For every pair (A, B) whose geometries intersect (share interior area), "
            "the algorithm records:\n"
            "  • The IDs of both features\n"
            "  • Any attribute fields you select (duplicated for both A and B, "
            "prefixed with 'a_' and 'b_')\n"
            "  • The overlap area (in CRS units²)\n"
            "  • The overlap area as a percentage of Feature A's area\n"
            "  • The overlap area as a percentage of Feature B's area\n\n"
            "A QgsSpatialIndex is built once and used to narrow candidates before "
            "any precise geometry call, keeping the algorithm fast even on large layers."
        )
 
    def tr(self, string):
        return QCoreApplication.translate("Processing", string)
 
    def createInstance(self):
        return OverlapTableAlgorithm()
 
    # ------------------------------------------------------------------
    # Parameters
    # ------------------------------------------------------------------
 
    def initAlgorithm(self, config=None):
        # 1. Input polygon layer
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT,
                self.tr("Input polygon layer"),
                types=[QgsProcessing.TypeVectorPolygon],
            )
        )
 
        # 2. Fields to carry through (optional, multi-select)
        self.addParameter(
            QgsProcessingParameterField(
                self.FIELDS,
                self.tr("Fields to include in output (from input layer)"),
                parentLayerParameterName=self.INPUT,
                allowMultiple=True,
                optional=True,
            )
        )
 
        # 3. Output — table (no geometry), so use QgsProcessing.TypeVector
        #    The user can save as .csv, .dbf, .gpkg (table), or leave as
        #    a temporary scratch layer.
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT,
                self.tr("Overlap table"),
                type=QgsProcessing.TypeVector,   # geometry-less / table
            )
        )
 
    # ------------------------------------------------------------------
    # Main logic
    # ------------------------------------------------------------------
 
    def processAlgorithm(self, parameters, context, feedback):
        # ── 1. Resolve inputs ──────────────────────────────────────────
        layer = self.parameterAsVectorLayer(parameters, self.INPUT, context)
        if layer is None:
            raise QgsProcessingException(self.tr("Invalid input layer."))
 
        selected_field_names = self.parameterAsFields(parameters, self.FIELDS, context)
        # QgsField objects for the chosen fields
        source_fields = layer.fields()
        chosen_fields = [source_fields.field(n) for n in selected_field_names]
 
        # ── 2. Build output schema ─────────────────────────────────────
        out_fields = QgsFields()
        out_fields.append(QgsField("fid_a", QMetaType.Type.LongLong))
        out_fields.append(QgsField("fid_b", QMetaType.Type.LongLong))
 
        for f in chosen_fields:
            fa = QgsField(f)
            fa.setName("a_" + f.name())
            out_fields.append(fa)
 
        for f in chosen_fields:
            fb = QgsField(f)
            fb.setName("b_" + f.name())
            out_fields.append(fb)
 
        out_fields.append(QgsField("overlap_area",   QMetaType.Type.Double))
        out_fields.append(QgsField("overlap_pct_a",  QMetaType.Type.Double))
        out_fields.append(QgsField("overlap_pct_b",  QMetaType.Type.Double))
 
        # ── 3. Create sink ─────────────────────────────────────────────
        (sink, dest_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            out_fields,
            QgsWkbTypes.NoGeometry,   # table — no geometry column
            layer.sourceCrs(),
        )
        if sink is None:
            raise QgsProcessingException(self.invalidSinkError(parameters, self.OUTPUT))
 
        # ── 4. Load all features into memory & build spatial index ─────
        feedback.setProgressText(self.tr("Loading features and building spatial index…"))
 
        features = {}          # fid → QgsFeature
        areas    = {}          # fid → float  (pre-computed, avoids repeated calls)
 
        for feat in layer.getFeatures():
            if feedback.isCanceled():
                return {self.OUTPUT: dest_id}
            fid = feat.id()
            geom = feat.geometry()
            if geom is None or geom.isEmpty():
                continue
            features[fid] = feat
            areas[fid]    = geom.area()
 
        total_features = len(features)
        if total_features < 2:
            feedback.pushWarning(self.tr("Fewer than 2 valid features found — nothing to compare."))
            return {self.OUTPUT: dest_id}
 
        # Build spatial index from the in-memory dict
        spatial_index = QgsSpatialIndex()
        for feat in features.values():
            spatial_index.addFeature(feat)
 
        feedback.setProgressText(self.tr("Detecting overlaps…"))
 
        # ── 5. Iterate — each pair checked exactly once ────────────────
        processed_pairs = set()   # store (min_fid, max_fid) to avoid duplicates
        overlap_count   = 0
        checked         = 0
 
        fid_list = list(features.keys())
 
        for i, fid_a in enumerate(fid_list):
            if feedback.isCanceled():
                return {self.OUTPUT: dest_id}
 
            feat_a = features[fid_a]
            geom_a = feat_a.geometry()
            bbox_a = geom_a.boundingBox()
            area_a = areas[fid_a]
 
            # Spatial index gives cheap candidate list
            candidates = spatial_index.intersects(bbox_a)
 
            for fid_b in candidates:
                if fid_b == fid_a:
                    continue
 
                # Canonical ordering so (a,b) and (b,a) map to the same key
                pair_key = (min(fid_a, fid_b), max(fid_a, fid_b))
                if pair_key in processed_pairs:
                    continue
                processed_pairs.add(pair_key)
 
                feat_b = features[fid_b]
                geom_b = feat_b.geometry()
                area_b = areas[fid_b]
 
                # Precise geometric check
                try:
                    if not geom_a.intersects(geom_b):
                        continue
 
                    intersection = geom_a.intersection(geom_b)
                    if intersection is None or intersection.isEmpty():
                        continue
 
                    # Only count true area overlaps (ignore shared edges/points)
                    overlap_area = intersection.area()
                    if overlap_area <= 0:
                        continue
 
                except Exception as e:
                    feedback.pushWarning(
                        self.tr(f"Geometry error for pair ({fid_a}, {fid_b}): {e}")
                    )
                    continue
 
                # ── Build output row ───────────────────────────────────
                out_feat = QgsFeature(out_fields)
                out_feat.setAttribute("fid_a", fid_a)
                out_feat.setAttribute("fid_b", fid_b)
 
                for field in chosen_fields:
                    fname = field.name()
                    out_feat.setAttribute("a_" + fname, feat_a[fname])
                    out_feat.setAttribute("b_" + fname, feat_b[fname])
 
                pct_a = (overlap_area / area_a * 100) if area_a > 0 else None
                pct_b = (overlap_area / area_b * 100) if area_b > 0 else None
 
                out_feat.setAttribute("overlap_area",  round(overlap_area, 6))
                out_feat.setAttribute("overlap_pct_a", round(pct_a, 4) if pct_a is not None else None)
                out_feat.setAttribute("overlap_pct_b", round(pct_b, 4) if pct_b is not None else None)
 
                sink.addFeature(out_feat, QgsFeatureSink.FastInsert)
                overlap_count += 1
 
            # Progress based on outer loop
            checked += 1
            feedback.setProgress(int(checked / total_features * 100))
 
        feedback.pushInfo(
            self.tr(f"Done. {overlap_count} overlapping pair(s) found across {total_features} features.")
        )
 
        return {self.OUTPUT: dest_id}
