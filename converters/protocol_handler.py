import networkx as nx
from opentrons.protocol_api.protocol_context import ProtocolContext

from converters.protocol import ot2_file_convert
from converters.protocol import nv_protocol_convert
from converters.protocol import autoprotocol_convert
from graph.protocol import ProtocolGraph

convert_dict = {"ot2-file" : ot2_file_convert,
                "nv-protocol"  : nv_protocol_convert,
                "autoprotocol" : autoprotocol_convert}

def convert(model_graph,filename=None,convert_type=None):
    if filename is None:
        return ProtocolGraph(nx.MultiDiGraph())
    if convert_type is None:
        convert_type = derive_convert_type(filename)
    graph = convert_dict[convert_type].convert(filename,model_graph)
    return ProtocolGraph(graph)

def get_converter_names():
    return list(convert_dict.keys())
    
def derive_convert_type(item):
    if item.lower().endswith(tuple(v.lower() for v in ot2_file_convert.accepted_file_types)):
        return "ot2-file"
    elif item.lower().endswith(tuple(v.lower() for v in nv_protocol_convert.accepted_file_types)):
        return "nv-protocol"
    elif item.lower().endswith(tuple(v.lower() for v in autoprotocol_convert.accepted_file_types)):
        return "autoprotocol"