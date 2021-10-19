import re
from visual.handlers.abstract_color import AbstractNodeColorHandler
from visual.handlers.abstract_color import AbstractEdgeColorHandler

class ColorHandler():
    def __init__(self,builder):
        self.node = self.NodeColorHandler(builder)
        self.edge = self.EdgeColorHandler(builder)

    class NodeColorHandler(AbstractNodeColorHandler):
        def __init__(self,builder):
            super().__init__(builder)
        
    class EdgeColorHandler(AbstractEdgeColorHandler):
        def __init__(self,builder):
            super().__init__(builder)