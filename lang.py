import locale


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
        if value not in self.data: return None
        else: return self.data[value]


class Lang:
    language = None
    translations = dict()
    translations['fr_FR'] = {
        'Home': Dictionary({
            'WindowTitle': 'EbookCollection - Gestionnaire de livre numérique',
            'AddBookWindowTitle': 'EbookCollection - Selection nouveaux livres',
            'HeaderBlockBtnAddBook': 'Ajouter Livre(s)',
            'HeaderBlockBtnSettings': 'Options',
            'SortingBlockTreeAll': 'Tout',
            'SortingBlockTreeSeries': 'Séries',
            'SortingBlockTreeAuthors': 'Auteurs',
            'CentralBlockTableTitle': 'Titre',
            'CentralBlockTableAuthors': 'Auteur',
            'CentralBlockTableSeries': 'Série',
            'CentralBlockTableTags': 'Étiquettes',
            'InfoBlockTitleLabel': 'Titre',
            'InfoBlockSerieLabel': 'Série',
            'InfoBlockAuthorsLabel': 'Auteur(s)',
            'InfoBlockFileFormatsLabel': 'Format(s)',
            'InfoBlockSizeLabel': 'Taille',
            'InfoBlockSynopsisLabel': 'Synopsis'
        })
    }

    translations['en_US'] = {
        'Home': Dictionary({
            'WindowTitle': 'EbookCollection - Ebook manager',
            'AddBookWindowTitle': 'EbookCollection - New books selection',
            'HeaderBlockBtnAddBook': 'Add Ebook',
            'HeaderBlockBtnSettings': 'Settings',
            'SortingBlockTreeAll': 'All',
            'SortingBlockTreeSeries': 'Series',
            'SortingBlockTreeAuthors': 'Authors',
            'CentralBlockTableTitle': 'Title',
            'CentralBlockTableAuthors': 'Author',
            'CentralBlockTableSeries': 'Serie',
            'CentralBlockTableTags': 'Tags',
            'InfoBlockTitleLabel': 'Title',
            'InfoBlockSerieLabel': 'Serie',
            'InfoBlockAuthorsLabel': 'Author(s)',
            'InfoBlockFileFormatsLabel': 'Format(s)',
            'InfoBlockSizeLabel': 'Size',
            'InfoBlockSynopsisLabel': 'Synopsis'
        })
    }

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
