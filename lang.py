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
            'HeaderBlockBtnDelBook': 'Supprimer Livre(s)',
            'HeaderBlockBtnSettings': 'Options',
            'SortingBlockTreeAll': 'Tout',
            'SortingBlockTreeSeries': 'Séries',
            'SortingBlockTreeAuthors': 'Auteurs',
            'SortingBlockSearchLabel': 'Filtre',
            'CentralBlockTableTitle': 'Titre',
            'CentralBlockTableAuthors': 'Auteur',
            'CentralBlockTableSeries': 'Série',
            'CentralBlockTableTags': 'Étiquettes',
            'CentralBlockTableModified': 'Modifié le',
            'CentralBlockTableAdded': 'Ajouté le',
            'InfoBlockTitleLabel': 'Titre',
            'InfoBlockSerieLabel': 'Série',
            'InfoBlockAuthorsLabel': 'Auteur(s)',
            'InfoBlockFileFormatsLabel': 'Format(s)',
            'InfoBlockSizeLabel': 'Taille',
            'InfoBlockSynopsisLabel': 'Synopsis',
            'DialogConfirmDeleteBookWindowTitle': 'Confirmation de suppression Ebook',
            'DialogConfirmDeleteBookWindowText': 'Confirmez vous la suppression des Ebook sélectionnés ?',
            'DialogConfirmDeleteBookBtnYes': 'Oui',
            'DialogConfirmDeleteBookBtnNo': 'Non'
        }),
        'Generic': Dictionary({
            'DialogBtnOk': 'Compris'
        }),
        'Reader': Dictionary({
            'WindowTitle': 'EbookCollection: Lecteur Ebook',
            'DialogInfoNoFileWindowTitle': 'Erreur Fichier',
            'DialogInfoNoFileWindowText': 'Vous n\'avez pas fournis d\'adresse fichier',
            'DialogInfoBadFileWindowTitle': 'Erreur Fichier',
            'DialogInfoBadFileWindowText': 'Format de fichier invalide',
            'ContentTableHeader': 'Table des Matières',
            'ContentTableTxtCover': 'Couverture',
            'ContentTableTxtEnd': 'Fin',
            'ContentTableTxtPageX': 'Page {}',
            'ContentTableTxtChapterX': 'Chapitre {}: {}'
        }),
        'Editor': Dictionary({
            'WindowTitle': 'EbookCollection: Editeur',
            'DialogInfoNoFileWindowTitle': 'Erreur Fichier',
            'DialogInfoNoFileWindowText': 'Vous n\'avez pas fournis d\'adresse fichier',
            'DialogInfoBadFileWindowTitle': 'Erreur Fichier',
            'DialogInfoBadFileWindowText': 'Format de fichier invalide',
            'ContentTableHeader': 'Table des Matières',
            'FileTableHeader': 'Explorateur de fichiers',
            'WebViewDefaultPageContent': '<?xml version=\'1.0\' encoding=\'utf-8\'?><html xmlns="http://www.w3.org/1999/xhtml" lang="fr"><head><title>Prévisualisation en direct</title></head><body><h3>Prévisualisation en direct</h3><p>Vous verrez ici une prévisualisation en direct du fichier HTML en cours d\'édition. 	La prévisualisation se mettra à jour automatiquement au fur et à mesure de vos changements.</p><p>Notez que ceci est une prévisualisation rapide, ceci n\'est pas prévu pour simuler un réel lecteur de livre numérique.</p></body></html>',
        }),
        'Time': Dictionary({
            'template': Dictionary({
                'numeric_date': '%d/%m/%Y',
                'numeric_datetime': '%d/%m/%Y %H:%M',
                'textual_date': '%d $month %Y',
                'textual_datetime': '%d $month %Y à %H:%M'
            }),
            'months_short': ['janv.', 'fev.', 'mars', 'avril', 'mai', 'juin', 'juil.', 'août', 'sept.', 'oct.', 'nov.', 'déc.'],
            'months_full': ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre']
        })
    }

    translations['en_US'] = {
        'Home': Dictionary({
            'WindowTitle': 'EbookCollection - Ebook manager',
            'AddBookWindowTitle': 'EbookCollection - New books selection',
            'HeaderBlockBtnAddBook': 'Add Ebook',
            'HeaderBlockBtnDelBook': 'Delete Ebook',
            'HeaderBlockBtnSettings': 'Settings',
            'SortingBlockTreeAll': 'All',
            'SortingBlockTreeSeries': 'Series',
            'SortingBlockTreeAuthors': 'Authors',
            'SortingBlockSearchLabel': 'Filter',
            'CentralBlockTableTitle': 'Title',
            'CentralBlockTableAuthors': 'Author',
            'CentralBlockTableSeries': 'Serie',
            'CentralBlockTableTags': 'Tags',
            'CentralBlockTableModified': 'Modified',
            'CentralBlockTableAdded': 'Imported',
            'InfoBlockTitleLabel': 'Title',
            'InfoBlockSerieLabel': 'Serie',
            'InfoBlockAuthorsLabel': 'Author(s)',
            'InfoBlockFileFormatsLabel': 'Format(s)',
            'InfoBlockSizeLabel': 'Size',
            'InfoBlockSynopsisLabel': 'Synopsis',
            'DialogConfirmDeleteBookWindowTitle': 'Confirmation de suppression Ebook',
            'DialogConfirmDeleteBookWindowText': 'Confirmez vous la suppression des Ebook sélectionnés ?',
            'DialogConfirmDeleteBookBtnYes': 'Yes',
            'DialogConfirmDeleteBookBtnNo': 'No'
        }),
        'Generic': Dictionary({
            'DialogBtnOk': 'Compris'
        }),
        'Reader': Dictionary({
            'WindowTitle': 'EbookCollection: Reader',
            'DialogInfoNoFileWindowTitle': 'Erreur Fichier',
            'DialogInfoNoFileWindowText': 'Vous n\'avez pas fournis d\'adresse fichier',
            'DialogInfoBadFileWindowTitle': 'Erreur Fichier',
            'DialogInfoBadFileWindowText': 'Format de fichier invalide',
            'ContentTableHeader': 'Content Table',
            'ContentTableTxtCover': 'Cover',
            'ContentTableTxtEnd': 'End',
            'ContentTableTxtPageX': 'Page {}',
            'ContentTableTxtChapterX': 'Chapitre {}: {}'
        }),
        'Editor': Dictionary({
            'WindowTitle': 'EbookCollection: Editor',
            'DialogInfoNoFileWindowTitle': 'Erreur Fichier',
            'DialogInfoNoFileWindowText': 'Vous n\'avez pas fournis d\'adresse fichier',
            'DialogInfoBadFileWindowTitle': 'Erreur Fichier',
            'DialogInfoBadFileWindowText': 'Format de fichier invalide',
            'ContentTableHeader': 'Content Table',
            'FileTableHeader': 'File Explorer',
            'WebViewDefaultPageContent': '<?xml version=\'1.0\' encoding=\'utf-8\'?><html xmlns="http://www.w3.org/1999/xhtml" lang="fr"><head><title>Prévisualisation en direct</title></head><body><h3>Prévisualisation en direct</h3><p>Vous verrez ici une prévisualisation en direct du fichier HTML en cours d\'édition. 	La prévisualisation se mettra à jour automatiquement au fur et à mesure de vos changements.</p><p style="font-size:x-small;">Notez que ceci est une prévisualisation rapide 	uniquement, ceci n\'est pas prévu pour simuler un réel lecteur de livre numérique. Certains 	aspects de votre livre numérique ne fonctionneront pas, comme, les sauts de page et 	les marges de page.</p></body></html>',
        }),
        'Time': Dictionary({
            'template': Dictionary({
                'numeric_date': '%m/%d/%Y',
                'numeric_datetime': '%m/%d/%Y %H:%M',
                'textual_date': '$month %d %Y',
                'textual_datetime': '$month %d %Y at %H:%M'
            }),
            'months_short': ['jan.', 'feb.', 'march', 'april', 'may', 'june', 'july.', 'aug.', 'sept.', 'oct.', 'nov.', 'dec.'],
            'months_full': ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
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
