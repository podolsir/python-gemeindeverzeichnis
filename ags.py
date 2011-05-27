# coding: utf-8
from codecs import open
from datetime import date

Kreis_KreisfreieStadt = 41
Kreis_Stadtkreis = 42
Kreis = 43
Landkreis = 44
Regionalverband = 45

VerbandsfreieGemeinde = 50
Amt = 51
Samtgemeinde = 52
Verbandsgemeinde = 53
Verwaltungsgemeinschaft = 54
Kirchspielslandgemeinde = 55
Verwaltungsverband = 56
VGTraegermodell = 57
ErfuellendeGemeinde = 68

Markt = 60
Gemeinde_KreisfreieStadt = 61
Gemeinde_Stadtkreis = 62
Stadt = 63
KreisangehoerigeGemeinde = 64
GemeindefreiesGebietBewohnt = 65
GemeindefreiesGebietUnbewohnt = 66
GrosseKreisstadt = 67
AmtsangehoerigeGemeinde = 68
AmtsfreieGemeinde = 69

_kreistypen = {
    41: u'Kreisfreie Stadt',
    42: u'Stadtkreis',
    43: u'Kreis',
    44: u'Landkreis',
    45: u'Regionalverband',
}

_verbandtypen = {
    50: u'Verbandsfreie Gemeinde',
    51: u'Amt',
    52: u'Samtgemeinde',
    53: u'Verbandsgemeinde',
    54: u'Verwaltungsgemeinschaft',
    55: u'Kirchspielslandgemeinde',
    56: u'Verwaltungsverband',
    57: u'VG Trägermodell',
    58: u'Erfüllende Gemeinde',
}

_gemeindetypen = {
    60: u'Markt',
    61: u'Kreisfreie Stadt',
    62: u'Stadtkreis',
    63: u'Stadt',
    64: u'Kreisangehörige Gemeinde',
    65: u'gemeindefreies Gebiet, bewohnt',
    66: u'gemeindefreies Gebiet, unbewohnt',
    67: u'große Kreisstadt',
    68: u'Amtsangehörige Gemeinde',
    69: u'Amtsfreie Gemeinde',
}

def kreistyp_string(typ):
    if typ in _kreistypen:
        return _kreistypen[typ]
    return None

def verbandstyp_string(typ):
    if typ in _verbandtypen:
        return _verbandtypen[typ]
    return None

def gemeindetyp_string(typ):
    if typ in _gemeindetypen:
        return _gemeindetypen[typ]
    return None

class ARSObject(object):
    def __init__(self, ags=None, ars=None, gebietsstand=None):
        self.ags = ags
        self.ars = ars
        self.gebietsstand = gebietsstand

class Land(ARSObject):
    def __init__(self, ars=None, gebietsstand=None, 
                 name=None, sitz_landesregierung=None):
        ARSObject.__init__(self, ars, ars, gebietsstand)
        self.name = name
        self.sitz_landesregierung = sitz_landesregierung

    def __repr__(self):
        return "<Land: %r %r %r>" % (self.ars, self.name, self.sitz_landesregierung)

class Regierungsbezirk(ARSObject):
    def __init__(self, ars=None, gebietsstand=None, 
                 name=None, sitz_verwaltung=None):
        ARSObject.__init__(self, ars, ars, gebietsstand)
        self.name = name
        self.sitz_verwaltung = sitz_verwaltung

    def __repr__(self):
        return "<Regierungsbezirk: %r %r %r>" % (self.ars, self.name, self.sitz_verwaltung)

class Region(ARSObject):
    def __init__(self, ars=None, gebietsstand=None, 
                 name=None, sitz_verwaltung=None):
        ARSObject.__init__(self, ars, ars, gebietsstand)
        self.name = name
        self.sitz_verwaltung = sitz_verwaltung

    def __repr__(self):
        return "<Region: %r %r %r>" % (self.ars, self.name, self.sitz_verwaltung)

class Kreis(ARSObject):
    def __init__(self, ars=None, gebietsstand=None, 
                 name=None, sitz_verwaltung=None, typ=None):
        ARSObject.__init__(self, ars, ars, gebietsstand)
        self.name = name
        self.sitz_verwaltung = sitz_verwaltung
        self.typ = typ

    def __repr__(self):
        return "<Kreis: %r %r %r %r>" % (self.ars, self.name, self.sitz_verwaltung, kreistyp_string(self.typ))

