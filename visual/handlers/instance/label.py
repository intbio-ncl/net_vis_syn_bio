from visual.handlers.abstract_label import AbstractNodeLabelHandler , AbstractEdgeLabelHandler

class LabelHandler:
    def __init__(self,builder):
        self.node = self.NodeLabelHandler(builder)
        self.edge = self.EdgeLabelHandler(builder)
    

    class NodeLabelHandler(AbstractNodeLabelHandler):
        def __init__(self,builder):
            super().__init__(builder)

        def role(self):
            role_names = []
            for node,data in self._builder.v_nodes(data=True):
                roles = self._builder.get_roles(node)
                if self._builder.get_role(node) == []:
                    role_names.append("No Role")
                else:
                    name = ""#identifiers.translate_roles(data["key"])
                    role_names.append(name)
            return role_names

    class EdgeLabelHandler(AbstractEdgeLabelHandler):
        def __init__(self,builder):
            super().__init__(builder)
        