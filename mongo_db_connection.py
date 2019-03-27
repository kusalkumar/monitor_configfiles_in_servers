#mongo_db_connection.py
from pymongo import MongoClient

#project specific imports
import paramiko_params as pp

class MongoDbConnection():

    def connect_to_db(self):
        try:
            self.myclient = MongoClient("mongodb://" + pp.mongo_db_host + ":{}".format(pp.mongo_db_port))
            self.mycollection = self.myclient[pp.mongo_db_database][pp.mongo_db_table]
        except:
            print("Error occured in DB Connection")


    def check_and_update(self, conn_dict):
        if self.mycollection.find({'server_name':conn_dict['server_name']}).count() > 0:
            print("updating")
            self.mycollection.update_one(
                {"server_name":conn_dict["server_name"]},
                {'$set':{"values": conn_dict["values"]}}
            )
        else:
            self.mycollection.insert_one(conn_dict)

    def closedb(self):
        self.myclient.close()

    def print_content_collection(self):
        cursor = self.mycollection.find()
        for record in cursor:
            print(record)
