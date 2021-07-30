import networkx as nx
class AbstractLayoutHandler:
    def __init__(self):
        pass
    
    def spring(self,graph):
        return nx.spring_layout(graph, iterations=200)

    def circular(self,graph):
        return nx.circular_layout(graph)
    
    def kamada_kawai(self,graph):
        return nx.kamada_kawai_layout(graph)
    
    def planar(self,graph):
        return nx.planar_layout(graph)

    def none(self):
        return {"name" : "preset"}

    def concentric(self):
        return {"name" : "concentric"}
    
    def breadthfirst(self):
        return {"name" : "breadthfirst",
                "directed": True}
    
    def cose(self):
        return {"name" : "cose",
                'idealEdgeLength': 100,
                'nodeOverlap': 20,
                'refresh': 20,
                'fit': True,
                'padding': 30,
                'randomize': False,
                'componentSpacing': 100,
                'nodeRepulsion': 400000,
                'edgeElasticity': 100,
                'nestingFactor': 5,
                'gravity': 80,
                'numIter': 1000,
                'initialTemp': 200,
                'coolingFactor': 0.95,
                'minTemp': 1.0}
    
    def cose_bilkent(self):
        return {"name" : "cose-bilkent"}
        
    def cola(self):
        return {"name" : "cola"}

    def euler(self):
        return {"name" : "euler"}
    
    def spread(self):
         return {"name" : "spread"}
    
    def dagre(self):
        return {"name" : "dagre"}
    
    def klay(self):
        return {"name" : "klay"}
    
    def grid(self):
        return {"name" : "grid"}
    