from builder.builders.abstract_view import AbstractViewBuilder

class ViewBuilder(AbstractViewBuilder):
    def __init__(self,builder):
        super().__init__(builder)

    
    def heirarchy(self):

        for e in self._builder.get_sub_classes():
            print(e)

        '''
        for n,v,k,e in self._builder.edges(data=True,keys=True):
            print(n,v,k,e)
        '''



