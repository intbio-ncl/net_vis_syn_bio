from dashboards.full_dash import FullDash
from visual.sbol_visual import SBOLVisualiser

class SBOLDash(FullDash):
    def __init__(self,name,server):
        super().__init__(SBOLVisualiser(),name,server,"/full_graph/")

    def load_graph(self,filename):
        self.visualiser = SBOLVisualiser(filename)
        return super()._load_graph()