from visual.handlers.color_palettes import StandardPalette
from visual.handlers.abstract_color import AbstractNodeColorHandler , AbstractEdgeColorHandler

class ColorHandler():
    def __init__(self):
        self.node = self.NodeColorHandler()
        self.edge = self.EdgeColorHandler()

    class NodeColorHandler(AbstractNodeColorHandler):
        def __init__(self):
            super().__init__()
            


    class EdgeColorHandler(AbstractEdgeColorHandler):
        def __init__(self):
            super().__init__()
        
