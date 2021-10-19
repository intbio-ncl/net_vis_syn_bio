import networkx as nx
from opentrons.simulate import simulate, format_runlog
accepted_file_types = ['py']
def convert(filename,model_graph):
    graph = nx.MultiDiGraph()
    protocol_file = open(filename)
    runlog, _bundle = simulate(protocol_file)
    print(runlog)
    protocol_file.close()
    return graph

def dump(l):
    for e in l:
        for k,v in e.items():
            if not isinstance(v,dict):
                print(k,v)
            else:
                for k1,v1 in v.items():
                    print(k1,v1)