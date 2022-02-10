from graph.abstract import AbstractGraph

class DesignGraph(AbstractGraph):
    def __init__(self,graph):
        super().__init__(graph)
        self._generate_labels()
        



