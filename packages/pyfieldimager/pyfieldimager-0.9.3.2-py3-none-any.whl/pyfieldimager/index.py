from enum import Enum


class BandIndex(Enum):

    Red = 1
    Green = 2
    Blue = 3
    ALPHA = 4

    R = 1
    G = 2
    B = 3
    A = 4
    
    NIR = 5
    SWIR = 6
    FIR = 7

    RE = 8

    @classmethod
    def list(cls):
        return list(map(lambda c: c.name, cls))
    

    @classmethod
    def get(cls, name):
        return cls[name].value
    

class HSVIndex(Enum):

    Hue = -1
    Saturation = -2
    Value = Brightness = -3

    H = -1
    S = -2
    V = -3

    @classmethod
    def list(cls):
        return list(map(lambda c: c.name, cls))
    

    @classmethod
    def get(cls, name):
        return cls[name].value
    

'''
vegetation indecies

cf. https://www.opendronemap.org/fieldimager/#p6
'''
class FieldIndex(Enum):

    BI = 1
    SCI = 2
    GLI = 3
    HI = 4
    NGRDI = 5
    GRDI = 5
    GRVI = 5
    SI = 6
    VARI = 7
    HUE = 8
    BGI = 9
    PSRI = 10
    NDVI = 11
    GNDVI = 12
    RVI = 13
    NDRE = 14
    TVI = 15
    CVI = 16
    EVI = 17
    CIG = 18
    CIRE = 19
    DVI = 20


    @classmethod
    def list(cls):
        return list(map(lambda c: c.name, cls))
    

    @classmethod
    def get(cls, name):
        return cls[name].value
    
