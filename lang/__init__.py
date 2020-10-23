import os, sys
import locale
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from lang.obj import *
import lang.fr_FR
import lang.en_US


class Lang:
    language = None
    translations = dict()
    translations['fr_FR'] = lang.fr_FR.data
    translations['en_US'] = lang.en_US.data

    def __init__(self):
        self.language = locale.getdefaultlocale()[0]

    def __getitem__(self, value: str):
        """
        get an translation

        :param value: index
        :return: str|None
        """
        ln = self.language
        if ln not in self.translations: ln = 'en_US'
        if value not in self.translations[ln]: return None
        else: return self.translations[ln][value]
