from visual.handlers.abstract_color import AbstractNodeColorHandler , AbstractEdgeColorHandler

class ColorHandler():
    def __init__(self,builder):
        self.node = self.NodeColorHandler(builder)
        self.edge = self.EdgeColorHandler(builder)

    class NodeColorHandler(AbstractNodeColorHandler):
        def __init__(self,builder):
            super().__init__(builder)
            
        def role(self):
            print("WARN:: Not implemented.")
            colors = []
            for node,data in self._builder.v_nodes(data=True):
                colors.append({"standard" : StandardPalette.primary.value})
            return colors

    class EdgeColorHandler(AbstractEdgeColorHandler):
        def __init__(self,builder):
            super().__init__(builder)
        
        def predicate(self):
            print("WARN:: Not Implemented")
            colors = []
            for n,v,k,e in self._builder.v_edges(keys=True,data=True):
                colors.append({"standard" : "#888"})
            return colors
        
        def interaction(self):
            print("WARN:: Not Implemented")
            colors = []
            for n,v,k,e in self._builder.v_edges(keys=True,data=True):
                colors.append({"standard" : "#888"})
            return colors