import networkx as nx
from opentrons.simulate import simulate, format_runlog
from opentrons.protocol_api.labware import Well,Location

accepted_file_types = ['py']
def convert(filename,model_graph):
    graph = nx.MultiDiGraph()
    protocol_file = open(filename)
    runlog, _bundle = simulate(protocol_file)
    objects,actions =_generalise(runlog)

    print("\n\n") 
    for k,v in objects.items():
        print(k,v)
    print("\n")
    for action in actions:
        for k,v in action.items():
            print(k,v)
        print("\n")
    protocol_file.close()
    return graph

def _generalise(runlog):
    objects = {}
    actions = []
    _dump(runlog)
    for operation in runlog:
        instrument = None
        source = None
        destination = None
        volume = None

        level = operation["level"]
        payload = operation["payload"]
        instrument = payload["instrument"]
        instrument = instrument.name
        if instrument not in objects:
            objects[instrument] = {"type" : "PIPETTE"}
        if "location" in payload:
            location = payload["location"]
            if isinstance(location,Location):
                location = location.labware.object
            if isinstance(location,Well):
                if location.well_name not in objects:
                    objects[location.display_name] = {"type" : "WELL","parent" : location.parent}

        if "locations" in payload:
            locations = payload["locations"]
        if "volume" in payload:
            volume = payload["volume"]
        if "source" in payload:
            source = payload["source"]
        if "dest" in payload:
            destination = payload["dest"]

        if source is None and destination is None:
            source,destination,action = _determine_action(payload["text"],location)


        action = {"instrument" : instrument,"source" : source,"destination" : destination, "action":action, "volume" : volume}

        actions.append(action)
    return objects,actions

def _determine_action(text,name):
    '''
    Very hacky, can't find another way of 
    determining if something is being pulled or pushed.
    '''
    d_dict = {"picking"    : [name,None,"pipette_pick"],
              "dropping"   : [None,name,"pipette_drop"],
              "aspirating" : [name,None,"pipette_asp"],
              "dispensing" : [None,name,"pipette_disp"]}

    return d_dict[name]

def _dump(runlog):
    for operation in runlog:
        print(operation)
        level = operation["level"]
        payload = operation["payload"]
        instrument = payload["instrument"]

        name = instrument.name
        print(name)

        if "location" in payload:
            location = payload["location"]
            print(f'Location: {location}')
            if isinstance(location,Location):
                location = location.labware.object
            if isinstance(location,Well):
                print(location.display_name)
                print(location.parent)

        if "locations" in payload:
            locations = payload["locations"]
            print(f'Locations: {locations} {type(locations)}')
        if "volume" in payload:
            volume = payload["volume"]
            print(f'Volume: {volume} {type(volume)}')
        if "source" in payload:
            source = payload["source"]
            print(f'Source: {source} {type(source)}')
        if "dest" in payload:
            dest = payload["dest"]
            print(f'Dest: {dest} {type(dest)}')

        print("\n")
