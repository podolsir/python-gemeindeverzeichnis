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

LAND_LEVEL = 10
REGIERUNGSBEZIRK_LEVEL = 20
REGION_LEVEL = 30
KREIS_LEVEL = 40
GEMEINDEVERBAND_LEVEL = 50
GEMEINDE_LEVEL = 60

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


def _int_or_none(s):
    if s.strip() == '':
        return None
    return int(s)

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

class DerivedBevoelkerungMixin(object):
    def _get_bevoelkerung(self):
        return reduce(lambda i, x: i + x, [a.bevoelkerung for a in self.children])

    bevoelkerung = property(_get_bevoelkerung)

    def _get_maennlich(self):
        return reduce(lambda i, x: i + x, [a.maennlich for a in self.children])

    maennlich = property(_get_maennlich)

    def _get_weiblich(self):
        return reduce(lambda i, x: i + x, [a.weiblich for a in self.children])

    weiblich = property(_get_weiblich)

class RSObject(object):
    def __init__(self, ags=None, rs=None, gebietsstand=None):
        self.ags = ags
        self.rs = rs
        self.gebietsstand = gebietsstand
        self.parent = None
        self.children = []
    
    def add_child(self, obj):
        self.children.append(obj)
        obj.parent = self

    def remove_child(self, obj):
        self.children.remove(obj)
        obj.parent = None

class Land(RSObject, DerivedBevoelkerungMixin):
    def __init__(self, rs=None, gebietsstand=None, 
                 name=None, sitz_landesregierung=None):
        RSObject.__init__(self, rs, rs, gebietsstand)
        self.name = name
        self.sitz_landesregierung = sitz_landesregierung
        self.level = LAND_LEVEL

    def __repr__(self):
        return "<Land: %r %r %r>" % (self.rs, self.name, self.sitz_landesregierung)

class Regierungsbezirk(RSObject, DerivedBevoelkerungMixin):
    def __init__(self, rs=None, gebietsstand=None, 
                 name=None, sitz_verwaltung=None):
        RSObject.__init__(self, rs, rs, gebietsstand)
        self.name = name
        self.sitz_verwaltung = sitz_verwaltung
        self.level = REGIERUNGSBEZIRK_LEVEL

    def __repr__(self):
        return "<Regierungsbezirk: %r %r %r>" % (self.rs, self.name, self.sitz_verwaltung)

class Region(RSObject, DerivedBevoelkerungMixin):
    def __init__(self, rs=None, gebietsstand=None, 
                 name=None, sitz_verwaltung=None):
        RSObject.__init__(self, rs, rs, gebietsstand)
        self.name = name
        self.sitz_verwaltung = sitz_verwaltung
        self.level = REGION_LEVEL

    def __repr__(self):
        return "<Region: %r %r %r>" % (self.rs, self.name, self.sitz_verwaltung)

class Kreis(RSObject, DerivedBevoelkerungMixin):
    def __init__(self, rs=None, gebietsstand=None, 
                 name=None, sitz_verwaltung=None, typ=None):
        RSObject.__init__(self, rs, rs, gebietsstand)
        self.name = name
        self.sitz_verwaltung = sitz_verwaltung
        self.typ = typ
        self.level = KREIS_LEVEL

    def _get_typ_string(self):
        return kreistyp_string(self.typ)
    typ_string = property(_get_typ_string)

    def __repr__(self):
        return "<Kreis: %r %r %r %r>" % (self.rs, self.name, self.sitz_verwaltung, kreistyp_string(self.typ))

class Gemeindeverband(RSObject, DerivedBevoelkerungMixin):
    def __init__(self, rs=None, gebietsstand=None, 
                 name=None, sitz_verwaltung=None, typ=None):
        RSObject.__init__(self, None, rs, gebietsstand)
        self.name = name
        self.sitz_verwaltung = sitz_verwaltung
        self.typ = typ
        self.level = GEMEINDEVERBAND_LEVEL
    
    def _get_typ_string(self):
        return verbandstyp_string(self.typ)
    typ_string = property(_get_typ_string)

    def __repr__(self):
        return "<Gemeindeverband: %r %r %r %r>" % (self.rs, self.name, self.sitz_verwaltung, verbandstyp_string(self.typ))
    
class Gemeinde(RSObject):
    def __init__(self, ags=None, rs=None, gebietsstand=None, 
                 name=None, typ=None):
        RSObject.__init__(self, ags, rs, gebietsstand)
        self.name = name
        self.typ = typ
        self.bevoelkerung = 0
        self.maennlich = 0
        self.flaeche = 0
        self.level = GEMEINDE_LEVEL

    def _get_typ_string(self):
        return gemeindetyp_string(self.typ)
    typ_string = property(_get_typ_string)

    def _get_weiblich(self):
        return self.bevoelkerung - self.maennlich
    weiblich = property(_get_weiblich)

    def __repr__(self):
        return "<Gemeinde: %r %r %r %r>" % (self.rs, self.ags, self.name, gemeindetyp_string(self.typ))

NONEXISTENT_REGIERUNGSBEZIRK_LIST = [u'031',u'032',u'033',u'034',u'071', u'072', u'073']

