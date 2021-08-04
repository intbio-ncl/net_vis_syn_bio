from visual.handlers.abstract_label import AbstractNodeLabelHandler , AbstractEdgeLabelHandler

class LabelHandler:
    def __init__(self):
        self.node = self.NodeLabelHandler()
        self.edge = self.EdgeLabelHandler()
    

    class NodeLabelHandler(AbstractNodeLabelHandler):
        def __init__(self):
            super().__init__()

        def role(self,builder):
            role_names = []
            for node,data in builder.v_nodes(data=True):
                roles = builder.get_roles(node)
                if builder.get_role(node) == []:
                    role_names.append("No Role")
                else:
                    name = ""#identifiers.translate_roles(data["key"])
                    role_names.append(name)
            return role_names

    class EdgeLabelHandler(AbstractEdgeLabelHandler):
        def __init__(self):
            super().__init__()
        