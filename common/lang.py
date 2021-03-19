import os
import re
import locale
import json.decoder
import traceback
import common.vars


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
    __default_language = 'en_US'
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
        ln = self.__test_lang(self.language)
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
        lang = self.__test_lang(lang)
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

    def __test_lang(self, language_code: str = None) -> str:
        if language_code is None:
            language_code = self.language
        if language_code == 'auto':
            language_code = locale.getdefaultlocale()[0]
        if language_code not in self.translations:
            passed = False
            tl = locale.getdefaultlocale()[0].split('_')
            for lc in self.translations:
                tlc = lc.split('_')
                if tl[0] == tlc[0]:
                    language_code = lc
                    passed = True
                    break
            if passed is False:
                language_code = self.__default_language
        return language_code

    def __load_langs(self):
        self.translations.clear()
        directory = common.vars.app_directory + os.sep + "ressources" + os.sep + "langs"
        directory2 = common.vars.app_user_directory + os.sep + "imports" + os.sep + "langs"
        ext = "json"
        for dir in [directory, directory2]:
            try:
                print(dir)
                for root, directories, files in os.walk(dir, topdown=False):
                    for name in files:
                        if re.search("\\.({})$".format(ext), name) is None:
                            continue
                        else:
                            try:
                                nm = name.replace(".json", "")
                                fp = open(dir + os.sep + name, "r", encoding="utf8")
                                content = fp.read()
                                fp.close()

                                # test JSON validity
                                decoder = json.decoder.JSONDecoder()
                                tab = decoder.decode(content)

                                self.translations[nm] = eval(
                                    content.replace('{APP_NAME}', common.vars.app_name)  # .replace('[', '"\\n".join([').replace(']', '])')
                                )
                            except Exception:
                                pass
            except Exception:
                pass

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
