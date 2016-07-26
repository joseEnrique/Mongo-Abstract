
import pymongo

from settings import MongoConfig
from singleton import singleton
import pdb



@singleton
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
        pdb.set_trace()

    def getConn(self):
        return self._instance

    def getDB(self):
        return self._currentDB

    def searchAll(self,collection=None):
        return self._currentDB[collection].find()


    def closeDB(self):
        self.instance.close()




prueba = MongoDB()
prueba.connDB()

