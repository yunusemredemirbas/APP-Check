import os
import winreg
import hash
from socket import gethostname
import json
from requests import post
from time import sleep

def appcheck_path():
    systemdrive = os.environ["SYSTEMDRIVE"]
    appcheckfolder = "\\Program Files\AppCheck"
    path = systemdrive + appcheckfolder
    if not os.path.exists(path):
        os.mkdir(path)
    return path


def get_serial_number():
    # kaynak : https://gist.github.com/angeloped/3febaaf71ac083bc2cd5d99d775921d0#file-get_serial_number-py
    command = "wmic bios get serialnumber"
    return os.popen(command).read().replace("\n", "").replace("	", "").replace(" ", "").replace("SerialNumber", "")

def conflist_to_dict(list):
    tut = {}
    for i in list:
        i = i.split(":")
        tut[i[0].strip()] = i[1].strip()
    return tut

def installed_apps(hive, flag):
    aReg = winreg.ConnectRegistry(None, hive)
    aKey = winreg.OpenKey(aReg, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
                          0, winreg.KEY_READ | flag)

    count_subkey = winreg.QueryInfoKey(aKey)[0]

    software_list = []
    for i in range(count_subkey):
        software = {}
        try:
            asubkey_name = winreg.EnumKey(aKey, i)
            asubkey = winreg.OpenKey(aKey, asubkey_name)
            software['name'] = winreg.QueryValueEx(asubkey, "DisplayName")[0]

            try:
                software['version'] = str(winreg.QueryValueEx(asubkey, "DisplayVersion")[0])
            except:
                software['version'] = ''
            try:
                software['installdate'] = str(winreg.QueryValueEx(asubkey, "InstallDate")[0])
            except:
                software['installdate'] = ''
            try:
                software['installsource'] = str(winreg.QueryValueEx(asubkey, "InstallSource")[0])
            except:
                software['installsource'] = ''
            try:
                software['installlocation'] = str(winreg.QueryValueEx(asubkey, "InstallLocation")[0])
            except:
                software['installlocation'] = ''
            try:
                software['uninstallstring'] = str(winreg.QueryValueEx(asubkey, "UninstallString")[0])
            except:

                try:
                    software['uninstallstring'] = str(winreg.QueryValueEx(asubkey, "UninstallString_Hidden")[0])

                except:
                    software['uninstallstring'] = ''

            try:
                software['publisher'] = str(winreg.QueryValueEx(asubkey, "Publisher")[0])
            except:
                software['publisher'] = ''

            software["hash"] = hash.Calculate_hash().list_dict_to_md5(software)
            software_list.append(software)
        except:
            continue

    return software_list




hostname = gethostname()
serial_number = get_serial_number()

with open(appcheck_path()+"\\config.txt", "r") as f:
    conf = f.read().splitlines()

conf = conflist_to_dict(conf)
server_address = conf["server_address"]
server_port = conf["server_port"]


BASE_URL = f"http://{server_address}:{server_port}/"
data = {
        "hostname": hostname,
        "serial_number": serial_number
    }

while True:
    software_list = installed_apps(winreg.HKEY_LOCAL_MACHINE, winreg.KEY_WOW64_32KEY) + installed_apps(
        winreg.HKEY_LOCAL_MACHINE, winreg.KEY_WOW64_64KEY) + installed_apps(winreg.HKEY_CURRENT_USER, 0)
    apps_hash = hash.Calculate_hash().list_dict_to_md5(software_list)
    data["request_code"] = 0
    data["apps_hash"] = apps_hash

    req = post(BASE_URL + "check", json=data)
    resp = req.json()

    live_conf = post(BASE_URL + "conf")


    if not resp["match_status"]: #app eşleşmemişse



    sleep(int(live_conf["sleep_time"]) * 60)