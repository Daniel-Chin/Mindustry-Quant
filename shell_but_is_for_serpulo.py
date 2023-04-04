from abc import ABCMeta, abstractstaticmethod

from shell import *

class Drillable22(Resource): pass

class Copper(Drillable22): pass
class Lead(Drillable22): pass
class Titanium(Drillable22): pass
class Coal(Drillable22): pass
class Sand(Drillable22): pass
class Pyratite(Resource): pass

class PneumaticDrill(Source, metaclass=ABCMeta):
    @abstractstaticmethod
    def drills() -> Type[Resource]:
        raise NotImplemented()
    @staticmethod
    def inItems() -> MM:
        return { }
    @classmethod
    def outItems(cls) -> Multipliable:
        return cls.drills()(.6)
@register
class CopperPneumaticDrill(PneumaticDrill):
    def drills() -> Type[Resource]:
        return Copper
@register
class LeadPneumaticDrill(PneumaticDrill):
    def drills() -> Type[Resource]:
        return Lead
@register
class TitaniumPneumaticDrill(PneumaticDrill):
    def drills() -> Type[Resource]:
        return Titanium
@register
class SandPneumaticDrill(PneumaticDrill):
    def drills() -> Type[Resource]:
        return Sand
@register
class CoalPneumaticDrill(PneumaticDrill):
    def drills() -> Type[Resource]:
        return Coal

@register # overwrites
class SurgeSmelter(Source):
    @staticmethod
    def inItems() -> MM:
        return {
            Copper: 2.4, 
            Lead: 3.2, 
            Titanium: 1.6, 
            Silicon: 2.4, 
        }
    @staticmethod
    def outItems() -> Multipliable:
        return SurgeAlloy(.8)

@register # overwrites
class SiliconCrucible(Source):
    @staticmethod
    def inItems() -> MM:
        return {
            Coal: 2.66, 
            Sand: 4, 
            Pyratite: .66, 
        }
    @staticmethod
    def outItems() -> Multipliable:
        return Silicon(5.33)

@register
class PyratiteMixer(Source):
    @staticmethod
    def inItems() -> MM:
        return {
            Coal: .75, 
            Lead: 1.5, 
            Sand: 1.5, 
        }
    @staticmethod
    def outItems() -> Multipliable:
        return Pyratite(.75)

if __name__ == '__main__':
    fullTime(SurgeSmelter)

    try:
        from console import console
    except ImportError:
        import IPython
        IPython.embed()
    else:
        console(globals())
