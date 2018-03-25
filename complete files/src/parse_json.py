#!/usr/bin/env python3

import sys
import json
import re

from difflib import SequenceMatcher
from geotext import GeoText
from astropy.io import ascii

'''
USAGE:
    python3 parse_json.py "input String"

    Ex: python3 parse_json.py "IIT Delhi" or "IIT Bombay" or "Materials Science Center, IIT, Kharagpur, 721 302 West Bengal India., Kharagpur"

'''

data    = json.load(open('data.json', 'r'))
cities  = json.load(open('cities.json', 'r'))

# guess city name from given string using geo.text
# city Information can be use to search for institutes
def guess_city(affiliation, cities=cities):
    out = []
    places = GeoText(affiliation)
    city = places.cities

    if city:
        return city
    elif not city:
        words = affiliation.split(',')
        for (n, city) in enumerate(cities):
            for word in words:
                word = word.strip()
                if word in cities[city]:
                    out.append(city)
        if out:
            return out
        else:
            words = affiliation.split()
            for (n, city) in enumerate(cities):
                for word in words:
                    word = word.strip()
                    word = word.strip(',')
                    word = word.strip(';')
                    word = word.strip(':')
                    if word in cities[city]:
                        out.append(city)
            return out



# guess federation name from given string using regular expression
class Federation:
    def __init__(self, affiliation):
        self.affiliation = affiliation

    def aicte(self):
        match = re.search(r"AICTE", self)
        if match: return True

    def aiims(self):
        match = re.search(r"AIIMS|AIIMS New Delhi|AIIMS Bhopal|AIIMS Bhubaneswar|AIIMS Jodhpur|AIIMS Patna|AIIMS Raipur|AIIMS Rishikesh", self)
        if match: return True

    def csir(self):
        match = re.search(r"CSIR|C.S.I.R|(CSIR)", self)
        if match: return True

    def dae(self):
        match = re.search(r"DAE", self)
        if match: return True

    def dbt(self):
        match = re.search(r"DBT", self)
        if match: return True

    def deemed(self):
        match = re.search(r"DEEMED", self)
        if match: return True

    def drdo(self):
        match = re.search(r"DRDO", self)
        if match: return True

    def dst(self):
        match = re.search(r"DST", self)
        if match: return True

    def icar(self):
        match = re.search(r"ICAR|I.C.A.R|(ICAR)", self)
        if match: return True

    def icmr(self):
        match = re.search(r"ICMR|I.C.M.R|(ICMR)", self)
        if match: return True

    def issr(self):
        match = re.search(r"ISSR|I.S.S.R|(ISSR)", self)
        if match: return True

    def iit(self):
        match = re.search(r"IIT|IITB|IITD|IITG|IITM|IITK|Indian Institute of Technology", self)
        if match: return True

    def meity(self):
        match = re.search(r"MEITY", self)
        if match: return True

    def nit(self):
        match = re.search(r"NIT|National Institute of Technology", self)
        if match: return True

    def niper(self):
        match = re.search(r"NIPER", self)
        if match: return True

    def tifr(self):
        match = re.search(r"TIFR", self)
        if match: return True

    def ugc(self):
        match = re.search(r"University", self)
        if match: return True

    def ltd(self):
        match =  re.search(r"Ltd|LTD|Limited", self)
        if match: return True

    def ngo(self):
        match = re.search(r"Foundation|foundation", self)
        if match: return True

    def hospital(self):
        match = re.search(r"Hospital", self)
        if match: return True


    federation = "OTHER"

    def Main(self):

        if Federation.aicte(self):
            federation = "AICTE"
        elif Federation.aiims(self):
            federation = "AIIMS"
        elif Federation.csir(self):
            federation = "CSIR"
        elif Federation.dae(self):
            federation = "DAE"
        elif Federation.dbt(self):
            federation = "DBT"
        elif Federation.drdo(self):
            federation = "DRDO"
        elif Federation.dst(self):
            federation = "DST"
        elif Federation.icar(self):
            federation = "ICAR"
        elif Federation.icmr(self):
            federation = "ICMR"
        elif Federation.issr(self):
            federation = "ISSR"
        elif Federation.iit(self):
            federation = "IIT"
        elif Federation.nit(self):
            federation = "NIT"
        elif Federation.niper(self):
            federation = "NIPER"
        elif Federation.tifr(self):
            federation = "TIFR"
        elif Federation.ugc(self):
            federation = "UGC"
        elif Federation.ltd(self):
            federation = "COMPANY"
        elif Federation.hospital(self):
            federation = "HOSPITAL"
        elif Federation.ngo(self):
            federation = "NGO"
        else:
            federation = "OTHER"

        return federation

# if we have city name and federation gussed
# we can also guess institute mapping those information together
def map_city_with_federation():
    pass

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


class Institute:
    def direct(aff):
        parts = aff.split(",")
        inst = {}
        for line in data:
            for part in parts:
                part = part.strip()
                if part in line['alt-name']:
                    inst['apid']        = line['apID']
                    inst['name']        = line['name']
                    inst['acronym']     = line['acronym']
                    inst['federation']  = line['federation']
                    inst['city']        = line['city']
                    #inst['district']    = line['district']
                    inst['state']       = line['state']
                    inst['country']     = "India."
        return inst

    def name_part(aff):
        con   = re.compile(r", India\.")
        insp  = re.compile(r"Educational|institute|Laboratory|centre|college|Research|Foundation|university|vidya|Kalamandalam|Facility|academy|Ltd|hospital|Medical School|Istituto|Scientifico|Technology|Research|Technical", re.IGNORECASE)
        num = re.compile(r"[0-9]+\.")
        mail = re.compile(r"Electronic Address: [a-z][\w][@][a-z][\w]+\.")
        name = re.sub(con, "", aff.strip())
        name = re.sub(mail, "", aff.strip())
        name = re.sub(num, "", aff.strip())
        parts = aff.split(',')

        for part in parts:
            m = re.search(insp, part)
            if m:
                name = part.strip()

        return name

def build_inst(federation, city, name):
    inst = {}
    inst['apid']        = ""
    inst['name']        = name
    inst['acronym']     = ""
    inst['federation']  = federation
    inst['city']        = city
    inst['district']    = ""
    inst['state']       = ""
    inst['country']     = "India."
    return inst



def Main(aff):
    inst = Institute.direct(aff)
    cities = guess_city(aff)
    fed = Federation.Main(aff)

    if inst:
        return inst
    elif fed == 'IIT':
        try:
            name = "Indian Institute of Technology," + cities[0]
        except:
            name = "Indian Institute of Technology," + " "
        return build_inst(fed, cities[0], name)

    elif "India" in aff:
        name = Institute.name_part(aff)
        try:
            inst = build_inst(fed, cities[0], name)
        except:
            inst = build_inst(fed, "", name)
        return inst

    else:
        name = Institute.name_part(aff)
        try:
            inst = build_inst(fed, cities[0], name)
        except:
            inst = build_inst(fed, "", name)
        return inst

if __name__ == '__main__':
    test = sys.argv[1]
    tmp = Main(test)
    print(tmp)
