import configparser

class ConfigParser():
    def __init__(self, file_path):
        self.file_path = file_path
        self.conf_parser = configparser.ConfigParser()
        self.conf_parser.read(file_path, encoding="utf-8")

        self.conf = {}
        for s in self.conf_parser.sections():
            dict_s = {}
            for k,v in self.conf_parser.items(s):
                dict_s[k] = str(v)
            self.conf[s] = dict_s

    def get_conf(self):
        return self.conf


