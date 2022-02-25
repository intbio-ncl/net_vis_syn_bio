from dashboard.abstract.full import FullDash
from visual.protocol import ProtocolVisual

class ProtocolDash(FullDash):
    def __init__(self,name,server,model,is_multiple):
        super().__init__(ProtocolVisual(model),name,server,"/protocol/",is_multiple=is_multiple)

    def load_graph(self,filename):
        self.visualiser._load_graph(filename)
        return super()._load_graph()