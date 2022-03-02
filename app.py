import threading
import random
import time

import pymongo.errors
from flask import Flask, jsonify, request, send_file
from threading import Thread
from database_operations import DBOperations

app = Flask(__name__)


@app.route("/")
def index():
    print(threading.current_thread().name, "start")
    if random.choice([True, False]):
        time.sleep(3)
    print(threading.current_thread().name, "stop")
    return "Hello"


@app.route("/setup", methods=["GET"])
def setup_app():
    path = "D://a.txt"
    return send_file(path, as_attachment=True)




@app.route("/enroll", methods=["POST"])
def check():
    enrollment_id = request.json["enrollment_id"]
    enrollment_pass = request.json["enrollment_pass"]
    hostname = request.json["hostname"]
    serial_number = request.json["serial_number"]
    response = {}

    # Kayıt kimliği ve parolası sorgulanıyor
    resp = DBOperations().check_enroll_id_and_pass(enrollment_id=enrollment_id, enrollment_pass=enrollment_pass)


    response["id_and_pass"] = resp
    #kayıt kimliği ve parolası doğruysa client e exe dosyası iletilmelidir.

    print("burada")
    insert_status = DBOperations().find_one_query("col_live_app_data", {"_id": serial_number, "hostname": hostname})
    print(insert_status)
    if resp and not insert_status: #Canlı veritabanında istek gönderen cihaz yoksa ve kayıt kimlikleri doğruysa
        try:
            DBOperations().insert_new_client(serial_number=serial_number, hostname=hostname)
            resp = True

        except BaseException:
            resp = "Error"

    else:
        resp = False

    response["insert_status"] = resp
    return response


@app.route("check", methods=["POST"])
def hash_check():
    response = {}
    hostname = request.json["hostname"]
    serial_number = request.json["serial_number"]
    request_code = request.json["request_code"]
    apps_hash = request.json["apps_hash"]
    if request_code == 0:
        response["request_code"] = 0
        resp = DBOperations().find_one_query("col_live_app_data",{"_id":serial_number, "hostname":hostname},{"apps_hash":1})

        if resp["apps_hash"] == apps_hash:
            response["match_status"] = True #matched
        else:
            response["match_status"] = False #notmatched


    else: #işlemler sunucuda yapılacak

        software_list = request.json["software_list"]

        changes = []
        appends = []
        deleteds = {}

        for software in software_list:


            resp = DBOperations().find_one_query("col_live_app_data", {"_id": serial_number, "hostname": hostname, "apps.name": software["name"]},
                                                 {"apps.$": 1, "_id": 0})[0]
            resp = resp["apps"][0]
            if resp: #uygulama adı daha önceden kayıtlıymış

                change = {}
                if resp["hash"] != software["hash"]: #uygulamada değişiklik olmuş değerleri değiştir

                    for key in resp.keys():
                        try:
                            if resp[key] != software[key]:
                                change[f"apps.$.{key}"] = software[key]
                        except:
                            continue
                DBOperations().update_one_query("col_live_app_data", {"_id": serial_number, "hostname": hostname, "apps.name": software["name"]},
                                                {"$set": change})
                changes.append(change)
            else: #uygulama daha önceden kayıtlı değilmiş. Kayıt ekle
                software["detectdate"] = ""
                DBOperations().update_one_query("col_live_app_data",{"_id": serial_number, "hostname": hostname}, {"$push": {"apps": software}})


        for software in software_list: #kaldırılmis uygulamalari bulma
            pass

    return response

@app.route("conf", methods=["POST"])
def live_config():
    resp = DBOperations().find_one_query("col_live_configs",{})
    return resp

if __name__ == "__main__":
    # thread deamon araştır
    th = Thread(target=app.run(debug=True))
    th.start()
