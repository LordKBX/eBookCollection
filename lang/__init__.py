import os
import sys
import re
import imp
import locale
import json.decoder


class Dictionary:
    def __init__(self, data: dict):
        self.data = data
        self.language = locale.getdefaultlocale()[0]

    def __getitem__(self, value: str):
        """
        get an item from storage data

        :param value: index
        :return: str|None
        """
        if value not in self.data:
            return None
        else:
            if type(self.data[value]) == "dict":
                return Dictionary(self.data[value])
            else:
                return self.data[value]


class Lang:
    language = None
    translations = dict()

    def __init__(self):
        self.language = locale.getdefaultlocale()[0]

        ext = "json"
        for root, directories, files in os.walk(os.path.dirname(os.path.realpath(__file__)), topdown=False):
            for name in files:
                if re.search("\\.({})$".format(ext), name) is None:
                    continue
                else:
                    nm = name.replace(".json", "")
                    fp = open(os.path.dirname(os.path.realpath(__file__)) + os.sep + name, "r", encoding="utf8")
                    content = fp.read()
                    fp.close()
                    decoder = json.decoder.JSONDecoder()
                    tab = decoder.decode(content)
                    self.translations[nm] = eval(content)

    def __getitem__(self, value: str):
        """
        get an translation

        :param value: index
        :return: str|None
        """
        ln = self.language
        if ln not in self.translations:
            ln = 'en_US'
        if value not in self.translations[ln]:
            return None
        else:
            if type(self.translations[ln][value]) == "dict":
                return Dictionary(self.translations[ln][value])
            else:
                return self.translations[ln][value]
