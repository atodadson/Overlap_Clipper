from qgis.core import QgsProcessingProvider
from .overlap_table import OverlapTableAlgorithm

class OverlapProvider(QgsProcessingProvider):

    def id(self):
        return "overlap_clipper_provider"          # must match the ID used in algorithmById()

    def name(self):
        return "Overlap Clipper"                 # group name shown in the Toolbox

    def longName(self):
        return "Overlap Clipper"

    def loadAlgorithms(self):
        self.addAlgorithm(OverlapTableAlgorithm())

    def icon(self):
        # Optional — return a QIcon for the Toolbox group
        return super().icon()