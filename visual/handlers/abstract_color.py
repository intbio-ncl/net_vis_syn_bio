from visual.handlers.color_producer import build_color
    
class AbstractNodeColorHandler:
    def __init__(self,builder):
        self._builder = builder
        self._color_picker = build_color()
    
    def standard(self):
        return [{"standard" : self._color_picker[0]} for node in self._builder.v_nodes()]

    def rdf_type(self):
        colors = []
        for node,data in self._builder.v_nodes(data=True):
            if self._builder.get_rdf_type(node) is not None:
                color = {"rdf_type" : self._color_picker[0]}
            else:
                color = {"no_type" : self._color_picker[1]}
            colors.append(color)
        return colors
    
class AbstractEdgeColorHandler:
    def __init__(self,builder):
        self._builder = builder

    def standard(self):
        return [{"standard" : "#888"} for e in self._builder.v_edges]
    

    