class ADReader(object):
    """
    Initializes a new reader for the GV100AD.ASC (administrative division) data set.

    Arguments:
    filename: the path to the ASC file containing GV100AD data.
    ignore_list: an iterable of unicode objects representing Regionalschluessel keys 
                 of entities to ignore. Try with NONEXISTENT_REGIERUNGSBEZIRK_LIST.
    remove_dummy_gemeindeverband: whether to remove the dummy Gemeindeverband-level
                 objects containing only a single Gemeinde
    """
    def __init__(self, filename, ignore_list=(), remove_dummy_gemeindeverband=True):
        self.filename = filename
        self._ignore_list = set(ignore_list)
        self._do_remove_bogus_gv = remove_dummy_gemeindeverband
        self.handlers = {
            '10': self._handle_land,
            '20': self._handle_regierungsbezirk,
            '30': self._handle_region,
            '40': self._handle_landkreis,
            '50': self._handle_gemeindeverband,
            '60': self._handle_gemeinde,
            }
        self.index = {}

    def read(self):
        """
        Reads in the data from the file.
        
        Returns all entries in a dictionary indexed by the Regionalschlüssel.
        """
        self.list = []
        f = open(self.filename, 'r', 'cp850')
        for line in f:
            t = line[0:2]
            self.handlers[t](line)
        if self._do_remove_bogus_gv:
            self._remove_bogus_gv(self.index)
        l = self.index
        self.index = None
        return l

    def _remove_bogus_gv(self, index):
        toremove = []
        for i in index:
            if not isinstance(index[i], Gemeindeverband):
                continue
            gv = index[i]
            if len(gv.children) == 1:
                p = gv.parent;
                p.remove_child(gv)
                p.add_child(gv.children[0])
                toremove.append(i)

        for i in toremove:
            del index[i]

    def _parse_gebietsstand(self, line):
        return date(int(line[2:6]), int(line[6:8]), int(line[8:10]))

    def _handle_land(self, line):
        rs = ags = line[10:12]
        if rs in self._ignore_list:
            return
        stand = self._parse_gebietsstand(line)
        name = line[22:72].strip()
        sl = line[72:122].strip()
        l = Land(rs=rs, name=name, gebietsstand=stand, sitz_landesregierung=sl)
        self.list.append(l)
        self.index[l.rs] = l
        pass

    def _handle_regierungsbezirk(self, line):
        stand = self._parse_gebietsstand(line)
        rs = ags = line[10:13]
        if rs in self._ignore_list:
            return
        name = line[22:72].strip()
        sl = line[72:122].strip()
        rb = Regierungsbezirk(rs=rs, name=name, gebietsstand=stand, sitz_verwaltung=sl)

        parent = self.index[rb.rs[0:2]]
        parent.add_child(rb)

        self.list.append(rb)
        self.index[rb.rs] = rb
        pass

    def _handle_region(self, line):
        stand = self._parse_gebietsstand(line)
        rs = ags = line[10:14]
        if rs in self._ignore_list:
            return
        name = line[22:72].strip()
        sl = line[72:122].strip()
        reg = Region(rs=rs, name=name, gebietsstand=stand, sitz_verwaltung=sl)

        parent = self.index[reg.rs[0:3]]
        parent.add_child(reg)

        self.list.append(reg)
        self.index[reg.rs] = reg

    def _handle_landkreis(self, line):
        stand = self._parse_gebietsstand(line)
        rs = ags = line[10:15]
        if rs in self._ignore_list:
            return
        name = line[22:72].strip()
        sl = line[72:122].strip()
        typ = int(line[122:124])
        k = Kreis(rs=rs, name=name, gebietsstand=stand, sitz_verwaltung=sl, typ=typ)

        # Region?
        if k.rs[0:4] in self.index:
            self.index[k.rs[0:4]].add_child(k)
        # Regierunsbezirk?
        elif k.rs[0:3] in self.index:
            self.index[k.rs[0:3]].add_child(k)
        else:
            # otherwise, Land
            self.index[k.rs[0:2]].add_child(k)

        self.list.append(k)
        self.index[k.rs] = k

    def _handle_gemeindeverband(self, line):
        stand = self._parse_gebietsstand(line)
        rs = line[10:15]+line[18:22]
        if rs in self._ignore_list:
            return
        name = line[22:72].strip()
        sl = line[72:122].strip()
        typ = int(line[122:124])
        gv = Gemeindeverband(rs=rs, name=name, gebietsstand=stand, sitz_verwaltung=sl, typ=typ)
        
        if gv.rs[0:5] in self.index:
            self.index[gv.rs[0:5]].add_child(gv)
        elif gv.rs[0:5].endswith('000'):
            self.index[gv.rs[0:2]].add_child(gv)

        self.list.append(gv)
        self.index[gv.rs] = gv

    def _handle_gemeinde(self, line):
        stand = self._parse_gebietsstand(line)
        rs = line[10:15]+line[18:22]+line[15:18]
        if rs in self._ignore_list:
            return
        ags = line[10:15]+line[15:18]
        name = line[22:72].strip()
        sl = line[72:122].strip()
        typ = int(line[122:124])
        gem = Gemeinde(rs=rs, ags=ags, name=name, gebietsstand=stand, typ=typ)
        gem.bevoelkerung = int(line[139:150].strip())
        gem.maennlich = int(line[150:161].strip())
        gem.flaeche = int(line[128:139].strip())
        gem.finanzamtsbezirk = _int_or_none(line[177:181])
        gem.oberlandesgerichtsbezirk = line[181:183].strip()
        gem.landgerichtsbezirk = _int_or_none(line[183])
        gem.amtsgerichtsbezirk = _int_or_none(line[184])
        gem.arbeitsamtsbezirk = _int_or_none(line[185:190])

        gem.plz = line[165:170]
        gem.plzeindeutig = line[170:175].strip() == ''

        bwvon = _int_or_none(line[190:193])
        bwbis = _int_or_none(line[193:196])
        gem.bundestagswahlkreis = (bwvon, bwbis)
        self.index[gem.rs[0:9]].add_child(gem)
        self.list.append(gem)
        self.index[gem.rs] = gem

def main(argv):
    result = ADReader(argv[0]).read()
    from pprint import pprint
    pprint(result['081155002013'])

if __name__ == '__main__':
    import sys
    main(sys.argv[1:])
