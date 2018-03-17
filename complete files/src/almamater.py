#!/usr/bin/env python3

import re
import sys
from astropy.io import ascii
from geotext import GeoText


states = [
    "Andra Pradesh",
    "Hyderabad",
    "Arunachal Pradesh",
    "Assam",
    "Bihar",
    "Chhattisgarh",
    "Goa",
    "Gujarat",
    "Haryana",
    "Chandigarh",
    "Himachal Pradesh",
    "Jammu and Kashmir",
    "Jharkhand",
    "Karnataka",
    "Kerala",
    "Madya Pradesh",
    "Maharashtra",
    "Meghalaya",
    "Mizoram",
    "Nagaland",
    "Odissa",
    "Punjab",
    "Chandigarh",
    "Rajasthan",
    "Sikkim",
    "Tamil Nadu",
    "Tripura",
    "Uttaranchal",
    "Uttar Pradesh",
    "West Bengal"
]


class Almamater():
    def __init__(self):
        pass

    def department(aff):
        dep = re.compile(r'department|lab|unit|school|division', re.IGNORECASE)
        cols = aff.split(',')
        cols = [col.strip() for col in cols]
        out = ""
        for col in cols:
            match = re.search(dep, col)
            if match:
                out = col
        return out


    def institute(aff, names, index):
        nes = []; out = []

        if index is not None:
            return names[index]

        else:
            cols = aff.split(',')
            cols = [col.strip() for col in cols]
            for (n, name) in enumerate(names):
                name = name.replace('(', '\\(')
                name = name.replace(')', '\\)')
                namre = re.compile(name)

                try:
                    sn = name.split('-')
                    snre  = re.compile(sn)
                except:
                    sn = None

                if name in cols:
                    nes.append(n)
                    out.append(name)
                elif sn != None:
                    match = re.search(snre, aff)
                    if match:
                        nes.append(n)
                        out.append(match.group(0))
                else:
                    match = re.search(namre, aff)
                    if match:
                        nes.append(n)
                        out.append(match.group(0))
                    else:
                        pass
            return nes, out



    def split_name(aff):
        out = ""
        con   = re.compile(r", India\.")
        insp  = re.compile(r"institute|Laboratory|centre|college|Research|Foundation|university|vidya|Kalamandalam|Facility|academy|Ltd|hospital|Medical School|Istituto|Scientifico|Technology|Research|Technical", re.IGNORECASE)
        num = re.compile(r"[0-9]+\.")
        mail = re.compile(r"Electronic Address: [a-z][\w][@][a-z][\w]+\.")
        name = re.sub(con, "", aff.strip())
        name = re.sub(mail, "", aff.strip())
        name = re.sub(num, "", aff.strip())
        parts = aff.split(',')

        for part in parts:
            m = re.search(insp, part)
            if m:
                out = part.strip()
        return out



    def federation(feds, index):
        if index:
            return feds[index]
        else:
            return 'OTHER'



    def city(aff, cities, index):
        nes = [];  out = []

        if index is not None:
            return(cities[index])

        else:
            places = GeoText(aff)
            out = places.cities

            cols = aff.split(',')
            cols = [col.strip() for col in cols]

            if out:
                for (n, cit) in enumerate(cities):
                    if out[0] == cit:
                        nes.append(n)
                        out.append(cit)

            elif not out:
                for (n, cit) in enumerate(cities):
                    namre = re.compile(cit)
                    if cit in cols:
                        nes.append(n)
                        out.append(cit)
                    else:
                        match = namre.search(aff)
                        if match:
                            nes.append(n)
                            out.append(match.group(0))
                        else:
                            pass
            else:
                pass


        return nes, out



    def state(states, index, aff):
        state = ""
        if index:
            state =  states[index]
        else:
            for st in states:
                if st in aff:
                    state = st
                else:
                    continue
        #print(state)
        return state



    def acronym(shorts, index, aff):
        acr = ''
        if index:
            acr = shorts[index]
        else:

            parts = aff.split( )
            for part in parts:
                if part.startswith('('):# and part.endswith(')') and part.isupppercase():
                    part = part.replace('(', '')
                    part = part.replace(')', '')
                    part = part.replace(',', '')
                    #print(part)
                    acr = part
        return acr


    def country():
        return "India."


def out(test):

    alma  = ascii.read("data/alma.csv", guess=False, header_start=0,
            data_start=1, delimiter=',', quotechar='"')
    names  = alma['Name']
    cities = alma['City']
    altcity= alma['AlterCity']
    states = alma['State']
    feds   = alma['Federation']
    shorts = alma['Acronym']
    contry = alma['Country']

    (nl, city_names)     = Almamater.city(test, cities, None)
    (al, city_names)     = Almamater.city(test, altcity, None)
    (ml, ins_names)      = Almamater.institute(test, names, None)

    try:
        comm = set(ml).intersection(nl)

    except:
        comm = set(ml).intersection(al)


    institute = {}

    if bool(comm):
        index    =  comm.pop()
        institute['apid']         = ""
        institute['federation']   = Almamater.federation(feds, index)
        institute['acronym']      = Almamater.acronym(shorts, index, test)
        institute['address']      = test
        institute['city']         = Almamater.city(test, cities, index)
        institute['district']     = ""
        institute['state']        = Almamater.state(states, index, test)
        institute['country']      = Almamater.country()
        institute['name']         = Almamater.institute(test, names, index) + ", " + Almamater.city(test, cities, index)


    else :
        index = None
        institute['apid']         = ""
        institute['federation']   = Almamater.federation(feds, index)
        institute['acronym']      = Almamater.acronym(shorts, index, test)
        institute['address']      = test

        try:
            (ids, cities)              = Almamater.city(test, cities, index)
            institute['city']         = cities[0]
        except:
            (ids, cities)              = Almamater.city(test, altcity, index)
            if cities != []:
                institute['city']         = cities[0]
            else:
                institute['city']         = ""

        institute['district']     = ""
        institute['state']        = Almamater.state(states, index, test)
        institute['country']      = Almamater.country()

        institute['name']         = Almamater.split_name(test) + ", " + institute['city']


    return institute



if __name__ == '__main__':
# almamater map file exported from university_list file

    alma  = ascii.read("data/alma.csv", guess=False, header_start=0,
        data_start=1, delimiter=',', quotechar='"')
    #test = sys.argv[1]
    test = "Department of Pharmaceutical Sciences and Drug Research, Punjabi University, Patiala-147 002, India"
    tmp = out(test)
    print(tmp)
