from converters import converter
class NVBuilder:
    def __init__(self,graph):
        self._graph = converter.convert(graph)

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

    def produce_pruned_graph(self):
        edges = []
        node_attrs = {}
        graph = self._graph.sub_graph(edges,node_attrs)
        return graph
         
    def produce_heirarchy_graph(self):
        edges = []
        node_attrs = {}
        graph = self._graph.sub_graph(edges,node_attrs)
        return graph
    def produce_components_graph(self):
        edges = []
        node_attrs = {}
        graph = self._graph.sub_graph(edges,node_attrs)
        return graph

    def produce_interaction_verbose_graph(self):
        edges = []
        node_attrs = {}
        graph = self._graph.sub_graph(edges,node_attrs)
        return graph

    def produce_interaction_graph(self):
        edges = []
        node_attrs = {}
        graph = self._graph.sub_graph(edges,node_attrs)
        return graph

    def produce_genetic_interaction_graph(self):
        edges = []
        node_attrs = {}
        graph = self._graph.sub_graph(edges,node_attrs)
        return graph
    def produce_protein_protein_interaction_graph(self):
        edges = []
        node_attrs = {}
        graph = self._graph.sub_graph(edges,node_attrs)
        return graph

    def produce_module_graph(self):
        edges = []
        node_attrs = {}
        graph = self._graph.sub_graph(edges,node_attrs)
        return graph
                                              
    def produce_maps_graph(self):
        edges = []
        node_attrs = {}
        graph = self._graph.sub_graph(edges,node_attrs)
        return graph