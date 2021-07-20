from visual.handlers.color_palettes import StandardPalette

class ColorHandler:
    def __init__(self):
        self.node = self.NodeColorHandler()
        self.edge = self.EdgeColorHandler()

    class NodeColorHandler:
        def __init__(self):
            pass
        
        def standard(self,view):
            return [{"standard" : StandardPalette.primary.value} for node in view.nodes()]

        def rdf_type(self,view,graph):
            colors = []
            for node,data in view.nodes(data=True):
                if graph.graph.get_rdf_type(node) is not None:
                    color = {"rdf_type" : StandardPalette.primary.value}
                else:
                    color = {"no_type" : StandardPalette.secondary.value}
                colors.append(color)
            return colors

        def nv_class(self,view,graph):
            print("WARN:: Not implemented.")
            colors = []
            for node,data in view.nodes(data=True):
                colors.append({"standard" : StandardPalette.primary.value})
            return colors
        
        def type(self,view,graph):
            print("WARN:: Not implemented.")
            colors = []
            for node,data in view.nodes(data=True):
                colors.append({"standard" : StandardPalette.primary.value})
            return colors
        
        def role(self,view,graph):
            print("WARN:: Not implemented.")
            colors = []
            for node,data in view.nodes(data=True):
                colors.append({"standard" : StandardPalette.primary.value})
            return colors

        def genetic(self,view,graph):
            print("WARN:: Not implemented.")
            colors = []
            for node,data in view.nodes(data=True):
                colors.append({"standard" : StandardPalette.primary.value})
            return colors

        def hierarchy(self,view,graph):
            print("WARN:: Not implemented.")
            colors = []
            for node,data in view.nodes(data=True):
                colors.append({"standard" : StandardPalette.primary.value})
            return colors
            
        def collection(self,view,graph):
            print("WARN:: Not implemented.")
            colors = []
            for node,data in view.nodes(data=True):
                colors.append({"standard" : StandardPalette.primary.value})
            return colors




    class EdgeColorHandler:
        def __init__(self):
            pass

        def standard(self,view):
            return [{"standard" : "#888"} for e in view.edges]
        
        def nv_class(self,view):
            print("WARN:: Not Implemented")
            colors = []
            for n,v,k,e in view.edges(keys=True,data=True):
                colors.append({"standard" : "#888"})
            return colors
        
        def type(self,view):
            print("WARN:: Not Implemented")
            colors = []
            for n,v,k,e in view.edges(keys=True,data=True):
                colors.append({"standard" : "#888"})
            return colors