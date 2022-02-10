from visual.handlers.abstract_size import AbstractSizeHandler
class SizeHandler(AbstractSizeHandler):
    def __init__(self,builder):
        super().__init__(builder)
        self._max_node_size = self._standard_node_size * 1.5
        self._modifier = 1.1

    def action(self):
        sizes = []
        nv_action = self._builder._model_graph.identifiers.objects.action
        nv_protocol = self._builder._model_graph.identifiers.objects.protocol
        for node,data in self._builder.v_nodes(data=True):
            rdf_type = self._builder.get_rdf_type(node)
            if rdf_type is None:
                sizes.append(int(self._standard_node_size / 2))
                continue
            
            rdf_type = rdf_type[1]["key"]
            if self._builder._model_graph.is_derived(rdf_type,nv_protocol):
                sizes.append(int(self._standard_node_size * self._modifier))
            elif self._builder._model_graph.is_derived(rdf_type,nv_action):
                sizes.append(self._standard_node_size)
            else:
                sizes.append(int(self._standard_node_size / 2))

        return sizes

    