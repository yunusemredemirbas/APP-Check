import os
from pymongo import MongoClient
from getpass import getpass
from json import loads,dumps


class DBOperations:
    db_username = os.environ.get("MONGODBUSERNAME")  # input("DB Username: ")
    db_password = os.environ.get("MONGODBPASS")  # getpass("DB Password: ")
    URL = f"mongodb+srv://{db_username}:{db_password}@cluster0.mfdun.mongodb.net/APP_INFOS?retryWrites=true&w=majority"


    try:
        db_connection = MongoClient(URL)
        dbAppInfos = db_connection["APP_INFOS"]
        col_enrollment = dbAppInfos["col_enrollment"]
        col_live_app_data = dbAppInfos["col_live_app_data"]

    except BaseException as err:
        print("connection error", err)
        print("exiting program")
        exit()

    def host_software_check_and_change(self):

        """
        burada cihazlarda olan uygulama kontrol edilmekte ve değişikliği yapılmaktadır,

        Keyler: _id(serial_number), hostname, pid, app_hash, apps{alınan bilgiler}

        """

        pass

    def update_one_query(self, collection, query, second_query=None):

        tempCollection = self.dbAppInfos[collection]
        if second_query == None:
            resp = tempCollection.update_one(query)
        else:
            resp = tempCollection.update_one(query, second_query)
        return resp

    def find_one_query(self, collection, query, second_query=None):

        #bir collection içerisinde istenen data var mı yok mu kontrol ediyor

        tempCollection = self.dbAppInfos[collection]
        if second_query == None:
            resp = tempCollection.find_one(query)
        else:
            resp = tempCollection.find_one(query,second_query)
        return resp

    def check_process_id(self, hostname, serial_number, pid):

        result = self.col_live_app_data.find_one("col_live_app_data", {"_id": serial_number, "hostname": hostname},
                                                 {"request_id": 1, "_id": 0})  #
        print(result)

        try:
            if pid == result["request_id"]:
                return True
            else:
                return False
        except:

            return False


    def check_enroll_id_and_pass(self, enrollment_id, enrollment_pass):

        resp = self.find_one_query("col_enrollment",{"enrollment_id": enrollment_id, "enrollment_pass": enrollment_pass})
        print("***", resp)
        if resp:
            print("Kayıt bilgileri doğru")
            return True
        else:
            print("Kayit bilgileri yanlis")
            return False

    def insert_new_client(self, serial_number, hostname):

        error = False

        req = {"_id": f"{serial_number}", "app_hash": "", "apps": {"7zip": {"date": {"$timestamp": {"t": 0, "i": 0}}}},
               "hostname": f"{hostname}", "request_id": {"$numberLong": "0"}}
        try:
            resp = self.col_live_app_data.insert_one(req)
            return resp.acknowledged

        except BaseException as err:

            return err

    def connection_close(self):
        self.db_connection.close()



resp = DBOperations().update_one_query("col_live_app_data",{"_id":"test","apps.hash" : "aa"},{"$set" : {"apps.$.names" : "abababaa"}})
resp = DBOperations().find_one_query("col_live_app_data", {"_id":"test", "apps.name": "aaa"},{"apps.$":1, "_id":0})
tut = {}
print(resp)
print(type(resp))

for key in resp["apps"][0].keys():
    tut[f"apps.$.{key}"] = key
if resp:
    print(resp["apps"][0].keys())
else:
    print("bos")

print(tut)

DBOperations().update_one_query("col_live_app_data", {"_id":"test"},{"$push": {"apps": {'apps.$.name': 'bba', 'apps.$.hash': 'bba', 'apps.$._id': 'bba', 'apps.$.names': 'abba'} }})
