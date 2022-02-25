def set_disconnected_mode(self):
    '''
    Only for multiple graph visualisation. 
    Seperates each input graph, i.e. doesn't connect graphs by common nodes.
    '''
    if self.mode == self.set_disconnected_mode:
        self._builder.set_disconnected_mode()
    else:
        self.mode = self.set_disconnected_mode