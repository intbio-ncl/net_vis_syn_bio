import argparse
from flask import Flask
from dashboards.sbol_dash import SBOLDash
from dashboards.results_dash import ResultDash
from dashboards.kg_dash import KnowledgeDash
assets_dir = "assets"


def process_input(filename,summary,knowledge):
    server = Flask(__name__)
    if summary:
        dashboard = ResultDash(__name__,server)
    elif knowledge:
        dashboard = KnowledgeDash(__name__,server)
    else:
        dashboard = SBOLDash(__name__,server)
    dashboard.load_graph(filename)

    dashboard.visualiser.set_single_module_view()
    dashboard.run()

def language_processor_args():
    parser = argparse.ArgumentParser(description="Network Visualisation Tool")
    parser.add_argument('filename', default=None, nargs='?',help="File to parse as Input")
    parser.add_argument('-s', '--summary', help="Renders Summary Dashboard.", default=None, action='store_true')
    parser.add_argument("-k", "--knowledge",help="For knowledge Graph", default=None, action='store_true')
    return  parser.parse_args()

if __name__ == "__main__":
    args = language_processor_args()
    process_input(args.filename,args.summary,args.knowledge)