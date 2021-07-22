from visual.handlers.color_palettes import StandardPalette

class ColorHandler:
    def __init__(self):
        self.node = self.NodeColorHandler()
        self.edge = self.EdgeColorHandler()

    class NodeColorHandler:
        def __init__(self):
            pass
        
        def standard(self,builder):
            return [{"standard" : StandardPalette.primary.value} for node in builder.nodes()]

        def rdf_type(self,builder):
            colors = []
            for node,data in builder.nodes(data=True):
                if builder.get_rdf_type(node) is not None:
                    color = {"rdf_type" : StandardPalette.primary.value}
                else:
                    color = {"no_type" : StandardPalette.secondary.value}
                colors.append(color)
            return colors

        def nv_class(self,builder):
            print("WARN:: Not implemented.")
            colors = []
            for node,data in builder.nodes(data=True):
                colors.append({"standard" : StandardPalette.primary.value})
            return colors
        
        def type(self,builder):
            print("WARN:: Not implemented.")
            colors = []
            for node,data in builder.nodes(data=True):
                colors.append({"standard" : StandardPalette.primary.value})
            return colors
        
        def role(self,builder):
            print("WARN:: Not implemented.")
            colors = []
            for node,data in builder.nodes(data=True):
                colors.append({"standard" : StandardPalette.primary.value})
            return colors

        def genetic(self,builder):
            print("WARN:: Not implemented.")
            colors = []
            for node,data in builder.nodes(data=True):
                colors.append({"standard" : StandardPalette.primary.value})
            return colors

        def hierarchy(self,builder):
            print("WARN:: Not implemented.")
            colors = []
            for node,data in builder.nodes(data=True):
                colors.append({"standard" : StandardPalette.primary.value})
            return colors
            
        def collection(self,builder):
            print("WARN:: Not implemented.")
            colors = []
            for node,data in builder.nodes(data=True):
                colors.append({"standard" : StandardPalette.primary.value})
            return colors

    class EdgeColorHandler:
        def __init__(self):
            pass

        def standard(self,builder):
            return [{"standard" : "#888"} for e in builder.edges]
        
        def nv_class(self,builder):
            print("WARN:: Not Implemented")
            colors = []
            for n,v,k,e in builder.edges(keys=True,data=True):
                colors.append({"standard" : "#888"})
            return colors
        
        def type(self,builder):
            print("WARN:: Not Implemented")
            colors = []
            for n,v,k,e in builder.edges(keys=True,data=True):
                colors.append({"standard" : "#888"})
            return colors