class ViewBuilder:
    def __init__(self,graph):
        self._graph = graph

    def full(self):
        return self._graph

    def pruned(self):
        edges = []
        node_attrs = {}
        self.view = self._graph.sub_graph(edges,node_attrs)
         
    def heirarchy(self):
        edges = []
        node_attrs = {}
        self.view = self._graph.sub_graph(edges,node_attrs)

    def components(self):
        edges = []
        node_attrs = {}
        self.view = self._graph.sub_graph(edges,node_attrs)

    def interaction_verbose(self):
        edges = []
        node_attrs = {}
        self.view = self._graph.sub_graph(edges,node_attrs)

    def interaction(self):
        edges = []
        node_attrs = {}
        self.view = self._graph.sub_graph(edges,node_attrs)

    def genetic_interaction(self):
        edges = []
        node_attrs = {}
        self.view = self._graph.sub_graph(edges,node_attrs)

    def protein_protein_interaction(self):
        edges = []
        node_attrs = {}
        self.view = self._graph.sub_graph(edges,node_attrs)

    def module(self):
        edges = []
        node_attrs = {}
        self.view = self._graph.sub_graph(edges,node_attrs)
                                              
    def maps(self):
        edges = []
        node_attrs = {}
        self.view = self._graph.sub_graph(edges,node_attrs)