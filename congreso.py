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
        return [ element for element in self._getCollection(collection).find()]

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


    def getInitiative(self, collection="iniciativas", ref = None, tipotexto= None, titulo = None):
        search = self._getCollection(collection).find_one(
            {
                'ref': ref,
                'tipotexto': tipotexto,
                'titulo': titulo
            }
        )

        return search


    def updateorinsertInitiative(self, collection="iniciativas", type = "insert", item = None):
        #metodo para el pipeline
        if type is 'insert':
            self._insertInitiative(collection,item)
            #update
        elif type is 'update':
            self._updateInitiative(collection,item)
            #inserta
        else:
            print "Not type accepted"
            raise

    def _insertInitiative(self,collection,item):
        self._getCollection(collection=collection).insert(dict(item))

    def _updateInitiative(self,collection,item):
        coll = self._getCollection(collection=collection)
        coll.update_one({
                 'ref': item['ref'],
                'tipotexto': item['tipotexto'],


        },{
            '$set': {
            'titulo': item['titulo'],
            'autor_diputado': item['autor_diputado'],
            'autor_grupo': item['autor_grupo'],
            'autor_otro': item['autor_otro'],
            'url': item['url'],
            'content': item['content'],
            'tipo': item['tipo'],
            'tramitacion': item['tramitacion'],
            'restramitacion': item['restramitacion'],
            'fecha': item['fecha'],
            'lugar': item['lugar'],
            'countcontent': item['countcontent'],
            'fechafin': item['fechafin'],

                    }
            ,}
        )


    def isDiffinitiative(self, collection="iniciativas", item = None, search = None):


        if search:#existe
            return not self.sameInitiative(item,search)
        else:
            return False

    def sameInitiative(self,item,search):
        if len(item.keys()) != len(search.keys())-1: # se descarta el content
            return False
        else:
            for key, value in search.iteritems():
                for ikey,ivalue in item.iteritems():
                    if key == ikey:
                        if value !=  ivalue and  key is not 'content':

                            return False
            return True









