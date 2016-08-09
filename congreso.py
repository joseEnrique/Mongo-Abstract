# -*- coding: utf-8 -*-
import re

from conn import MongoDBconn
import pdb

class Congress(object):
    _conn = None
    def __init__(self):
        self._conn = MongoDBconn()

    def _getCollection(self,collection):
        return self._conn.getDB()[collection]

    def searchAll(self,collection=None):
        return self._getCollection(collection).find()

    def getMember(self,collection= "diputados", name = None):
        search = self._getCollection(collection).find_one({
            'nombre': name
        })
        try:
            return search
        except:
            return None

    def getGroupfrommember(self, collection= "diputados", name = None):
        search = self.getMember(collection,name)

        return self.getGroup(name=search['grupo'])


    def getGroup(self, collection = "grupos", name = None):
        #sebusca por acronimo
        acronimo = None
        if re.search("la izquierda plural",name,re.IGNORECASE)  \
                or re.search("GIP",name,re.IGNORECASE) :
            acronimo = u'GIP'
        elif re.search("popular",name,re.IGNORECASE) \
                or re.search("GP",name,re.IGNORECASE):
            acronimo = u'GP'
        elif re.search("vasco", name, re.IGNORECASE) \
                or re.search("EAJ-PNV",name,re.IGNORECASE):
            acronimo = u'GV (EAJ-PNV)'
        elif re.search("socialista", name, re.IGNORECASE) \
                or re.search("GS",name,re.IGNORECASE):
            acronimo = u'GS'
        elif re.search("mixto", name, re.IGNORECASE) \
            or re.search("GMx",name,re.IGNORECASE):
            acronimo = u'GMx'
        elif re.search("converg", name, re.IGNORECASE) \
            or re.search("GC-CiU",name,re.IGNORECASE):
            acronimo = u'GC-CiU'
        elif re.search("progreso", name, re.IGNORECASE) \
                or re.search("GUPyD",name,re.IGNORECASE):
            acronimo = u'GUPyD'
        try:
            search = self._getCollection(collection).find_one({
            'acronimo': acronimo
            })
        except:
            return None

        return search

    def typeAutor(self, name):
        if self.getMember(name=name):
            return "diputado"
        elif self.getGroup(name=name):
            return "grupo"
        else:
            return "otro"


    def insertorupdateItem(self, collection, item):
        search = self._getCollection(collection).find(
            {
                'ref': item['ref'],
                'tipotexto': item['tipotexto'],
                'titulo': item['titulo']

            }
        )
        if search:
            pass

        else:
            pass

        for i in search:

            print i


def concatlist(list):
    if list:
        return ' '.join(elem for elem in list)
    else:
        return ' '




