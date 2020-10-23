import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from lang.obj import *

data = {
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
            'DialogBtnOk': 'Compris',
            'DialogBtnYes': 'Oui',
            'DialogBtnNo': 'Non',
            'DialogBtnCancel': 'Annuler'
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
            'DialogConfirmSaveWindowTitle': 'Sauvegarde fichier',
            'DialogConfirmSaveWindowText': 'Confirmez vous la sauvegarde du fichier ?',
            'DialogCreateCheckpointWindowTitle': 'Création checkpoint session',
            'DialogCreateCheckpointWindowText': 'Checkpoint {} crée avec success',
            'LinkWindow': Dictionary({
                'WindowTitle': 'Ajout/Modification lien',
                'labelUrl': 'URL du lien',
                'labelText': 'Texte du lien',
                'btnOk': 'Ok',
                'btnCancel': 'Annuler'
            }),
            'ImgWindow': Dictionary({
                'WindowTitle': 'Ajout/Modification image',
                'labelUrl': 'URL de l\'image',
                'labelText': 'Texte alternatif',
                'btnOk': 'Ok',
                'btnCancel': 'Annuler'
            }),
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