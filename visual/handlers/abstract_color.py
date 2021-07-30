from visual.handlers.color_palettes import StandardPalette

class AbstractNodeColorHandler:
    def __init__(self):
        pass
    
    def standard(self,builder):
        return [{"standard" : StandardPalette.primary.value} for node in builder.v_nodes()]

    def rdf_type(self,builder):
        colors = []
        for node,data in builder.v_nodes(data=True):
            if builder.get_rdf_type(node) is not None:
                color = {"rdf_type" : StandardPalette.primary.value}
            else:
                color = {"no_type" : StandardPalette.secondary.value}
            colors.append(color)
        return colors

    def nv_class(self,builder):
        print("WARN:: Not implemented.")
        colors = []
        for node,data in builder.v_nodes(data=True):
            colors.append({"standard" : StandardPalette.primary.value})
        return colors
    
class AbstractEdgeColorHandler:
    def __init__(self):
        pass

    def standard(self,builder):
        return [{"standard" : "#888"} for e in builder.v_edges]
    
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