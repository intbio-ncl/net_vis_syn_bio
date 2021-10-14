from dashboard.full import FullDash
from visual.model import ModelVisual

class ModelDash(FullDash):
    def __init__(self,name,server):
        super().__init__(ModelVisual(),name,server,"/model_graph/")

    def load_graph(self,filename):
        self.visualiser = ModelVisual(filename)
        return super()._load_graph()