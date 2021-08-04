from visual.handlers.color_palettes import StandardPalette
from visual.handlers.abstract_color import AbstractNodeColorHandler , AbstractEdgeColorHandler

class ColorHandler():
    def __init__(self):
        self.node = self.NodeColorHandler()
        self.edge = self.EdgeColorHandler()

    class NodeColorHandler(AbstractNodeColorHandler):
        def __init__(self):
            super().__init__()
            
        def role(self,builder):
            print("WARN:: Not implemented.")
            colors = []
            for node,data in builder.v_nodes(data=True):
                colors.append({"standard" : StandardPalette.primary.value})
            return colors

    class EdgeColorHandler(AbstractEdgeColorHandler):
        def __init__(self):
            super().__init__()
        
        def predicate(self,builder):
            print("WARN:: Not Implemented")
            colors = []
            for n,v,k,e in builder.v_edges(keys=True,data=True):
                colors.append({"standard" : "#888"})
            return colors
        
        def interaction(self,builder):
            print("WARN:: Not Implemented")
            colors = []
            for n,v,k,e in builder.v_edges(keys=True,data=True):
                colors.append({"standard" : "#888"})
            return colors