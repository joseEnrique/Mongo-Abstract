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


    def getGroupfrommember(self, collection= "miembros", name = None):
        search = self._getCollection(collection).find_one({
            'nombre': name
        })
        return search['grupo']

    def getGroup(self, collection = "grupos", name = None):
        regx = re.compile(name, re.IGNORECASE)
        search = self.searchAll(collection)
        for field in search:
            pdb.set_trace()

            camposnombre = field['nombre'].split(' ')
            regexstring = camposnombre[0]+" .*? "+concatlist(camposnombre[1:])
            if re.search(regexstring, name,re.IGNORECASE ):

                pdb.set_trace()



    def typeAutor(self, name):
        if self.getGroupfrommember(name):
            return "diputado"
        elif self.getGroup(name):
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
        return ''.join(elem for elem in list)
    else:
        return ''







a = Congress()
a.getGroup(name="Grupo Parlamentario de IU, ICV-EUiA, CHA: La Izquierda Plural")


