# Network Visualiser SynBio

A tool focused on visualising common data within Synthetic Biology projects via a network-centric view.

* Tailor the representation based on your requirements.
* Share data with a multi-disciplined team.

## Get Started

### Dependencies

NV-SB requires Python 3.x. and Python package dependencies are listed in `requirements.txt`.

### Install

1. Download or clone repository. `git clone https://github.com/intbio-ncl/net_vis_syn_bio`
2. Navigate to your install directory
3. Install dependencies with `python -m pip install -r requirements.txt`


### Example usage

1. To visualise genetic designs:
    - Valid Files: 
        - SBOL (Recommended)
        - GBK.
    - To execute: `python run.py <filename>`
    - To View: Open browser and enter: `http://127.0.0.1:5000/design/`

2. To visualise build protocols:
    - Valid Files: 
        - Autoprotocol (Recommended)
        - OT2 Script.
    To execute: `python run.py <filename> -t protocol`
    To View: Open browser and enter: `http://127.0.0.1:5000/protocol/`

### Loading the application
To see an exhaustive list of inputs: `python run.py -h`

### Using the application
 - Once the application is loaded, all commands are located on the left of the screen.
 - A help button is located below the title, which provides information on a given command.
 - An advanced input button is located next to the help button, allowing for more control over layouts.
 - Below are views - selecting specific information within a large dataset to provide a predefined perspective. 
 - Below are the layouts - Provide nodes with spatial coordinates. Note: Node positions can be manually changed by dragging individual nodes or groups of nodes with CTRL + click.
 - Data can be exported as a static image (PNG, JPG or SVG) or as standard graph formats such as GML, GEXF, graphml.
 - All remaining options are purely visual manipulations focused on highlighting attributes.



