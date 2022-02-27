def set_connected_mode(self):
    '''
    Only for multiple graph visualisation. 
    Connects graphs by merging duplicate nodes between graphs.
    '''
    if self.mode == self.set_connected_mode:
        self._builder.set_connected_mode()
    else:
        self.mode = self.set_connected_mode