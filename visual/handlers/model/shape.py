from visual.handlers.abstract_shape import AbstractNodeShapeHandler,AbstractEdgeShapeHandler
from rdflib import OWL

class ShapeHandler:
    def __init__(self,builder):
        self.node = self.NodeShapeHandler(builder)
        self.edge = self.EdgeShapeHandler()


    class NodeShapeHandler(AbstractNodeShapeHandler):
        def __init__(self,builder):
            super().__init__(builder)
        
        def logical(self):
            shapes = []
            shape_map = {OWL.intersectionOf : {"AND" : "rectangle"},
                         OWL.unionOf    : {"OR"  : "triangle"}}

            for node in self._builder.v_nodes():
                n_data = self._builder.v_nodes[node]
                try:
                    shapes.append(shape_map[n_data["key"]])
                except KeyError:
                    shapes.append({"not_logical" : "circle"})    
            return shapes
                            
    class EdgeShapeHandler(AbstractEdgeShapeHandler):
        def __init__(self):
            super().__init__()
