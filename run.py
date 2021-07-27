import argparse
from flask import Flask
from dashboard.full_dash import NVFullDash
from dashboard.result_dash import NVResultDash
assets_dir = "assets"
def process_input(filename,summary):
    server = Flask(__name__)

    if summary:
        dashboard = NVResultDash(__name__,server)
    else:
        dashboard = NVFullDash(__name__,server)
    dashboard.load_graph(filename)
    server.run()

def language_processor_args():
    parser = argparse.ArgumentParser(description="Network Visualisation Tool")
    parser.add_argument('filename', default=None, nargs='?',help="File to parse as Input")
    parser.add_argument('-s', '--summary', help="Renders Summary Dashboard.", default=None, action='store_true')
    return  parser.parse_args()

if __name__ == "__main__":
    args = language_processor_args()
    process_input(args.filename,args.summary)