# This Python file uses the following encoding: utf-8
import os, sys, traceback
from PyQt5.QtWidgets import *
import PyQt5.sip
import PyQt5.QtCore
import PyQt5.QtGui
import PyQt5.uic
from PyQt5.uic import *
import zipfile
import jsonschema

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
import common.common
import common.files
import common.books
import common.dialog
import common.archive
from common.vars import *


class SettingsWindow(QDialog):
    verticalSpacer = None

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

        if debug is False:
            self.dialog_tabs.setCurrentIndex(0)

        #GLOBAL tab
        self.tab_global_lang_combo_box.currentIndexChanged.connect(self.change_language)
        self.tab_global_style_combo_box.currentIndexChanged.connect(self.change_style)

        self.tab_global_lang_btn.clicked.connect(self.import_lang)
        self.tab_global_style_import_btn.clicked.connect(self.import_style)

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

        self.tab_plugins_import.clicked.connect(self.install_plugin)

        self.tab_about_btn_license.clicked.connect(lambda: os.system("start " + app_directory + os.sep + 'LICENSE.txt'))
        self.tab_about_btn_website.clicked.connect(lambda: os.system("start https://github.com/LordKBX/eBookCollection"))

        # tab sync
        sync_ip = self.BDD.get_param('sync/ip')
        sync_port = self.BDD.get_param('sync/port')
        sync_protocol = self.BDD.get_param('sync/protocol')
        sync_user = self.BDD.get_param('sync/user')
        sync_password = self.BDD.get_param('sync/password')

        print('sync_ip = "{}"'.format(sync_ip))
        print('sync_port = "{}"'.format(sync_port))
        print('sync_protocol = "{}"'.format(sync_protocol))
        print('sync_user = "{}"'.format(sync_user))
        print('sync_password = "{}"'.format(sync_password))

        self.tab_sync_interface_ip_edit.setText('{}'.format(sync_ip))
        self.tab_sync_interface_port_edit.setText('{}'.format(sync_port))
        self.tab_sync_interface_protocol_combobox.setCurrentIndex(self.BDD.sync_protocols.index(sync_protocol))
        self.tab_sync_identification_user_edit.setText('{}'.format(sync_user))
        self.tab_sync_identification_password_edit.setText('{}'.format(sync_password))

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

            if self.test_archiver() is True:
                self.BDD.set_param('archiver_dir', self.tab_global_archiver_folder_line_edit.text())

            self.BDD.set_param('sync/ip', self.tab_sync_interface_ip_edit.text())
            self.BDD.set_param('sync/port', self.tab_sync_interface_port_edit.text())
            self.BDD.set_param('sync/protocol', self.tab_sync_interface_protocol_combobox.currentText())
            self.BDD.set_param('sync/user', self.tab_sync_identification_user_edit.text())
            self.BDD.set_param('sync/password', self.tab_sync_identification_password_edit.text())

            return 'ok'
        else:
            self.lng.set_lang(self.app_lang)
            self.BDD.set_param('lang', self.app_lang)
            self.BDD.set_param('style', self.app_style)
            return None

    def import_lang(self):
        dest_dir = app_user_directory + os.sep + "imports" + os.sep + "langs"
        try:
            options = QFileDialog.Options()
            # options |= QFileDialog.DontUseNativeDialog
            list_files, _ = QFileDialog.getOpenFileNames(
                self, self.lng['Settings/LanguageImportTitle'], app_directory,
                "eBook Collection language file (*.ebclang)",
                options=options
            )
            print(list_files)
            for file in list_files:
                myzip = zipfile.ZipFile(file, 'r')
                myfile = myzip.open('mimetype')
                mimetype = myfile.read().decode('utf8')
                myfile.close()
                if mimetype == 'application/ebook+collection+lang':
                    file_list = myzip.namelist()
                    for fi in file_list:
                        if fi.endswith('.json') is True:
                            myfile = myzip.open(fi)
                            data = myfile.read().decode('utf8')
                            myfile.close()
                            try: os.makedirs(dest_dir)
                            except Exception: pass
                            fd = open(dest_dir + os.sep + fi, 'w', encoding='utf8')
                            fd.write(data)
                            fd.close()
                            break
            self.lng.refresh()
            self.load_languages(self.lng.language)
        except Exception:
            traceback.print_exc()

    def import_style(self):
        dest_dir = app_user_directory + os.sep + "imports" + os.sep + "styles"
        try:
            options = QFileDialog.Options()
            # options |= QFileDialog.DontUseNativeDialog
            list_files, _ = QFileDialog.getOpenFileNames(
                self, self.lng['Settings/StyleImportTitle'], app_directory,
                "eBook Collection language file (*.ebcstyle)",
                options=options
            )
            style = ''
            for file in list_files:
                myzip = zipfile.ZipFile(file, 'r')
                myfile = myzip.open('mimetype')
                mimetype = myfile.read().decode('utf8')
                myfile.close()
                if mimetype == 'application/ebook+collection+style':
                    file_list = myzip.namelist()
                    for fi in file_list:
                        if fi.endswith('.json') is True:
                            style = fi.replace('.json', '')
                            myfile = myzip.open(fi)
                            data = myfile.read().decode('utf8')
                            myfile.close()
                            try: os.makedirs(dest_dir)
                            except Exception: pass
                            fd = open(dest_dir + os.sep + fi, 'w', encoding='utf8')
                            fd.write(data)
                            fd.close()
                            break
            load_styles()
            self.tab_global_style_combo_box.addItem(style)
            self.tab_global_style_combo_box.setItemData(self.tab_global_style_combo_box.count() - 1, style, 99)
        except Exception:
            traceback.print_exc()

    def change_library_folder(self):
        print("test")
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        options |= QFileDialog.Directory

        dlg = QFileDialog()
        dlg.setOptions(options)
        dlg.setFileMode(QFileDialog.Directory)

        preset = self.BDD.get_param("library_directory")
        folder = dlg.getExistingDirectory(self, "Choose Directory", preset)
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
        try:
            load_styles()
            if selected_style is None:
                selected_style = self.BDD.get_param('style')
            while self.tab_global_style_combo_box.count() > 0:
                self.tab_global_style_combo_box.removeItem(0)
            i = 0
            sel = 0
            for style in get_styles():
                st = style
                if self.lng['Settings/Style'+style] is not None:
                    st = self.lng['Settings/Style'+style]
                self.tab_global_style_combo_box.addItem(st)
                self.tab_global_style_combo_box.setItemData(self.tab_global_style_combo_box.count() - 1, style, 99)
                if selected_style == style:
                    sel = i
                i += 1
            self.tab_global_style_combo_box.setCurrentIndex(sel)
        except Exception:
            traceback.print_exc()

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
            self.dialog_tabs.setTabText(2, self.lng['Settings/TabSyncTitle'])
            self.dialog_tabs.setTabText(3, self.lng['Settings/TabPluginsTitle'])
            self.dialog_tabs.setTabText(4, self.lng['Settings/TabAboutTitle'])

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
                st = data
                if self.lng["Settings/Style" + data] is not None:
                    st = self.lng["Settings/Style" + data]
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

            # tab_plugins
            self.tab_plugins_import.setText(self.lng['Settings/Import'])

            # tab_about
            #   About group
            self.tab_about_btn_license.setText(self.lng['Settings/AboutBtnLicense'])
            self.tab_about_btn_website.setText(self.lng['Settings/AboutBtnWebsite'])
            self.tab_about_label.setText(self.lng['Settings/AboutLabel'])

            # tab sync
            self.tab_sync_interface_group.setTitle(self.lng['Settings/SyncInterfaceGroupTitle'])
            self.tab_sync_interface_ip_label.setText(self.lng['Settings/SyncInterfaceIP'])
            self.tab_sync_interface_port_label.setText(self.lng['Settings/SyncInterfacePort'])
            self.tab_sync_interface_protocol_label.setText(self.lng['Settings/SyncInterfaceProtocol'])

            self.tab_sync_identification.setTitle(self.lng['Settings/SyncIdentificationGroupTitle'])
            self.tab_sync_identification_user_label.setText(self.lng['Settings/SyncIdentificationUser'])
            self.tab_sync_identification_password_label.setText(self.lng['Settings/SyncIdentificationPassword'])

            self.load_plugins_tab()
        except Exception:
            traceback.print_exc()

    def apply_style(self, style: str = None):
        if style is None:
            style = self.BDD.get_param('style')
        cursor = QtGui.QCursor(QtCore.Qt.PointingHandCursor)
        self.setStyleSheet(get_style_var(style, 'QDialog') + get_style_var(style, 'SettingsDialogBox'))

        cls = self.__dir__()
        for var_name in cls:
            obj = eval('self.'+var_name)
            if isinstance(obj, (QPushButton, QComboBox)) and var_name not in ['tab_metadata_default_cover_preview']:
                obj.setCursor(cursor)
            if isinstance(obj, QWidget):
                obj.setStyleSheet(get_style_var(style, 'QTabWidgetVertical'))
        self.test_archiver()

        self.button_box.button(QDialogButtonBox.Ok).setStyleSheet(get_style_var(style, 'fullAltButton'))
        self.button_box.button(QDialogButtonBox.Ok).setCursor(cursor)
        self.button_box.button(QDialogButtonBox.Cancel).setStyleSheet(get_style_var(style, 'fullAltButton'))
        self.button_box.button(QDialogButtonBox.Cancel).setCursor(cursor)

        self.tab_global.setStyleSheet(get_style_var(style, 'QDialog'))
        self.tab_metadata.setStyleSheet(get_style_var(style, 'QDialog'))
        self.tab_plugins.setStyleSheet(get_style_var(style, 'QDialog'))
        self.tab_about.setStyleSheet(get_style_var(style, 'QDialog'))

        self.tab_metadata_import_filename_separator_line_edit.setStyleSheet(get_style_var(style, 'SettingsQLineEditPrecise'))
        self.cover_combo_changed()

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
                "QComboBox:!editable {{ color: {}; }}".format(color) + get_style_var(self.app_style, 'SettingsQComboBoxArrow')
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
            self.tab_global_archiver_folder_line_edit.setStyleSheet(get_style_var(style, 'SettingsQLineEditBad'))
        else:
            self.tab_global_archiver_folder_line_edit.setStyleSheet(get_style_var(style, 'SettingsQLineEditGood'))
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
        folder = dlg.getExistingDirectory(self, "Choose Directory", preset)
        print(folder)
        self.tab_global_archiver_folder_line_edit.setText(folder)
        self.test_archiver()

    def load_plugins_tab(self):
        try:
            style = self.BDD.get_param('style')
            cursor = QtGui.QCursor(QtCore.Qt.PointingHandCursor)
            plugs = list_plugins()

            self.clear_layout(self.tab_plugins_list_zone)
            self.tab_plugins_scroll_area1.repaint()

            for plug in plugs:
                # plugin = plugs[plug]
                print(plug)
                box = QGroupBox()
                box.setTitle(plug)
                box.setLayout(QVBoxLayout())

                lines = []
                line_style = ""
                if plugs[plug]['context']['app'] == 'library':
                    line_style = "background-color:#66ff66;color:#000000;"
                elif plugs[plug]['context']['app'] == 'reader':
                    line_style = "background-color:#ff6666;color:#ffffff;"
                elif plugs[plug]['context']['app'] == 'editor':
                    line_style = "background-color:#6666ff;color:#ffffff;"
                lines.append(
                    self.lng['Settings/pluginsForApp']
                        .format('<span style="'+line_style+'">&nbsp;'+plugs[plug]['context']['app']+' </span>')
                )
                arct = [plugs[plug]['context']['archetype']]
                try: arct = plugs[plug]['context']['archetype'].split(':')
                except Exception: pass
                line_style = "background-color:#00AEFF;color:#000000;"
                lines.append(self.lng['Settings/pluginsArchetype'].format('<span style="'+line_style+'">&nbsp;'+arct[0]+' </span>'))

                for line in lines:
                    l1 = QHBoxLayout()
                    la1 = QLabel(line)
                    la1.setMinimumHeight(25)
                    l1.addWidget(la1)
                    l1.addStretch(1)
                    box.layout().addLayout(l1)

                l2 = QHBoxLayout()
                pb1 = QPushButton()
                pb1.setText(self.lng['Settings/pluginsUninstallButton'])
                pb1.setCursor(cursor)
                pb1.setMinimumHeight(25)
                # pb1.setStyleSheet(get_style_var(style, 'fullButton'))
                pb1.setProperty('plugin', plug)
                pb1.clicked.connect(self.uninstall_plugin)
                l2.addWidget(pb1)
                pb2 = QPushButton()
                pb2.setText(self.lng['Settings/pluginsSettingsButton'])
                pb2.setCursor(cursor)
                pb2.setMinimumHeight(25)
                # pb2.setStyleSheet(get_style_var(style, 'fullButton'))
                pb2.setProperty('plugin', plug)
                pb2.clicked.connect(self.plugin_settings_open)
                l2.addWidget(pb2)
                # l2.addStretch(1)
                box.layout().addLayout(l2)

                self.tab_plugins_list_zone.addWidget(box)
            # self.tab_plugins_list_zone.addItem(QSpacerItem(10, 99999999, QSizePolicy.Maximum, QSizePolicy.Maximum))
        except Exception:
            traceback.print_exc()

    def install_plugin(self):
        print('install a plugin')
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        list_files, _ = QFileDialog.getOpenFileNames(
            self, self.lng['Settings/StyleImportTitle'], app_directory,
            "eBook Collection plug-in file (*.ebcplugin)",
            options=options
        )
        style = ''
        try:
            for file in list_files:
                file = file.replace('/', os.sep)
                file_name = file[file.rindex(os.sep)+1:].replace('.ebcplugin', '')
                myzip = zipfile.ZipFile(file, 'r')
                myfile = myzip.open('mimetype')
                mimetype = myfile.read().decode('utf8')
                myfile.close()
                if mimetype != 'application/ebook+collection+plugin':
                    common.dialog.WarnDialog(self.lng['Settings/ImportErrorTitle'], self.lng['Settings/ImportErrorFileType'])
                    return

                myfile = myzip.open('package.json')
                package = myfile.read().decode('utf8')
                myfile.close()

                # test id valid JSON
                decoder = json.decoder.JSONDecoder()
                tab = decoder.decode(package)
                # test package JSON schema
                jsonschema.validate(instance=tab, schema=plugin_package_schema)

                dest_dir = app_user_directory + os.sep + "imports" + os.sep + "plugins" + os.sep + file_name
                common.archive.inflate(file, dest_dir)

            load_plugins()
            self.load_plugins_tab()
        except Exception:
            traceback.print_exc()
            common.dialog.WarnDialog(self.lng['Settings/ImportErrorTitle'], self.lng['Settings/ImportErrorFileCorrupted'])

    def uninstall_plugin(self):
        try:
            plugin_name = self.sender().property('plugin')
            print('uninstall', plugin_name)
            dest_dir = app_user_directory + os.sep + "imports" + os.sep + "plugins" + os.sep + plugin_name
            if os.path.isdir(dest_dir) is True:
                ret = common.dialog.WarnDialogConfirm(
                        self.lng['Settings/DialogConfirmDeletePluginWindowTitle'],
                        self.lng['Settings/DialogConfirmDeletePluginWindowText'],
                        self.lng['Settings/DialogConfirmDeletePluginBtnYes'],
                        self.lng['Settings/DialogConfirmDeletePluginBtnNo'],
                        self
                    )
                if ret is True:
                    common.files.rmDir(dest_dir)
                    load_plugins()
                    self.load_plugins_tab()
        except Exception:
            traceback.print_exc()

    def plugin_settings_open(self):
        try:
            plugin_name = self.sender().property('plugin')
            print('plugin_settings_open', plugin_name)
            plug = get_plugin(plugin_name)
            if plug is not None:
                settings = plug['settings']
                print(settings)
                ui = QDialog(self, QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
                style = self.BDD.get_param('style')
                PyQt5.uic.loadUi(
                    os.path.dirname(os.path.realpath(__file__)) + os.sep + 'settings_plugin_params.ui'.replace('/', os.sep),
                    ui
                )

                cursor = QtGui.QCursor(QtCore.Qt.PointingHandCursor)
                ui.setStyleSheet(get_style_var(style, 'QDialog') + get_style_var(style, 'SettingsDialogBox'))
                ui.button_box.button(QDialogButtonBox.Ok).setStyleSheet(get_style_var(style, 'fullAltButton'))
                ui.button_box.button(QDialogButtonBox.Ok).setCursor(cursor)
                ui.button_box.button(QDialogButtonBox.Cancel).setStyleSheet(get_style_var(style, 'fullAltButton'))
                ui.button_box.button(QDialogButtonBox.Cancel).setCursor(cursor)
                ui.button_box.button(QDialogButtonBox.Ok).setText(self.lng.get('Generic/DialogBtnSave'))
                ui.button_box.button(QDialogButtonBox.Cancel).setText(self.lng.get('Generic/DialogBtnCancel'))

                ui.setWindowTitle(self.lng['Settings/pluginsSettingsTitle'].format(plugin_name))

                if ui.scrollArea.layout() is not None:
                    ui.scrollArea.widget().deleteLater()
                if ui.scrollArea.layout() is None:
                    ui.scrollArea.setLayout(QVBoxLayout())

                ui_params = {}
                language = self.lng.test_lang()

                for param in settings:
                    block = QVBoxLayout()
                    l1 = QHBoxLayout()
                    lab = param['name']
                    for tx in param['label']:
                        if tx['lang'] == language:
                            lab = tx['content']

                    la1 = QLabel(lab)
                    l1.addWidget(la1)
                    if param['archetype'] == 'int' or param['archetype'] == 'float':
                        if param['archetype'] == 'int': ui_params[param['name']] = QSpinBox()
                        else: ui_params[param['name']] = QDoubleSpinBox()

                        if 'min' in param: ui_params[param['name']].setMinimum(param['min'])
                        else: ui_params[param['name']].setMinimum(0)

                        if 'max' in param: ui_params[param['name']].setMaximum(param['max'])
                        else: ui_params[param['name']].setMaximum(2147483647)

                        if param['archetype'] == 'int': ui_params[param['name']].setValue(int(float(param['value'])))
                        else: ui_params[param['name']].setValue(float(param['value']))

                        l1.addWidget(ui_params[param['name']])
                    else:
                        ui_params[param['name']] = QLineEdit()
                        ui_params[param['name']].setText(param['value'])
                        l1.addWidget(ui_params[param['name']])

                    ui.scrollArea.layout().addLayout(l1)
                ui.scrollArea.layout().addStretch(1)

                ret = ui.exec_()
                print(ret)
                if ret == 1:
                    settings = QtCore.QSettings(app_editor, app_name)
                    for param in ui_params:
                        value = ''
                        if isinstance(ui_params[param], QLineEdit):
                            value = ui_params[param].text()
                        elif isinstance(ui_params[param], QSpinBox):
                            value = ui_params[param].value()
                        elif isinstance(ui_params[param], QDoubleSpinBox):
                            value = ui_params[param].value()
                        settings.setValue('plugins/' + plugin_name + '/' + param, value)
                        print(param, '=', value)


        except Exception:
            traceback.print_exc()

    def clear_layout(self, layout: QLayout):
        if layout is None:
            return
        r = []
        i = layout.count()
        while i > 0:
            i -= 1
            r.append(i)

        for i in r:
            child = layout.itemAt(i)
            print(child)
            if isinstance(child, QWidgetItem):
                try:
                    child.widget().deleteLater()
                except Exception:
                    traceback.print_exc()
            elif isinstance(child, QLayoutItem):
                layout.removeItem(child)
            del child

