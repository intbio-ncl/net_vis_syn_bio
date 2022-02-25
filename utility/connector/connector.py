from utility.connector.sbol_connector.connector import SBOLConnector

sbol_connector = SBOLConnector()
def can_connect(filename):
    if sbol_connector.can_connect(filename):
        return True
    return False

def connect(filename):
    graph = sbol_connector.connect(filename)
    new_fn = filename.split(".")[0] + "_connected.xml"
    graph.save(new_fn)
    return new_fn