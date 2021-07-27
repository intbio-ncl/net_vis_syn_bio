from dashboards.full_dash import FullDash
from visual.knowledge_visual import KnowledgeVisualiser

class KnowledgeDash(FullDash):
    def __init__(self,name,server):
        super().__init__(KnowledgeVisualiser(),name,server,"/knowledge_graph/")

    def load_graph(self,filename):
        self.visualiser = KnowledgeVisualiser(filename)
        return super()._load_graph()