# This Python file uses the following encoding: utf-8
import os, sys, traceback
from PyQt5.QtWidgets import *
import PyQt5.sip
import PyQt5.QtCore
import PyQt5.QtGui
import PyQt5.uic
from PyQt5.uic import *

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
import common.common
import common.files
import common.books
from common.vars import *


class SettingsWindow(QDialog):
    def __init__(self, parent, bdd):
        super(SettingsWindow, self).__init__(parent, QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
        self.BDD = bdd
        PyQt5.uic.loadUi(os.path.dirname(os.path.realpath(__file__)) + os.sep + 'settings.ui'.replace('/', os.sep), self)  # Load the .ui file

        self.color_selectors = [
            'tab_metadata_default_cover_background_combo_box',
            'tab_metadata_default_cover_pattern_color_combo_box',
            'tab_metadata_default_cover_title_combo_box',
            'tab_metadata_default_cover_series_combo_box',
            'tab_metadata_default_cover_authors_combo_box'
        ]

        self.lng = parent.lang  # language
        self.app_lang = self.BDD.get_param('lang')
        self.app_style = self.BDD.get_param('style')
        self.load_languages(self.app_lang)
        self.load_styles(self.app_style)

        self.dialog_tabs.setCurrentIndex(0)

        #GLOBAL tab
        self.tab_global_lang_combo_box.currentIndexChanged.connect(self.change_language)
        self.tab_global_style_combo_box.currentIndexChanged.connect(self.change_style)

        self.tab_global_library_folder_btn.clicked.connect(self.change_library_folder)
        self.tab_global_library_folder_line_edit.setText(self.BDD.get_param('library/directory'))

        path = self.BDD.get_param('archiver_dir')
        if path is None or path == '':
            path = env_vars['tools']['archiver']['path']
        if path is None or path == '':
            path = '<UNKNOW>'
        self.tab_global_archiver_folder_line_edit.setText(path)
        self.tab_global_archiver_folder_test_btn.clicked.connect(self.test_archiver)
        self.tab_global_archiver_folder_browse_btn.clicked.connect(self.change_archiver_folder)

        # METADATA tab
        default_cover_background = self.BDD.get_param('defaultCover/background')
        default_cover_pattern = self.BDD.get_param('defaultCover/pattern')
        default_cover_pattern_color = self.BDD.get_param('defaultCover/pattern_color')
        default_cover_title = self.BDD.get_param('defaultCover/title')
        default_cover_series = self.BDD.get_param('defaultCover/series')
        default_cover_authors = self.BDD.get_param('defaultCover/authors')

        for selector in self.color_selectors:
            selector_type = selector.replace('tab_metadata_default_cover_', '').replace('_combo_box', '')
            combo = eval('self.'+selector)
            # combo = QComboBox()
            model = combo.model()
            selected = 0
            nb = 0
            for color in env_vars['vars']['default_cover']['colors']:
                entry = PyQt5.QtGui.QStandardItem('███')
                entry.setForeground(PyQt5.QtGui.QColor(color))
                entry.setData(color, 99)
                model.appendRow(entry)
                # print('color = ', color)
                # print('default_cover_' + selector_type + ' = ', eval('default_cover_'+selector_type))
                if color == eval('default_cover_'+selector_type):
                    selected = nb
                nb += 1
            # print('selected = ', selected)
            combo.setCurrentIndex(selected)
            combo.currentIndexChanged.connect(self.cover_combo_changed)

        selected = 0
        nb = 0
        model = self.tab_metadata_default_cover_pattern_combo_box.model()
        for pattern in env_vars['vars']['default_cover']['patterns']:
            entry = PyQt5.QtGui.QStandardItem(pattern)
            entry.setData(pattern, 99)
            model.appendRow(entry)
            if pattern == default_cover_pattern:
                selected = nb
            nb += 1
        self.tab_metadata_default_cover_pattern_combo_box.setCurrentIndex(selected)
        self.tab_metadata_default_cover_pattern_combo_box.currentIndexChanged.connect(self.cover_combo_changed)
        self.cover_combo_changed()

        filename_template = self.BDD.get_param('import_file_template')
        selected = 0
        for index in env_vars['vars']['import_file_template']:
            if index == 'default':
                continue
            if filename_template == env_vars['vars']['import_file_template'][index]:
                selected = self.tab_metadata_import_filename_template_combo_box.count()
            self.tab_metadata_import_filename_template_combo_box.insertItem(
                self.tab_metadata_import_filename_template_combo_box.count(),
                env_vars['vars']['import_file_template'][index]
            )
        self.tab_metadata_import_filename_template_combo_box.setCurrentIndex(selected)
        self.tab_metadata_import_filename_separator_line_edit.setText(self.BDD.get_param('import_file_separator'))

        self.tab_about_btn_license.clicked.connect(lambda: os.system("start " + app_directory + os.sep + 'LICENSE.txt'))
        self.tab_about_btn_website.clicked.connect(lambda: os.system("start https://github.com/LordKBX/eBookCollection"))

        self.apply_style()
        self.apply_translation()

    def open_exec(self):
        ret = self.exec_()  # Show the GUI
        if ret == 1:
            new_folder = self.tab_global_library_folder_line_edit.text()
            if self.BDD.get_param('library/directory') != new_folder:
                self.BDD.migrate(new_folder)

            parse_list = [
                'tab_metadata_default_cover_background_combo_box',
                'tab_metadata_default_cover_pattern_combo_box',
                'tab_metadata_default_cover_pattern_color_combo_box',
                'tab_metadata_default_cover_title_combo_box',
                'tab_metadata_default_cover_series_combo_box',
                'tab_metadata_default_cover_authors_combo_box'
            ]
            for id in parse_list:
                selector = id.replace('tab_metadata_default_cover_', '').replace('_combo_box', '')
                self.BDD.set_param(
                    'defaultCover/'+selector,
                    eval('self.'+id+'.currentData(99)')
                )

            template = self.tab_metadata_import_filename_template_combo_box.currentText()
            if self.BDD.get_param('import_file_template') != template:
                self.BDD.set_param('import_file_template', template)

            template_separator = self.tab_metadata_import_filename_separator_line_edit.text()
            if self.BDD.get_param('import_file_separator') != template_separator:
                self.BDD.set_param('import_file_separator', template_separator)

            return 'ok'
        else:
            self.lng.set_lang(self.app_lang)
            self.BDD.set_param('lang', self.app_lang)
            self.BDD.set_param('style', self.app_style)
            return None

    def change_library_folder(self):
        print("test")
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        options |= QFileDialog.Directory

        dlg = QFileDialog()
        dlg.setOptions(options)
        dlg.setFileMode(QFileDialog.Directory)

        preset = self.BDD.get_param("library_directory").replace('{APP_DIR}', app_directory)
        folder = dlg.getExistingDirectory(self, "Choose Directory", preset).replace(app_directory, '{APP_DIR}')
        print(folder)
        self.tab_global_library_folder_line_edit.setText(folder)

    def load_languages(self, selected_lang: str = None):
        self.tab_global_lang_combo_box.clear()
        self.tab_global_lang_combo_box.addItem(self.lng['Settings']['LanguageAutomatic'])
        self.tab_global_lang_combo_box.setItemData(self.tab_global_lang_combo_box.count() - 1, 'auto', 99)
        languages = self.lng.get_langs()
        i = 1
        sel = 0
        for lg in languages:
            self.tab_global_lang_combo_box.addItem(lg['name'])
            self.tab_global_lang_combo_box.setItemData(self.tab_global_lang_combo_box.count() - 1,
                                                       lg['code'], 99)
            if selected_lang == lg['code']:
                sel = i
            i += 1
        self.tab_global_lang_combo_box.setCurrentIndex(sel)

    def load_styles(self, selected_style: str = None):
        self.tab_global_style_combo_box.clear()
        i = 0
        sel = 0
        for style in env_vars['styles']:
            st = self.lng['Settings/Style'+style]
            if st is None:
                st = style
            self.tab_global_style_combo_box.addItem(st)
            self.tab_global_style_combo_box.setItemData(self.tab_global_style_combo_box.count() - 1, style, 99)
            if selected_style == style:
                sel = i
            i += 1
        self.tab_global_style_combo_box.setCurrentIndex(sel)

    def change_language(self):
        index = self.tab_global_lang_combo_box.currentIndex()
        selected_lang = self.tab_global_lang_combo_box.itemData(index, 99)
        self.lng.set_lang(selected_lang)
        self.BDD.set_param('lang', selected_lang)
        self.apply_translation()

    def change_style(self):
        index = self.tab_global_style_combo_box.currentIndex()
        selected_style = self.tab_global_style_combo_box.itemData(index, 99)
        self.BDD.set_param('style', selected_style)
        self.apply_style(selected_style)

    def apply_translation(self):
        try:
            self.setWindowTitle(self.lng['Settings/WindowTitle'])
            self.button_box.button(QDialogButtonBox.Ok).setText(self.lng.get('Generic/DialogBtnSave'))
            self.button_box.button(QDialogButtonBox.Cancel).setText(self.lng.get('Generic/DialogBtnCancel'))

            # Tabs
            self.dialog_tabs.setTabText(0, self.lng['Settings/TabGlobalTitle'])
            self.dialog_tabs.setTabText(1, self.lng['Settings/TabMetadataTitle'])
            self.dialog_tabs.setTabText(2, self.lng['Settings/TabConversionTitle'])
            self.dialog_tabs.setTabText(3, self.lng['Settings/TabAboutTitle'])

            # tab_global
            #   lang group
            self.tab_global_lang_group_box.setTitle(self.lng['Settings/LanguageGroupTitle'])
            self.tab_global_lang_combo_box.setItemText(0, self.lng['Settings/LanguageAutomatic'])
            self.tab_global_lang_btn.setText(self.lng['Settings/Import'])

            #   style group
            self.tab_global_style_group_box.setTitle(self.lng['Settings/StyleGroupTitle'])
            self.tab_global_style_import_btn.setText(self.lng['Settings/Import'])
            for index in range(0, self.tab_global_style_combo_box.count()):
                data = self.tab_global_style_combo_box.itemData(index, 99)
                st = self.lng["Settings/Style" + data]
                if st is None:
                    st = data
                self.tab_global_style_combo_box.setItemText(index, st)

            #   Library group
            self.tab_global_library_group_box.setTitle(self.lng['Settings/LibraryGroupTitle'])
            self.tab_global_library_folder_label.setText(self.lng['Settings/LibraryFolder'])
            self.tab_global_library_folder_btn.setText(self.lng['Settings/LibraryFolderBrowse'])

            #   archiver group
            if os.name == 'nt':
                self.tab_global_archiver_group_box.setTitle(self.lng['Settings/ArchiverGroupTitleNT'])
            else:
                self.tab_global_archiver_group_box.setTitle(self.lng['Settings/ArchiverGroupTitle'])
            self.tab_global_archiver_folder_label.setText(self.lng['Settings/ArchiverFolder'])
            self.tab_global_archiver_folder_test_btn.setText(self.lng['Settings/ArchiverFolderTest'])
            self.tab_global_archiver_folder_browse_btn.setText(self.lng['Settings/ArchiverFolderBrowse'])

            # tab_metadata
            #   Default Cover group
            self.tab_metadata_default_cover_group_box.setTitle(self.lng['Settings/DefaultCoverGroupTitle'])
            self.tab_metadata_default_cover_background_label.setText(self.lng['Settings/DefaultCoverBackground'])
            self.tab_metadata_default_cover_pattern_label.setText(self.lng['Settings/DefaultCoverPattern'])
            self.tab_metadata_default_cover_pattern_color_label.setText(self.lng['Settings/DefaultCoverPatternColor'])
            self.tab_metadata_default_cover_title_label.setText(self.lng['Settings/DefaultCoverTitle'])
            self.tab_metadata_default_cover_series_label.setText(self.lng['Settings/DefaultCoverSeries'])
            self.tab_metadata_default_cover_authors_label.setText(self.lng['Settings/DefaultCoverAuthors'])

            #   eBook import
            self.tab_metadata_import_group_box.setTitle(self.lng['Settings/eBookImportGroupTitle'])
            self.tab_metadata_import_filename_template_label.setText(self.lng['Settings/eBookImportFilenameTpl'])
            self.tab_metadata_import_filename_separator_label.setText(self.lng['Settings/eBookImportFilenameTplSeparator'])

            # tab_about
            #   About group
            self.tab_about_btn_license.setText(self.lng['Settings/AboutBtnLicense'])
            self.tab_about_btn_website.setText(self.lng['Settings/AboutBtnWebsite'])
            self.tab_about_label.setText(self.lng['Settings/AboutLabel'])

        except Exception:
            traceback.print_exc()

    def apply_style(self, style: str = None):
        if style is None:
            style = self.BDD.get_param('style')
        cursor = QtGui.QCursor(QtCore.Qt.PointingHandCursor)
        self.setStyleSheet(env_vars['styles'][style]['QDialog'])

        cls = self.__dir__()
        for var_name in cls:
            obj = eval('self.'+var_name)
            if isinstance(obj, (QPushButton, QComboBox)) and var_name not in ['tab_metadata_default_cover_preview']:
                obj.setCursor(cursor)
            if isinstance(obj, QWidget):
                obj.setStyleSheet(env_vars['styles'][style]['QTabWidget'])
        self.test_archiver()

        self.button_box.button(QDialogButtonBox.Ok).setStyleSheet(env_vars['styles'][style]['fullAltButton'])
        self.button_box.button(QDialogButtonBox.Ok).setCursor(cursor)
        self.button_box.button(QDialogButtonBox.Cancel).setStyleSheet(env_vars['styles'][style]['fullAltButton'])
        self.button_box.button(QDialogButtonBox.Cancel).setCursor(cursor)

        self.tab_global.setStyleSheet(env_vars['styles'][style]['QDialog'])
        self.tab_metadata.setStyleSheet(env_vars['styles'][style]['QDialog'])
        self.tab_conversion.setStyleSheet(env_vars['styles'][style]['QDialog'])
        self.tab_about.setStyleSheet(env_vars['styles'][style]['QDialog'])

        self.tab_metadata_import_filename_separator_line_edit.setStyleSheet(env_vars['styles'][style]['QLineEditPrecise'])

        # IN DEV DISABLED CONTENT
        cursor_disabled = QtGui.QCursor(QtCore.Qt.ForbiddenCursor)
        # self.tab_global_lang_btn.setDisabled(True)
        # self.tab_global_style_import_btn.setDisabled(True)
        self.tab_global_lang_btn.setCursor(cursor_disabled)
        self.tab_global_style_import_btn.setCursor(cursor_disabled)
        self.tab_global_lang_btn.setToolTip(self.lng['NotImplemented'])
        self.tab_global_style_import_btn.setToolTip(self.lng['NotImplemented'])

    def cover_combo_changed(self):
        vals = {
            'background': '',
            'pattern': '',
            'pattern_color': '',
            'title': '',
            'series': '',
            'authors': ''
        }
        style = self.BDD.get_param('style')
        for selector in self.color_selectors:
            selector_type = selector.replace('tab_metadata_default_cover_', '').replace('_combo_box', '')
            combo = eval('self.'+selector)
            index = combo.currentIndex()
            color = combo.itemData(index, 99)
            vals[selector_type] = color
            combo.setStyleSheet(
                "QComboBox:!editable {{ color: {}; }}".format(color) + env_vars['styles'][self.app_style]['QComboBoxArrow']
            )

        vals['pattern'] = self.tab_metadata_default_cover_pattern_combo_box.currentData(99)
        cover = common.books.create_cover("TITRE", "auteur", "La série", 2, style=vals)
        icon = PyQt5.QtGui.QIcon()
        icon.addPixmap(PyQt5.QtGui.QPixmap(cover, "png"))
        self.tab_metadata_default_cover_preview.setIcon(icon)

        isize = icon.actualSize(PyQt5.QtCore.QSize(500, 500))
        image = PyQt5.QtGui.QImage(icon.pixmap(isize.width(), isize.height()).toImage())
        byte_array = PyQt5.QtCore.QByteArray()
        buffer = PyQt5.QtCore.QBuffer(byte_array)
        image.save(buffer, "PNG")
        icon_base64 = byte_array.toBase64().data()

        self.tab_metadata_default_cover_preview.setToolTip(
            '<img src="data:image/png;base64,{}" width="500"/>'.format(icon_base64.decode('UTF-8'))
        )

    def test_archiver(self):
        style = self.BDD.get_param('style')
        path = self.tab_global_archiver_folder_line_edit.text()
        ret = False
        if os.path.isdir(path) is True:
            path += os.sep + env_vars['tools']['archiver'][os.name]['exe']
            if os.path.isfile(path) is True:
                ret = True
        if ret is False:
            self.tab_global_archiver_folder_line_edit.setStyleSheet(env_vars['styles'][style]['QLineEditBad'])
        else:
            self.tab_global_archiver_folder_line_edit.setStyleSheet(env_vars['styles'][style]['QLineEditGood'])
        return ret

    def change_archiver_folder(self):
        print("test")
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        options |= QFileDialog.Directory

        dlg = QFileDialog()
        dlg.setOptions(options)
        dlg.setFileMode(QFileDialog.Directory)

        preset = self.BDD.get_param("library_directory").replace('{APP_DIR}', app_directory)
        folder = dlg.getExistingDirectory(self, "Choose Directory", preset).replace(app_directory, '{APP_DIR}')
        print(folder)
        self.tab_global_library_folder_line_edit.setText(folder)