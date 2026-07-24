from qgis.core import QgsProcessingProvider
from .overlap_table import OverlapTableAlgorithm


class OverlapProvider(QgsProcessingProvider):

    def id(self):
        return "overlap_clipper_provider"

    def name(self):
        return "Overlap Clipper"

    def longName(self):
        return "Overlap Clipper"

    def loadAlgorithms(self):
        self.addAlgorithm(OverlapTableAlgorithm())

    def icon(self):
        return super().icon()
