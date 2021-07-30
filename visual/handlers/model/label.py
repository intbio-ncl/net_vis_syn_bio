from visual.handlers.abstract_label import AbstractNodeLabelHandler , AbstractEdgeLabelHandler

class LabelHandler:
    def __init__(self):
        self.node = self.NodeLabelHandler()
        self.edge = self.EdgeLabelHandler()
    

    class NodeLabelHandler(AbstractNodeLabelHandler):
        def __init__(self):
            super().__init__()

    class EdgeLabelHandler(AbstractEdgeLabelHandler):
        def __init__(self):
            super().__init__()
        