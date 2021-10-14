from visual.handlers.abstract_size import AbstractSizeHandler
class SizeHandler(AbstractSizeHandler):
    def __init__(self,builder):
        super().__init__(builder)
        self._max_node_size = self._standard_node_size * 1.5
        self._modifier = 1.1

    def hierarchy(self):
        node_sizes = []
        for node in self._builder.v_nodes():
            depth = self._builder.get_class_depth(node)
            if depth == 0:
                node_sizes.append(self._max_node_size)
            else:
                node_sizes.append(int(self._max_node_size / (depth * self._modifier)))
        return node_sizes




    