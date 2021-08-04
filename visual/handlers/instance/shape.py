from visual.handlers.abstract_shape import AbstractNodeShapeHandler,AbstractEdgeShapeHandler

class ShapeHandler:
    def __init__(self):
        self.node = self.NodeShapeHandler()
        self.edge = self.EdgeShapeHandler()


    class NodeShapeHandler(AbstractNodeShapeHandler):
        def __init__(self):
            super().__init__()

            
    class EdgeShapeHandler(AbstractEdgeShapeHandler):
        def __init__(self):
            super().__init__()
