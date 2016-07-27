# -*- coding: utf-8 -*-
import pymongo

from settings import MongoConfig
from singleton import singleton
import pdb



class MongoDB(object):

    _instance = None
    _currentDB =  None

    def connDB(self):
        configuration = MongoConfig()
        mongo_client = pymongo.MongoClient(host=configuration.host, port=configuration.port)
        self._instance = mongo_client
        try:
            db = mongo_client[configuration.db_name]
            if configuration.username is not None:
                db.authenticate(configuration.username, password=configuration.password)
            self._currentDB = db
        except:
            pass

    def getConn(self):
        return self._instance

    def getDB(self):
        return self._currentDB

    def searchAll(self,collection=None):
        return self.getDB()[collection].find()

    def insertorupdateItem(self,collection,item):
        search =  self.getDB()[collection].find(
            {
                'ref': item['ref'],
                'type': item['type']

            }
        )
        if search:
            pass

        else:
            pass

        for i in search:

            print i



    def closeDB(self):
        self._instance.close()


item = {'ref':'110/000141',
        'type': u'Autorización de Convenios Internacionales'
        }

prueba = MongoDB()
prueba.connDB()
prueba.insertorupdateItem('test',item)

