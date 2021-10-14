import networkx as nx
from converters.sbol import convert as sbol_convert
from converters.nv import convert as nv_convert
from converters.gbk import convert as gbk_convert
from graph.instance import InstanceGraph

convert_dict = {"sbol" : sbol_convert,
                "gbk"  : gbk_convert, # Not Implemented..
                "nv"   : nv_convert}

def convert(model_graph,filename=None,convert_type=None):
    if filename is None:
        return InstanceGraph(nx.MultiDiGraph())
    if convert_type is None:
        convert_type = derive_convert_type(filename)
    graph = convert_dict[convert_type].convert(filename,model_graph)
    return InstanceGraph(graph)

def get_converter_names():
    return list(convert_dict.keys())
    
def derive_convert_type(filename):
    if filename.lower().endswith(tuple(v.lower() for v in sbol_convert.accepted_file_types)):
        return "sbol"
    elif filename.lower().endswith(tuple(v.lower() for v in gbk_convert.accepted_file_types)):
        return 'gbk'
    elif filename.lower().endswith(tuple(v.lower() for v in nv_convert.accepted_file_types)):
        return "nv"