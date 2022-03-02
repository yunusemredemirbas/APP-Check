
DB = """APP_INFOS"""


col_live_app_data = {
    "_id" : "serial_number",
    "hostname" : "", #bilgisayar adı
    "apps" : {}, #agentten gelen veriler
    "created_time" : "", #clientin eklendiği tarih
    "request_id" : None, #istekleri işlemek için gereken kontrol değeri, default değer None, bir dakika süreli
    "apps_hash": "", #sha256

}


col_deleted_host = {
    "serial_number" : "",#serial numarası buraya gelecek,
    "hostname" : "", #bilgisayar adı
    "deleted_time" : "", #timestamp
    "created_time" : "", #silmeden önce oluşturma zamanı
    "apps" : {}, #silme sırasında üzerinde bulunan uygulamalar
    "deleted_apps" : {} #silmeden önce ilgili bilgisayardan kaldırılan uygulamalar

}


col_deleted_apps = {
    "serial_number" : "",#serial numarası buraya gelecek,
    "hostname" : "", #bilgisayar adı
    "deleted_time" : "", #timestamp
    "app_info" : {}
}

col_enrollment = {
    "enroll_id" : "",
    "enroll_pass" : "", #sha256
    "change_date" : "" #timestamp

}

apps = {
    "FileZilla Client 3.55.1" : {'name': 'FileZilla Client 3.55.1',
                                 'version': '3.55.1',
                                 'installdate': '',
                                 'installsource': '',
                                 'installlocation': 'C:\\Program Files\\FileZilla FTP Client',
                                 'uninstallstring': '"C:\\Program Files\\FileZilla FTP Client\\uninstall.exe"',
                                 'publisher': 'Tim Kosse',
                                 'hash' : '',
                                 'detectdate': ''}

}

col_live_configs = {
    "sleep_time" : 30 #dakika
}