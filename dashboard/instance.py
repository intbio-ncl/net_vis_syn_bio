from dashboard.full import FullDash
from visual.instance import InstanceVisual

class InstanceDash(FullDash):
    def __init__(self,name,server,model):
        super().__init__(InstanceVisual(model),name,server,"/full_graph/")

    def load_graph(self,filename):
        self.visualiser._load_graph(filename)
        return super()._load_graph()