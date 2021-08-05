color_list = [
        "#7DF5DF",
        "#86E078",
        "#8C5EE0",
        "#FF675D",
        "#FAC57D",
        "#25CCF7",
        "#CAD3C8",
        "#1B9CFC",
        "#F8EFBA",
        "#58B19F",
        "#2C3A47",
        "#B33771",
        "#3B3B98",
        "#D6A2E8",
        "#6D214F",
        "#BDC581",
        "#EAB543",
        "#FEA47F",
        "#FC427B",
        "#F97F51",]
    

class AbstractNodeColorHandler:
    def __init__(self,builder):
        self._builder = builder
        self._color_list = color_list
    
    def standard(self):
        return [{"standard" : color_list[0]} for node in self._builder.v_nodes()]

    def rdf_type(self):
        colors = []
        for node,data in self._builder.v_nodes(data=True):
            if self._builder.get_rdf_type(node) is not None:
                color = {"rdf_type" : color_list[0]}
            else:
                color = {"no_type" : color_list[1]}
            colors.append(color)
        return colors
    
class AbstractEdgeColorHandler:
    def __init__(self,builder):
        self._builder = builder

    def standard(self):
        return [{"standard" : "#888"} for e in self._builder.v_edges]
    

    