import hashlib
from json import dumps


class Calculate_hash:

    md5 = hashlib.md5()
    sha256 = hashlib.sha256()

    def list_dict_to_md5(self, data):

        encoded = dumps(data, sort_keys=True).encode()
        self.md5.update(encoded)
        return self.md5.hexdigest()


    def str_to_md5(self, data):

        encoded = data.encode()
        self.md5.update(encoded)
        return self.md5.update(encoded)

b = {'name': 'FileZilla Client 3.55.1', 'version': '3.55.1', 'installdate': '', 'installsource': '', 'installlocation': 'C:\\Program Files\\FileZilla FTP Client', 'uninstallstring': '"C:\\Program Files\\FileZilla FTP Client\\uninstall.exe"', 'publisher': 'Tim Kosse'}
a = {'name': 'FileZilla Client 3.55.1', 'version': '3.55.1', 'installdate': '', 'installsource': '', 'installlocation': 'C:\\Program Files\\FileZilla FTP Client', 'uninstallstring': '"C:\\Program Files\\FileZilla FTP Client\\uninstall.exe"', 'publisher': 'Tim Kosse'}
print(Calculate_hash().list_dict_to_md5({'name': 'FileZilla Client 3.55.1', 'version': '3.55.1', 'installdate': '', 'installsource': '', 'installlocation': 'C:\\Program Files\\FileZilla FTP Client', 'uninstallstring': '"C:\\Program Files\\FileZilla FTP Client\\uninstall.exe"', 'publisher': 'Tim Kosse'}))
#86d535ebe65e8ddab9bcbebb15639448