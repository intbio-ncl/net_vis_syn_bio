from visual.handlers.abstract_size import AbstractSizeHandler
class SizeHandler(AbstractSizeHandler):
    def __init__(self,builder):
        super().__init__(builder)

    def hierarchy(self):
        print("Warn:: Not implemented")
        sizes = []
        for node in self._builder.v_nodes():
            sizes.append(10)
        return sizes


    