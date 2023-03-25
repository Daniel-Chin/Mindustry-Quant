from typing import *

class Multipliable:
    def __init__(self, num=1) -> None:
        self.num = num

    def name(self):
        return self.__class__.__name__
    
    def __repr__(self) -> str:
        return f'{self.num : .1f} {self.name()},'
    
    def __mul__(self, other):
        return self.__class__(self.num * other)
    
    def __rmul__(self, other):
        return self.__mul__(other)

MM = Dict[Type[Multipliable], int]

def MMItem2Instance(x: Tuple[Type[Multipliable], int], /):
    MType, num = x
    return MType(num)

def merge(*mms: MM) -> MM:
    if len(mms) == 2:
        a, b = mms
        s: MM = {}
        for _type, num in [*a.items(), *b.items()]:
            s[_type] = s.get(_type, 0) + num
        return s
    return merge(merge(*mms[:2]), *mms[2:])

class Resource(Multipliable): pass

class Drillable23(Resource): pass
class Beryllium(Drillable23): pass
class Graphite(Drillable23): pass
class Sand(Resource): pass
class Tungsten(Resource): pass
class Silicon(Resource): pass
class Thorium(Resource): pass
class Carbide(Resource): pass
class SurgeAlloy(Resource): pass
class Hydrogen(Resource): pass
class Arkycite(Resource): pass
class Cyanogen(Resource): pass
class Heat(Resource): pass

class Source(Multipliable): 
    @staticmethod
    def inItems() -> MM:
        raise NotImplementedError()
    @staticmethod
    def outItems() -> Multipliable:
        raise NotImplementedError()

sourceOf: Dict[Type[Multipliable], Type[Source]] = {}
def register(SourceClass: Type[Source]):
    sourceOf[SourceClass.outItems().__class__] = SourceClass
    return SourceClass

@register
class GraphitePlasmaBore(Source):
    @staticmethod
    def inItems() -> MM:
        return {Hydrogen: .25}
    @staticmethod
    def outItems() -> Multipliable:
        return Graphite(.75 * 2.5)
@register
class BerylliumPlasmaBore(Source):
    @staticmethod
    def inItems() -> MM:
        return {Hydrogen: .25}
    @staticmethod
    def outItems() -> Multipliable:
        return Beryllium(.75 * 2.5)

@register
class SiliconArcFurnance(Source):
    @staticmethod
    def inItems() -> MM:
        return {Graphite: 1.2, Sand: 4.8}
    @staticmethod
    def outItems() -> Multipliable:
        return Silicon(4.8)

@register
class CarbideCrucible400(Source):
    @staticmethod
    def inItems() -> MM:
        return {
            Tungsten: .88 * 4, 
            Graphite: 1.33 * 4, 
            Heat: 10 * 4, 
        }
    @staticmethod
    def outItems() -> Multipliable:
        return Carbide(.44 * 4)

@register
class CyanogenSynthesizer400(Source):
    @staticmethod
    def inItems() -> MM:
        return {
            Arkycite: 40 * 4, 
            Graphite: .75 * 4, 
            Heat: 5 * 4, 
        }
    @staticmethod
    def outItems() -> Multipliable:
        return Cyanogen(3 * 4)

class Unit(Multipliable): pass

class LargeCarbideWall(Unit): pass

class Stell(Unit): pass
class Locus(Unit): pass
class Conquer(Unit): pass
class Elude(Unit): pass
class Avert(Unit): pass
class Disrupt(Unit): pass

@register
class CarbideConstructor(Source):
    build_time = 5
    @staticmethod
    def inItems() -> MM:
        return {
            Thorium: 24 / __class__.build_time, 
            Carbide: 24 / __class__.build_time, 
        }
    @staticmethod
    def outItems() -> Multipliable:
        return LargeCarbideWall(1 / __class__.build_time)

@register
class TankFabricator(Source):
    build_time = 35
    @staticmethod
    def inItems() -> MM:
        return {
            Beryllium: 40 / __class__.build_time, 
            Silicon: 50 / __class__.build_time, 
        }
    @staticmethod
    def outItems() -> Multipliable:
        return Stell(1 / __class__.build_time)

@register
class TankRefabricator(Source):
    build_time = 30
    @staticmethod
    def inItems() -> MM:
        return {
            Stell: 1 / __class__.build_time, 
            Hydrogen: 3, 
            Silicon: 1.33, 
            Tungsten: 1, 
        }
    @staticmethod
    def outItems() -> Multipliable:
        return Locus(1 / __class__.build_time)

@register
class TankAssembler(Source):
    build_time = 180
    @staticmethod
    def inItems() -> MM:
        return {
            Locus: 6 / __class__.build_time, 
            LargeCarbideWall: 20 / __class__.build_time, 
            Cyanogen: 9, 
        }
    @staticmethod
    def outItems() -> Multipliable:
        return Conquer(1 / __class__.build_time)

@register
class ShipFabricator(Source):
    build_time = 40
    @staticmethod
    def inItems() -> MM:
        return {
            Graphite: 50 / __class__.build_time, 
            Silicon: 70 / __class__.build_time, 
        }
    @staticmethod
    def outItems() -> Multipliable:
        return Elude(1 / __class__.build_time)

@register
class ShipRefabricator(Source):
    build_time = 50
    @staticmethod
    def inItems() -> MM:
        return {
            Elude: 1 / __class__.build_time, 
            Hydrogen: 3, 
            Silicon: 1.2, 
            Tungsten: .8, 
        }
    @staticmethod
    def outItems() -> Multipliable:
        return Avert(1 / __class__.build_time)

@register
class ShipAssembler(Source):
    build_time = 180
    @staticmethod
    def inItems() -> MM:
        return {
            Avert: 6 / __class__.build_time, 
            LargeCarbideWall: 20 / __class__.build_time, 
            Cyanogen: 12, 
        }
    @staticmethod
    def outItems() -> Multipliable:
        return Disrupt(1 / __class__.build_time)

def breakdown(x: Multipliable, /) -> MM:
    TX = type(x)
    try:
        SourceType = sourceOf[TX]
    except KeyError:
        return {TX: x.num}
    else:
        scale = x.num / SourceType.outItems().num
        mm = merge(
            {SourceType: scale}, 
            *[
                {MType: num * scale} 
                for (MType, num) in SourceType.inItems().items()
            ],
        )
        return merge(*map(breakdown, map(
            MMItem2Instance, mm.items(), 
        )))

def displayMM(x: MM, /):
    print('{', *map(MMItem2Instance, x.items()), sep='\n  ')
    print('}')

# print('One full-time', ShipAssembler.__name__, 'needs (/sec):')
# displayMM(breakdown(Disrupt(1 / ShipAssembler.build_time)))

print('One full-time', TankAssembler.__name__, 'needs (/sec):')
displayMM(breakdown(Conquer(1 / TankAssembler.build_time)))

from console import console
console(globals())
