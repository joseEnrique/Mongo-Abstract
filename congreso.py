# -*- coding: utf-8 -*-
import re

from conn import MongoDBconn
import pdb

class Congress(object):
    _conn = None
    def __init__(self):
        self._conn= MongoDBconn()

    def _getCollection(self,collection):
        return self._conn.getDB()[collection]

    def searchAll(self,collection=None):
        return self._getCollection(collection).find()

    def getMember(self,collection= "miembros", name = None):
        search = self._getCollection(collection).find_one({
            'nombre': name
        })
        try:
            return search
        except:
            return None

    def getGroupfrommember(self, collection= "miembros", name = None):
        search = self.getMember(collection,name)

        return search['grupo']


    def getGroup(self, collection = "grupos", name = None):
        acronimo = None
        if re.search("la izquierda plural",name,re.IGNORECASE):
            acronimo = u'GIP'
        elif re.search("popular",name,re.IGNORECASE):
            acronimo = u'GP'
        elif re.search("vasco", name, re.IGNORECASE):
            acronimo = u'GV (EAJ-PNV)'
        elif re.search("socialista", name, re.IGNORECASE):
            acronimo = u'GS'
        elif re.search("mixto", name, re.IGNORECASE):
            acronimo = u'GMx'
        elif re.search("converg(e|è)ncia", name, re.IGNORECASE):
            acronimo = u'GC-CiU'
        elif re.search("progreso", name, re.IGNORECASE):
            acronimo = u'GUPyD'
        search = self._getCollection(collection).find_one({
            'acronimo': acronimo
        })
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


item = {'ref': '110/000141',
        'type': u'Autorización de Convenios Internacionales'
        }

a = Congress()
b =a.typeAutor(name="Macias i Arau, Pere")
pdb.set_trace()

