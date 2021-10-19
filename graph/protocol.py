from graph.abstract import AbstractGraph

class ProtocolGraph(AbstractGraph):
    def __init__(self,graph):
        super().__init__(graph)
        self._generate_labels()
        



