class ViewBuilder:
    def __init__(self,builder):
        self._builder = builder

    def full(self):
        return self._builder._graph