class Gemeindeverband(ARSObject):
    def __init__(self, ars=None, gebietsstand=None, 
                 name=None, sitz_verwaltung=None, typ=None):
        ARSObject.__init__(self, None, ars, gebietsstand)
        self.name = name
        self.sitz_verwaltung = sitz_verwaltung
        self.typ = typ

    def __repr__(self):
        return "<Gemeindeverband: %r %r %r %r>" % (self.ars, self.name, self.sitz_verwaltung, verbandstyp_string(self.typ))
    
class Gemeinde(ARSObject):
    def __init__(self, ags=None, ars=None, gebietsstand=None, 
                 name=None, typ=None):
        ARSObject.__init__(self, ags, ars, gebietsstand)
        self.name = name
        self.typ = typ
        self.bevoelkerung = 0
        self.maennlich = 0
        self.flaeche = 0

    def _get_weiblich(self):
        return self.bevoelkerung - self.maennlich
    weiblich = property(_get_weiblich)
    def __repr__(self):
        return "<Gemeinde: %r %r %r %r>" % (self.ars, self.ags, self.name, gemeindetyp_string(self.typ))


class Reader(object):
    def __init__(self, filename):
        self.list = None
        self.filename = filename
        self.handlers = {
            '10': self.handle_land,
            '20': self.handle_regierungsbezirk,
            '30': self.handle_region,
            '40': self.handle_landkreis,
            '50': self.handle_gemeindeverband,
            '60': self.handle_gemeinde,
            }

    def parse_gebietsstand(self, line):
        return date(int(line[2:6]), int(line[6:8]), int(line[8:10]))

    def read(self):
        self.list = []
        f = open(self.filename, 'r', 'cp850')
        for line in f:
            t = line[0:2]
            self.handlers[t](line)
        l = self.list
        self.list = None
        return l

    def handle_land(self, line):
        stand = self.parse_gebietsstand(line)
        ars = ags = line[10:12]
        name = line[22:72].strip()
        sl = line[72:122].strip()
        self.list.append(Land(ars=ars, name=name, gebietsstand=stand, sitz_landesregierung=sl))
        pass

    def handle_regierungsbezirk(self, line):
        stand = self.parse_gebietsstand(line)
        ars = ags = line[10:13]
        name = line[22:72].strip()
        sl = line[72:122].strip()
        self.list.append(Regierungsbezirk(ars=ars, name=name, gebietsstand=stand, sitz_verwaltung=sl))
        pass

    def handle_region(self, line):
        stand = self.parse_gebietsstand(line)
        ars = ags = line[10:14]
        name = line[22:72].strip()
        sl = line[72:122].strip()
        self.list.append(Region(ars=ars, name=name, gebietsstand=stand, sitz_verwaltung=sl))

    def handle_landkreis(self, line):
        stand = self.parse_gebietsstand(line)
        ars = ags = line[10:15]
        name = line[22:72].strip()
        sl = line[72:122].strip()
        typ = int(line[122:124])
        self.list.append(Kreis(ars=ars, name=name, gebietsstand=stand, sitz_verwaltung=sl, typ=typ))

    def handle_gemeindeverband(self, line):
        stand = self.parse_gebietsstand(line)
        ars = line[10:15]+line[18:22]
        name = line[22:72].strip()
        sl = line[72:122].strip()
        typ = int(line[122:124])
        self.list.append(Gemeindeverband(ars=ars, name=name, gebietsstand=stand, sitz_verwaltung=sl, typ=typ))

    def handle_gemeinde(self, line):
        stand = self.parse_gebietsstand(line)
        ars = line[10:15]+line[18:22]+line[15:18]
        ags = line[10:15]+line[15:18]
        name = line[22:72].strip()
        sl = line[72:122].strip()
        typ = int(line[122:124])
        self.list.append(Gemeinde(ars=ars, ags=ags, name=name, gebietsstand=stand, typ=typ))

def main(argv):
    result = Reader(argv[0]).read()
    print len(result)

if __name__ == '__main__':
    import sys
    main(sys.argv[1:])
