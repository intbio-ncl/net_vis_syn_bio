from property.property import Property

class HasInstrument(Property):
    def __init__(self,range):
        super().__init__(range)

class HasExternal(Property):
    def __init__(self,range):
        super().__init__(range)

class HasContainer(Property):
    def __init__(self,range):
        super().__init__(range)

class Actions(Property):
    def __init__(self,range):
        super().__init__(range=range)