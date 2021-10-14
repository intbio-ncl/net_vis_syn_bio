import argparse
import os
from flask import Flask

from dashboard.instance import InstanceDash
from dashboard.model import ModelDash
from dashboard.result import ResultDash
assets_dir = "assets"
model_fn = os.path.join("utility","nv_model.xml")
def process_input(filename,summary,model):
    server = Flask(__name__)

    if model:
        dashboard = ModelDash(__name__,server)
        filename = model_fn
    elif summary:
        dashboard = ResultDash(__name__,server,model_fn)
    else:
        dashboard = InstanceDash(__name__,server,model_fn)
    dashboard.load_graph(filename)
    server.run()

def language_processor_args():
    parser = argparse.ArgumentParser(description="Network Visualisation Tool")
    parser.add_argument('filename', default=None, nargs='?',help="File to parse as Input")
    parser.add_argument('-s', '--summary', help="Renders Summary Dashboard.", default=None, action='store_true')
    parser.add_argument('-m', '--model', help="Visualises the underlying data structure..", default=None, action='store_true')
    return  parser.parse_args()

if __name__ == "__main__":
    args = language_processor_args()
    process_input(args.filename,args.summary,args.model)