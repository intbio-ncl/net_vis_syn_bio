from dashboard.full import FullDash
from visual.design import DesignVisual

class ProtocolDash(FullDash):
    def __init__(self,name,server,model):
        super().__init__(DesignVisual(model),name,server,"/full_graph/")

    def load_graph(self,filename):
        self.visualiser._load_graph(filename)
        return super()._load_graph()