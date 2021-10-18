import argparse
import os
from flask import Flask

from dashboard.design import DesignDash
from dashboard.protocol import ProtocolDash
from dashboard.model import ModelDash
#from dashboard.result import ResultDash
assets_dir = "assets"
visual_modes = {"design" : [os.path.join("utility","nv_design.xml"),DesignDash],
                "protocol" : [os.path.join("utility","nv_protocol.xml"),ProtocolDash]}

def process_input(filename,v_type,summary,model):
    server = Flask(__name__)

    model_fn,dash = visual_modes[v_type]
    if model:
        dashboard = ModelDash(__name__,server)
        filename = model_fn
    else:
        dashboard = dash(__name__,server,model_fn)

    dashboard.load_graph(filename)
    server.run()

def language_processor_args():
    parser = argparse.ArgumentParser(description="Network Visualisation Tool")
    parser.add_argument('filename', default=None, nargs='?',help="File to parse as Input")
    parser.add_argument('--type', '-t', help='Set type of visualisation',
                        default=list(visual_modes.keys())[0],type=str,
                        choices=visual_modes.keys())

    parser.add_argument('-s', '--summary', help="Renders Summary Dashboard.", 
                        default=None, action='store_true')
    parser.add_argument('-m', '--model', help="Visualises the underlying data structure.", 
    default=None, action='store_true')
    return  parser.parse_args()

if __name__ == "__main__":
    args = language_processor_args()
    process_input(args.filename,args.type,args.summary,args.model)