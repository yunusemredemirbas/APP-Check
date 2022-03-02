import time

from requests import post,get
from getpass import getpass
from hashlib import sha256
from socket import gethostname
import os
import cgi
import shutil
import winreg


server_ip = "localhost"  # input("Sunucu ip adresini/dnsini giriniz: ")
server_port = "5000"  # input("Sunucu portunu giriniz: ")



def set_autostart_registry(app_name, key_data=None, autostart: bool = True) -> bool:
    """
    Create/update/delete Windows autostart registry key

    ! Windows ONLY
    ! If the function fails, OSError is raised.

    :param app_name:    A string containing the name of the application name
    :param key_data:    A string that specifies the application path.
    :param autostart:   True - create/update autostart key / False - delete autostart key
    :return:            True - Success / False - Error, app name dont exist
    """

    with winreg.OpenKey(
            key=winreg.HKEY_LOCAL_MACHINE,
            sub_key=r'Software\Microsoft\Windows\CurrentVersion\Run',
            reserved=0,
            access=winreg.KEY_ALL_ACCESS,
    ) as key:
        try:
            if autostart:
                winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, key_data)
            else:
                winreg.DeleteValue(key, app_name)
        except OSError:
            return False
    return True


def download_url(url, directory):
    """Download file from url to directory

    URL is expected to have a Content-Disposition header telling us what
    filename to use.

    Returns filename of downloaded file.

    """
    response = get(url, stream=True)
    if response.status_code != 200:
        raise ValueError('Failed to download')

    params = cgi.parse_header(response.headers.get('Content-Disposition', ''))[-1]
    if 'filename' not in params:
        raise ValueError('Could not find a filename')

    filename = os.path.basename(params['filename'])
    abs_path = os.path.join(directory, filename)
    with open(abs_path, 'wb') as target:
        response.raw.decode_content = True
        shutil.copyfileobj(response.raw, target)


    print("İndirme tamamlandı ", abs_path)

def get_serial_number():
    # kaynak : https://gist.github.com/angeloped/3febaaf71ac083bc2cd5d99d775921d0#file-get_serial_number-py
    command = "wmic bios get serialnumber"
    return os.popen(command).read().replace("\n", "").replace("	", "").replace(" ", "").replace("SerialNumber", "")


hostname = gethostname()
serial_number = get_serial_number()

while True:
    enrollment_id = "kayt"  # input("Kayit kimligini giriniz: ")
    # enrollment_pass = getpass(prompt='Password: ', stream=None)
    enrollment_pass = "123"

    hsh_sha256 = sha256()
    hsh_sha256.update(enrollment_pass.encode("utf-8"))
    enrollment_pass = hsh_sha256.hexdigest()


    data = {
        "enrollment_id": enrollment_id,
        "enrollment_pass": enrollment_pass,
        "hostname": hostname,
        "serial_number": serial_number
    }


    BASE_URL = f"http://{server_ip}:{server_port}/"
    url_enroll = "enroll"
    req = post(BASE_URL + url_enroll, json=data)

    req_data = req.json()
    print(req_data)

    def appcheck_path():
        systemdrive = os.environ["SYSTEMDRIVE"]
        appcheckfolder = "\\Program Files\AppCheck"
        path = systemdrive + appcheckfolder
        if not os.path.exists(path):
            os.mkdir(path)
        return path
    if req_data["id_and_pass"]:
        secim = int(input("Uygulamanın idirilmesini istediğiniz klasörü seciniz.\n"
                          "1 - Download Klasörü\n"
                          "2 - AppCheck Uygulama Klasörü\n"
                          "Seciminiz: "))



        if secim == 2:
            path = appcheck_path()
            download_url(BASE_URL + "setup", path)
        else:

            userpath = os.environ["USERPROFILE"]
            path = userpath + "\\Downloads"
            download_url(BASE_URL + "setup", path)
    else:
        tekrar = input("Kayıt id veya parola hatalı.\nBilgileri tekrar girmek için E/e harfini girerek Enter'a basınız.\n"
                       "Kurulumu sonlandırmak için direkt Enter'a basabilirsiniz.").lower()
        if tekrar != "e":
            print("Kurulum sonlandırılıyor...")
            exit()
    kurulum = input("Kuruluma devam edilsin mi E/e yazıp 'Enter' a basınız."
                    "Kurulumu sonlandırmak için direkt Enter'a basabilirsiniz.").lower()
    if kurulum == "e":

        with open(appcheck_path()+"\config.txt", "w") as f:
            f.write(f"""server_ip:{server_ip}\nserver_port:{server_port}""")
        appchck = appcheck_path() + "\\AppCheck.exe"
        set_autostart_registry("appcheck", appchck)

        print("Otomatik başlatmak için registry ayarları yapıldı.")

        os.startfile(appchck)

        print("Agent başlatıldı")
        print("Kurulum Tamamlandı")
        input("Exiting...")
        time.sleep(3)
        exit()

    print("Kurulum sonlandırılıyor...")
    exit()