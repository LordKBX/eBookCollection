import os
import re
import locale
import json.decoder
import traceback
import common.vars
from jsonschema import validate
from common.json_shema import JSONSchemaGenerator


def trim_lang(text: str = None) -> str:
    if text is not None:
        return text.replace('{APP_NAME}', common.vars.app_name)
    else:
        return None


class Dictionary:
    def __init__(self, data: dict):
        self.data = data
        self.language = locale.getdefaultlocale()[0]

    def __getitem__(self, value: str) -> any:
        """
        get an item from storage data

        :param value: index
        :return: str|None
        """
        try:
            if value not in self.data:
                return None
            else:
                if type(self.data[value]) == "dict":
                    return Dictionary(self.data[value])
                elif type(self.data[value]) == "str":
                    return trim_lang(self.data[value])
                else:
                    return self.data[value]
        except Exception:
            traceback.print_exc()
            return None


class Lang:
    default_language = 'en_US'
    language = None
    translations = dict()
    translations[default_language] = {
        "Label": "English (U.S.A)",
        "NotImplemented": "Not implemented",
        "Global": {
            "ArchiverErrorTitle": "Attention",
            "ArchiverErrorText": "Archiver folder not defined"
        },
        "Library": {
            "WindowTitle": "EbookCollection - Ebook manager",
            "AddBookWindowTitle": "EbookCollection - New books selection",
            "HeaderBlockBtnAddBook": "Add Ebook",
            "HeaderBlockBtnCreateBook": "Create Empty Ebook",
            "HeaderBlockBtnDelBook": "Delete Ebook",
            "HeaderBlockBtnSettings": "Settings",
            "SortingBlockTreeAll": "All",
            "SortingBlockTreeSeries": "Series",
            "SortingBlockTreeAuthors": "Authors",
            "SortingBlockSearchLabel": "Filter",
            "CentralBlockTableTitle": "Title",
            "CentralBlockTableAuthors": "Author",
            "CentralBlockTableSeries": "Serie",
            "CentralBlockTableTags": "Tags",
            "CentralBlockTableModified": "Modified",
            "CentralBlockTableAdded": "Imported",
            "CentralBlockTableContextMenu": {
                "EditMetadata": "Edit Metadata",
                "EditBook": "Edit eBook"
            },

            "InfoBlockTitleLabel": "Title",
            "InfoBlockSerieLabel": "Serie",
            "InfoBlockAuthorsLabel": "Author(s)",
            "InfoBlockFileFormatsLabel": "Format(s)",
            "InfoBlockSizeLabel": "Size",
            "InfoBlockSynopsisLabel": "Synopsis",

            "InfoBlockLinkContestMenu": {
                "open": "Open file with default application",
                "edit": "Edit file",
                "delete": "Delete file",
                "deleteBook": "Delete book"
            },

            "DialogConfirmDeleteBookWindowTitle": "Delete Ebook",
            "DialogConfirmDeleteBookWindowTitle2": "Delete Ebook file",
            "DialogConfirmDeleteBookWindowText": "Confirm Ebook remove ?",
            "DialogConfirmDeleteBookWindowText2": "Confirm file remove ?",
            "DialogConfirmDeleteBookBtnYes": "Yes",
            "DialogConfirmDeleteBookBtnNo": "No",

            "blockHeaderTitle": "  Toolbar",
            "blockSortTitle": "  Filters",
            "blockInfoTitle": "  Infos",

            "emptyBooks": {
                "WindowTitle": "Add empty eBook",
                "Number": "Quantity",
                "Authors": "Authors",
                "Series": "Series",
                "SeriesVolume": "Volume number",
                "Name": "eBook(s) title",
                "Format": "File format"
            },
            "emptyBookCreation": {
                "Cover": "Cover",
                "Chapter1": "Chapters 1",
                "Author": "Author:",
                "Authors": "Authors:"
            },
            "Metadata": {
                "WindowTitle": "Editing Metadata"
            }
        },
        "Generic": {
            "DialogBtnOk": "Ok",
            "DialogBtnSave": "Save",
            "DialogBtnYes": "Yes",
            "DialogBtnNo": "No",
            "DialogBtnCancel": "Cancel"
        },
        "Reader": {
            "WindowTitle": "EbookCollection: Reader",
            "DialogInfoNoFileWindowTitle": "File Error",
            "DialogInfoNoFileWindowText": "File Path not given",
            "DialogInfoBadFileWindowTitle": "File Error",
            "DialogInfoBadFileWindowText": "Invalid file format",
            "ContentTableHeader": "Content Table",
            "ContentTableTxtCover": "Cover",
            "ContentTableTxtEnd": "End",
            "ContentTableTxtPageX": "Page {}",
            "ContentTableTxtChapterX": "Chapter {}: {}",
            "InfoBlockHeader": "Informations",
            "InfoBlockText": "File: {FILE}\n\nTitle: {TITLE}\n\nSeries: {SERIES}\n\nAuthors: {AUTHORS}\n\nFormat: {FORMAT}\n\nSize: {SIZE}",
            "ContextMenuInfo": "Show eBook informations",
            "ContextMenuCT": "Show Content Table",
            "ContextMenuCopyText": "Copy text",
            "ContextMenuCopyHTML": "Copy HTML code"
        },
        "Editor": {
            "WindowTitle": "EbookCollection: Editor",
            "DialogInfoNoFileWindowTitle": "File Error",
            "DialogInfoNoFileWindowText": "File Path not given",
            "DialogInfoBadFileWindowTitle": "File Error",
            "DialogInfoBadFileWindowText": "Invalid file format",

            "BlockToolbar": {
                "Header": "Toolbar",
                "Save": "Save eBook",
                "CheckPointLoad": "Load session checkpoint",
                "CheckPointCreate": "Create session checkpoint",
                "FileManager": "File Management",
                "EditContentTable": "Edit Content Table"
            },
            "BlockFileListHeader": "Files explorer",
            "BlockContentTableHeader": "Content table",
            "BlockPreviewHeader": "Preview",

            "CentralZoneEmpty": "Please double click a file in the file explorer or an index in the content table for opening it in the editing zone",

            "ContentTableHeader": "Content Table",
            "FileTableHeader": "File Explorer",
            "WebViewDefaultPageContent": [
                "<?xml version=\"1.0\" encoding=\"utf-8\"?><html xmlns=\"http://www.w3.org/1999/xhtml\" lang=\"fr\">",
                "<head><title>Live Preview</title></head>",
                "<body><h3>Live Preview</h3>",
                "<p>You could see a here the live preview of the HTML file being edited. The preview will update automatically as you make your changes.</p>",
                "<p style=\"font-size:x-small;\">Note that this is a quick preview only, this is not intended to simulate a real digital book reader. Some aspects of your eBook will not work, such as page breaks and page margins.</p>",
                "</body></html>"
            ],
            "DialogConfirmSaveWindowTitle": "Save File",
            "DialogConfirmSaveWindowText": "Do you confirm saving the file changes ?",
            "DialogCreateCheckpointWindowTitle": "Create session checkpoint",
            "DialogCreateCheckpointWindowText": "Checkpoint {} successfuly created",
            "ChechpointWindow": {
                "WindowTitle": "Load Checkpoint",
                "btnOk": "Ok",
                "btnCancel": "Cancel"
            },
            "LinkWindow": {
                "WindowTitle": "Add/modify link",
                "labelUrl": "Link URL",
                "labelText": "Link text",
                "btnOk": "Ok",
                "btnCancel": "Cancel"
            },
            "ImgWindow": {
                "WindowTitle": "Add/modify image",
                "labelUrl": "Image URL",
                "labelText": "Image alternate texte",
                "btnOk": "Ok",
                "btnCancel": "Cancel"
            },
            "FilesWindow": {
                "WindowTitle": "Files manager",
                "ImportWindowTitle": "Import file",
                "FileNameWindowTitle": "Input name",
                "FileNameWindowLabel": "Name",
                "btnOk": "Ok",
                "btnCancel": "Cancel"
            },
            "ContentTableWindow": {
                "WindowTitle": "Content Table Editor",
                "ListLabel": "Content Table",
                "AddIndexLabel": "Insert new index",
                "AddIndexPlaceholder": "Index name",
                "ModifyIndexLabel": "Modify index",
                "BtnRename": "Rename index",
                "BtnDelete": "Delete index",
                "NameWindowTitle": "Input name",
                "NameWindowLabel": "Name",
                "btnOk": "Ok",
                "btnCancel": "Cancel"
            },
            "EditPane": {
                "Save": "Save File in session",
                "Undo": "Undo",
                "Redo": "Redo",
                "Cut": "Cut",
                "Copy": "Copy",
                "Paste": "Paste",
                "Debug": "Debug document",
                "Comment": "Comment selection",
                "Prettify": "Prettify File",
                "Bold": "Bold",
                "Italic": "Italic",
                "Underline": "Underline",
                "Strikethrough": "Strikethrough",
                "Sub": "Put text in sub line",
                "Sup": "Put text in super line",
                "TextColor": "Text Color",
                "BackColor": "Back Color",
                "AlignLeft": "Align Left",
                "AlignCenter": "Align Center",
                "AlignRight": "Align Right",
                "Align Justify": "Align Justify",
                "List": "List",
                "NumericList": "Numeric List",
                "Link": "Link",
                "Image": "Image"
            },
            "ColorPicker": {
                "WindowTitle": "Color Picker",
                "Palette": "Color palette",
                "ChromaGraph": "Chroma Graph",
                "RgbBox": "RGB",
                "RgbR": "R",
                "RgbG": "G",
                "RgbB": "B",
                "RgbHexa": "Hexa",
                "Preview": "Color Preview"
            }
        },
        "Time": {
            "template": {
                "numeric_date": "%m/%d/%Y",
                "numeric_datetime": "%m/%d/%Y %H:%M",
                "textual_date": "$month %d %Y",
                "textual_datetime": "$month %d %Y at %H:%M"
            },
            "months_short": ["jan.", "feb.", "march", "april", "may", "june", "july.", "aug.", "sept.", "oct.", "nov.",
                             "dec."],
            "months_full": [
                "January", "February", "March", "April", "May", "June", "July", "August",
                "September", "October", "November", "December"
            ]
        },
        "Settings": {
            "WindowTitle": "Settings",
            "TabGlobalTitle": "Global",
            "TabMetadataTitle": "Metadata",
            "TabPluginsTitle": "Plugins",
            "TabAboutTitle": "About",

            "LanguageGroupTitle": "Language",
            "LanguageAutomatic": "< System defined >",
            "LanguageImportTitle": "Import translation file",
            "Import": "Import",
            "ImportErrorTitle": "ERROR",
            "ImportErrorFileType": "File type invalid",
            "ImportErrorFileCorrupted": "File corrupted",

            "StyleGroupTitle": "Style",
            "StyleLight": "Light",
            "StyleDark": "Dark",
            "StyleImportTitle": "Import style file",

            "LibraryGroupTitle": "Library",
            "LibraryFolder": "Library storage folder",
            "LibraryFolderBrowse": "Browse...",

            "ArchiverGroupTitle": "Archiver",
            "ArchiverGroupTitleNT": "7zip",
            "ArchiverFolder": "Folder Path",
            "ArchiverFolderTest": "Test",
            "ArchiverFolderBrowse": "...",

            "DefaultCoverGroupTitle": "Default Cover Style",
            "DefaultCoverBackground": "Background Color",
            "DefaultCoverPattern": "Pattern",
            "DefaultCoverPatternColor": "Pattern Color",
            "DefaultCoverTitle": "Title Color",
            "DefaultCoverSeries": "Series Color",
            "DefaultCoverAuthors": "Authors Color",

            "eBookImportGroupTitle": "eBook Import settings",
            "eBookImportFilenameTpl": "File name parse template",
            "eBookImportFilenameTplSeparator": "File name parse separator",

            "AboutLabel": "{APP_NAME}\n\n License MIT\n\n Copyright (c) 2020-2021 Boulain Kévin",
            "AboutBtnLicense": "License",
            "AboutBtnWebsite": "Web Site",

            "pluginsSettingsButton": "Settings",
            "pluginsUninstallButton": "Uninstall",
            "pluginsSettingsTitle": "Settings of plugin-in '{}'",
            "pluginsForApp": "For App {}",
            "pluginsArchetype": "Type {}",

            "DialogConfirmDeletePluginWindowTitle": "Uninstall Plug-in",
            "DialogConfirmDeletePluginWindowText": "Confirm Plug-in Uninstall ?",
            "DialogConfirmDeletePluginBtnYes": "Yes",
            "DialogConfirmDeletePluginBtnNo": "No"
        }
    }

    def __init__(self):
        self.set_lang(locale.getdefaultlocale()[0])
        self.__load_langs()

    def __getitem__(self, value: str) -> any:
        """
        get an translation

        :param value: index
        :return: str|None
        """
        ln = self.test_lang(self.language)
        try:
            if '/' in value:
                return self.get(value, ln)
            if value not in self.translations[ln]:
                return None
            else:
                if type(self.translations[ln][value]) == "dict":
                    return Dictionary(self.translations[ln][value])
                elif type(self.translations[ln][value]) == "str":
                    return trim_lang(self.translations[ln][value])
                else:
                    return self.translations[ln][value]
        except Exception:
            return None

    def get(self, path: str, lang: str = None, compress: bool = True) -> str:
        lang = self.test_lang(lang)
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
                        if isinstance(base[obj], list) is True:
                            if compress is True:
                                return trim_lang("".join(base[obj]))
                            else:
                                return base[obj]
                        if isinstance(base[obj], str) is True:
                            return trim_lang(base[obj])
                        else:
                            return base[obj]
                else:
                    return None
        except Exception:
            traceback.print_exc()
            return None

    def test_lang(self, language_code: str = None) -> str:
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
                language_code = self.default_language
        return language_code

    def __load_langs(self) -> None:
        # self.translations.clear()
        directory = common.vars.app_directory + os.sep + "ressources" + os.sep + "langs"
        directory2 = common.vars.app_user_directory + os.sep + "imports" + os.sep + "langs"

        jssgenerator = JSONSchemaGenerator()
        encoder = json.encoder.JSONEncoder()
        print(self.translations)
        tab = encoder.encode(self.translations[self.default_language])
        jssgenerator.load(tab)
        schema = jssgenerator.generate()
        try:
            if common.vars.debug is True:
                with open(common.vars.app_directory + os.sep + "doc" + os.sep + "packages" + os.sep + "lang" + os.sep + "lang.json_schema", 'wt', encoding='utf8') as file:
                    file.write(json.dumps(schema, indent=4))
        except Exception:
            traceback.print_exc()

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
                                # test package JSON schema
                                validate(instance=tab, schema=schema)

                                print('lang '+nm+' OK')

                                self.translations[nm] = eval(content)
                            except Exception:
                                traceback.print_exc()
            except Exception:
                pass

    def refresh(self) -> None:
        self.__load_langs()

    def set_lang(self, lang: str) -> bool:
        if lang not in self.translations and lang != "auto":
            return False
        else:
            self.language = lang
            return True

    def get_langs(self) -> list:
        output = []
        for lang in self.translations:
            output.append({
                "code": lang,
                "name": self.translations[lang]['Label']
            })
        return output
