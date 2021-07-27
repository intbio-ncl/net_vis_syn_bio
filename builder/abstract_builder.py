class AbstractBuilder:
    def __init__(self):
        pass

    @property
    def nodes(self):
        return self._graph.nodes
    @property
    def edges(self):
        return self._graph.edges

    @property
    def graph(self):
        return self._graph
        
    @graph.setter
    def graph(self,graph):
        self._graph = graph
        
    def produce_full_graph(self):
        return self._graph

    def produce_tree(self):
        return self._graph.get_tree()

    def produce_network(self):
        return self._graph.get_network()
