from dashboard.abstract.full import FullDash
from visual.model import ModelVisual

class ModelDash(FullDash):
    def __init__(self,name,server,model_fn):
        super().__init__(ModelVisual(model_fn),name,server,"/model/")

    def load_graph(self,filename):
        self.visualiser = ModelVisual(filename)
        return super()._load_graph()