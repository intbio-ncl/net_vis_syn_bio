from dashboard.full import FullDash
from visual.instance import InstanceVisual

class InstanceDash(FullDash):
    def __init__(self,name,server):
        super().__init__(InstanceVisual(),name,server,"/full_graph/")

    def load_graph(self,filename):
        self.visualiser = InstanceVisual(filename)
        return super()._load_graph()