
def set_key_connect(self):
    '''
    Connects nodes and edges based on full URI
    '''
    self._builder.connect_label = "key"

def set_display_name_connect(self):
    '''
    Connects nodes and edges based on display name
    '''
    self._builder.connect_label = "display_name"

def set_intersection_preset(self):
    '''
    Pre-set methods with an affinity for displaying the intersection between graphs.
    '''
    preset_functions = [self.set_connected_mode,
                        self.set_intersection_view,
                        self.set_cose_layout,
                        self.add_type_node_color,
                        self.add_type_edge_color,
                        self.add_node_name_labels, 
                        self.add_edge_no_labels,
                        self.add_standard_node_size,
                        self.set_circle_node_shape,
                        self.set_bezier_edge_shape]
    return self._set_preset(preset_functions)


def set_difference_preset(self):
    '''
    Pre-set methods with an affinity for displaying the difference between graphs.
    '''
    preset_functions = [self.set_network_mode,
                        self.set_difference_view,
                        self.set_cose_layout,
                        self.add_type_node_color,
                        self.add_type_edge_color,
                        self.add_node_name_labels, 
                        self.add_edge_no_labels,
                        self.add_standard_node_size,
                        self.set_circle_node_shape,
                        self.set_bezier_edge_shape]
    return self._set_preset(preset_functions)

def set_connected_mode(self):
    '''
    Only for multiple graph visualisation. 
    Connects graphs by merging duplicate nodes between graphs.
    '''
    if self.mode == self.set_connected_mode:
        self._builder.set_connected_mode()
    else:
        self.mode = self.set_connected_mode

def set_difference_view(self):
    '''
    Only for multiple graph visualisation. 
    Visualised the difference between Graphs. 
    I.e. where common nodes and edges are removed. 
    '''
    if self.view == self.set_difference_view:
        self._builder.set_difference_view()
    else:
        self.view = self.set_difference_view

def set_intersection_view(self):
    '''
    Only for multiple graph visualisation. 
    Visualised the intersection between Graphs. 
    I.e. where non common nodes and edges are removed. 
    '''
    if self.view == self.set_intersection_view:
        self._builder.set_intersection_view()
    else:
        self.view = self.set_intersection_view