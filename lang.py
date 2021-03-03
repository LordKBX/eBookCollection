import os
import sys
import re
import imp
import locale
import json.decoder
import traceback
import vars


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
        self.__load_langs()
        self.set_lang(locale.getdefaultlocale()[0])

    def __getitem__(self, value: str):
        """
        get an translation

        :param value: index
        :return: str|None
        """
        ln = self.language
        if ln == 'auto':
            ln = locale.getdefaultlocale()[0]
        if ln not in self.translations:
            ln = 'en_US'
        try:
            if '/' in value:
                return self.get(value, ln)
            if value not in self.translations[ln]:
                return None
            else:
                if type(self.translations[ln][value]) == "dict":
                    return Dictionary(self.translations[ln][value])
                else:
                    return self.translations[ln][value]
        except Exception:
            return None

    def get(self, path: str, lang: str = None):
        if lang is None:
            lang = self.language
        if lang == 'auto':
            lang = locale.getdefaultlocale()[0]
        if lang not in self.translations:
            lang = 'en_US'
        if lang not in self.translations:
            return None
        path_tab = path.split('/')
        try:
            base = self.translations[lang]
            for obj in path_tab:
                if obj in base:
                    if isinstance(base[obj], dict) is True:
                        base = base[obj]
                    else:
                        return base[obj]
                else:
                    return None
        except Exception:
            traceback.print_exc()
            return None

    def __load_langs(self):
        self.translations.clear()
        directory = os.path.dirname(os.path.realpath(__file__)) + os.sep + "ressources" + os.sep + "langs"
        ext = "json"
        for root, directories, files in os.walk(directory, topdown=False):
            for name in files:
                if re.search("\\.({})$".format(ext), name) is None:
                    continue
                else:
                    nm = name.replace(".json", "")
                    fp = open(directory + os.sep + name, "r", encoding="utf8")
                    content = fp.read()
                    fp.close()
                    decoder = json.decoder.JSONDecoder()
                    tab = decoder.decode(content)
                    self.translations[nm] = eval(
                        content.replace('[', '"\\n".join([').replace(']', '])').replace('{APP_NAME}', vars.app_name)
                    )

    def refresh(self):
        self.__load_langs()

    def set_lang(self, lang: str):
        if lang not in self.translations and lang != "auto":
            return False
        else:
            self.language = lang
            return True

    def get_langs(self):
        output = []
        for lang in self.translations:
            output.append({
                "code": lang,
                "name": self.translations[lang]['Label']
            })
        return output
