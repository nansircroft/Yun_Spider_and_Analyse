#!/usr/bin env python
# coding = utf-8

from pymongo import MongoClient
import config 


class CommentsDb():
    def __init__(self):
        super().__init__()
        self.__host = config.db_host
        self.__port = config.db_port
    
    def __get_connection(self):
        try:
            connection = MongoClient(self.__host, self.__port)
            return connection
        except Exception:
            print("exception when getting a connection")
            return False

    def get_a_database(self,db_name):
        con = self.__get_connection()
        try:
            db = con[db_name]
            return db
        except Exception:
            print("exception when getting a db")
            return False
    
    def get_a_collection(self,db,collection):
        col = db[collection]
        return col

    def insert_one(self,collection,doc):
        try:
            collection.insert_one(doc)
            return True
        except Exception:
            print("exception when inserting one doc")
            return False
    
    def find_one(self,collection,doc):
        try:
            result = collection.find_one(doc)
            return result
        except Exception:
            print("error when finding one doc")
            return False

    def find_many(self,collection):
        try:
            for re in collection.find():
                yield re
        except Exception:
            print("exception find one when finding many doc")
            yield False
    
    def del_many(self,collention,doc):
        try:
            res = collention.delete_many(doc)
            print("successfully delete %s docs in %s"%(res.deleted_count,collention))
            return res
        except Exception as e:
            print("exception delete one when deleting many doc in %s"%collention)
            print(e)
            return False