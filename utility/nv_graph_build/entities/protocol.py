from entities.abstract_entity import ConceptualEntity
from entities.instrument import Instrument
from entities.external_machine import ExternalMachine
from entities.container import Container
from entities.action import Action
from property import protocols as pp

class Protocol(ConceptualEntity):
    def __init__(self,properties=[],equivalents=[],restrictions=[]):
        p = properties + [pp.HasInstrument(Instrument),
                          pp.HasExternal(ExternalMachine),
                          pp.HasContainer(Container),
                          pp.Actions(Action)]
        super().__init__(properties=p,equivalents=equivalents,
                        restrictions=restrictions)