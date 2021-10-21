from entities.abstract_entity import ConceptualEntity
from entities.instrument import Instrument
from entities.external_machine import ExternalMachine
from entities.container import Container
from entities.action import Action
from property import protocols as pp
from equivalent import protocol_equivalent as pe

class Protocol(ConceptualEntity):
    def __init__(self,properties=[],equivalents=[],restrictions=[]):
        if equivalents == []:
            e = [pe.ProtocolEquivalent()]
        else:
            e = equivalents
        p = properties + [pp.HasInstrument(Instrument),
                          pp.HasExternal(ExternalMachine),
                          pp.HasContainer(Container),
                          pp.Actions(Action)]
        super().__init__(properties=p,equivalents=e,
                        restrictions=restrictions)