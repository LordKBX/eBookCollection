import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from lang.obj import *

data = {
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
            'DialogBtnOk': 'Compris',
            'DialogBtnYes': 'Oui',
            'DialogBtnNo': 'Non',
            'DialogBtnCancel': 'Annuler'
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
            'FilesWindow': Dictionary({
                'WindowTitle': 'Gestion des fichiers',
                'ImportWindowTitle': 'Importation de fichier fichiers',
                'FileNameWindowTitle': 'Saisissez un nom',
                'FileNameWindowLabel': 'Nom',
                'btnOk': 'Ok',
                'btnCancel': 'Annuler'
            }),
            'ContentTableWindow': Dictionary({
                'WindowTitle': 'Edition table des matières',
                'ListLabel': 'Table des matières',
                'AddIndexLabel': 'Insérer un index',
                'AddIndexPlaceholder': 'Nom d\'index',
                'ModifyIndexLabel': 'Modification d\'un index',
                'BtnRename': 'Renommer index',
                'BtnDelete': 'Supprimer index',

                'NameWindowTitle': 'Saisissez un nom',
                'NameWindowLabel': 'Nom',
                'btnOk': 'Ok',
                'btnCancel': 'Annuler'
            }),
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