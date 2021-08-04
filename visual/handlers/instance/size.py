from visual.handlers.abstract_size import AbstractSizeHandler
class SizeHandler(AbstractSizeHandler):
    def __init__(self):
        super().__init__()

    def hierarchy(self,builder):
        print("Warn:: Not implemented")
        sizes = []
        for node in builder.v_nodes():
            sizes.append(10)
        return sizes


    