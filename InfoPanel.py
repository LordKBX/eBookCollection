import os, sys, re
import base64
import traceback
import urllib.parse
import PyQt5.QtCore
import PyQt5.QtGui
import PyQt5.QtWidgets

from common.common import *
from common.vars import *
from common.dialog import *


class HomeWindowInfoPanel:
    current_book = None
    info_panel_current_link = None
    info_panel_link_last_sender = None
    info_panel_current_nb_files = None
    info_panel_link_context_menu_open = False
    info_panel_initialized = False

    def init_info_panel(self):
        self.info_block_file_formats_value.setOpenExternalLinks(True)
        self.info_block_file_formats_value.setContextMenuPolicy(PyQt5.QtCore.Qt.CustomContextMenu)
        self.info_block_file_formats_value.linkHovered.connect(self.info_panel_link_hover)
        self.info_block_file_formats_value.customContextMenuRequested.connect(self.info_panel_link_context_menu)
        self.info_panel_initialized = True

    def set_info_panel(self, book: dict = None):
        """
        Insert into the info pannel the details values of the book

        :param book: dict of the spécified book
        :return: void
        """
        if self.info_panel_initialized is False:
            self.init_info_panel()
        # print(book)
        passed = True
        if book is None: 
            passed = False
        else:
            if not is_in(book, ['title', 'series', 'authors', 'files']):
                passed = False

        if passed is True:
            try:
                boldind_list = [
                    self.info_block_title_label,
                    self.info_block_serie_label,
                    self.info_block_authors_label,
                    self.info_block_file_formats_label,
                    self.info_block_size_label
                ]
                for elm in boldind_list:
                    elm.setProperty('bold', True)
                    elm.style().unpolish(elm)
                    elm.style().polish(elm)

                self.current_book = book['guid']
                self.info_block_title_value.setText(book['title'])
                self.info_block_serie_value.setText(book['series'])
                self.info_block_authors_value.setText(book['authors'])

                # info_block_synopsis
                self.metadata_window_clear_layout(self.info_block_synopsis.layout())
                la0 = QtWidgets.QLabel('Synopsis')
                la0.setProperty('bold', True)
                self.info_block_synopsis.layout().addWidget(la0)

                spacer1 = QtWidgets.QSpacerItem(10, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
                self.info_block_synopsis.layout().addItem(spacer1)

                la1 = QtWidgets.QLabel(book['synopsis'])
                la1.setWordWrap(True)
                self.info_block_synopsis.layout().addWidget(la1)

                formats = ''
                sizes = ''
                self.info_panel_current_nb_files = len(book['files'])
                for file in book['files']:
                    if formats != '':
                        formats += ' / '
                        sizes += ' / '
                    link = file['link']
                    if re.search("^data/", link):
                        link = 'file:///' + self.app_directory.replace(os.sep, '/') + '/' + link
                        # link = self.app_directory.replace(os.sep, '/') + '/' + link
                    # elif re.search("^(http|https)://", link): {}
                    else:
                        link = 'file:///' + link.replace(os.sep, '/')
                    link = link.replace(' ', '%20')
                    formats += '<a href="' + link + '" style="color: rgb(255, 255, 255);">' + file['format'] + '</a>'
                    sizes += file['size']

                self.info_block_file_formats_value.setProperty('book_id', self.current_book)
                self.info_block_file_formats_value.setText(formats)

                self.info_block_size_value.setText(sizes)
            except Exception:
                traceback.print_exc()
            try:
                icon = PyQt5.QtGui.QIcon()
                tbimg = book['cover'].split(',')
                by = PyQt5.QtCore.QByteArray()
                by.fromBase64(tbimg[1].encode('utf-8'))
                image = PyQt5.QtGui.QPixmap()
                image.loadFromData(base64.b64decode(tbimg[1]))
                """
                if tbimg[0] == 'data:image/jpeg;base64':
                    image.loadFromData(by, "JPG")
                if tbimg[0] == 'data:image/png;base64':
                    image.loadFromData(by, "PNG")
                """
                icon.addPixmap(image, PyQt5.QtGui.QIcon.Normal, PyQt5.QtGui.QIcon.Off)
                self.info_block_cover.setIcon(icon)
                self.info_block_cover.setIconSize(PyQt5.QtCore.QSize(160, 160))
                self.info_block_cover.setToolTip("<img src='{}'/>".format(book['cover']))
            except Exception:
                traceback.print_exc()
                icon = PyQt5.QtGui.QIcon()
                icon.addPixmap(PyQt5.QtGui.QPixmap(self.app_directory + '/ressources/icons/white/book.png'), PyQt5.QtGui.QIcon.Normal, PyQt5.QtGui.QIcon.Off)
                self.info_block_cover.setIcon(icon)
                self.info_block_cover.setIconSize(PyQt5.QtCore.QSize(130, 130))
        else:
            self.info_block_title_value.setText("")
            self.info_block_serie_value.setText("")
            self.info_block_authors_value.setText("")
            self.info_block_file_formats_value.setText("")
            self.info_block_size_value.setText("")

            icon = PyQt5.QtGui.QIcon()
            icon.addPixmap(PyQt5.QtGui.QPixmap(self.app_directory+'/icons/white/book.png'), PyQt5.QtGui.QIcon.Normal, PyQt5.QtGui.QIcon.Off)
            self.info_block_cover.setIcon(icon)
            self.info_block_cover.setIconSize(PyQt5.QtCore.QSize(130, 130))

    def info_panel_link_hover(self, link: str):
        if link is None or link.strip() == '':
            return
        self.info_panel_current_link = urllib.parse.unquote(link).replace('/', os.sep)

    def info_panel_link_context_menu(self):
        if self.info_panel_link_context_menu_open is True:
            return
        self.info_panel_link_context_menu_open = True
        try:
            if self.info_panel_current_link is None or self.info_panel_current_link.strip() == '':
                return

            menu = PyQt5.QtWidgets.QMenu(self.info_block_file_formats_value)

            action0 = PyQt5.QtWidgets.QAction(self.lang['Library/InfoBlockLinkContestMenu/open'], None)
            action0.triggered.connect(self.info_panel_link_open)
            menu.addAction(action0)

            if self.info_panel_current_link.lower().endswith(('.epub', '.epub2', '.epub3')):
                action1 = PyQt5.QtWidgets.QAction(self.lang['Library/InfoBlockLinkContestMenu/edit'], None)
                action1.triggered.connect(self.info_panel_link_edit)
                menu.addAction(action1)

            if self.info_panel_current_nb_files > 1:
                action2 = PyQt5.QtWidgets.QAction(self.lang['Library/InfoBlockLinkContestMenu/delete'], None)
                action2.triggered.connect(self.info_panel_link_delete_file)
                menu.addAction(action2)
            else:
                action2 = PyQt5.QtWidgets.QAction(self.lang['Library/InfoBlockLinkContestMenu/deleteBook'], None)
                action2.triggered.connect(self.info_panel_link_delete_book)
                menu.addAction(action2)

            ext = self.info_panel_current_link[self.info_panel_current_link.rindex('.')+1:].upper()
            print('ext=', ext)
            plugs = common.vars.get_plugins('library', 'contextMenu', None, ext)
            for plug in plugs:
                lg = self.lang.test_lang()
                tx = None
                for label in plug['interface']['label']:
                    if label['lang'] == self.lang.default_language and tx is None:
                        tx = label['content']
                    if label['lang'] == lg:
                        tx = label['content']
                action3 = PyQt5.QtWidgets.QAction(tx, None)
                action3.setProperty('plugin', plug['name'])
                action3.setProperty('book_id', self.current_book)
                tt = [plug['archetype']]
                try:
                    tt = plug['archetype'].split(':')
                except Exception:
                    pass
                action3.setProperty('archetype', tt[0])
                if tt[0] == 'conversion':
                    tt2 = ['.', 'conv']
                    try:
                        tt2 = tt[1].split('-')
                        action3.setProperty('end_format', tt2[1])
                    except Exception:
                        action3.setProperty('end_format', 'CONV')
                    pf = self.info_panel_current_link.replace('/', os.sep)
                    rp = pf.rindex('.')
                    action3.setProperty('args', {
                        'input': pf,
                        'output': os.path.dirname(os.path.realpath(pf)),
                        'output2': pf[:rp]
                    })
                else:
                    action3.setProperty('args', {})
                # plugin_exec(executor_dir, {'input': executor_file, 'output': executor_file2})
                action3.triggered.connect(self.context_menu_plugin_exec)
                menu.addAction(action3)

            menu.exec_(PyQt5.QtGui.QCursor.pos())
        except Exception:
            traceback.print_exc()
        self.info_panel_link_context_menu_open = False

    def info_panel_link_open(self):
        cmd = '"'+self.info_panel_current_link+'"'
        print(cmd)
        os.system(cmd)

    def info_panel_link_edit(self):
        args = list()
        exe = app_directory + '/editor.exe'.replace('/', os.sep)
        if os.path.isfile(exe):
            args.append(app_directory + '/editor.exe'.replace('/', os.sep))
            args.append(self.info_panel_current_link)
            args.append('debug')
        else:
            args.append('python')
            args.append(app_directory + '/editor/editor.py'.replace('/', os.sep))
            args.append(self.info_panel_current_link)
            args.append('debug')
        try:
            return_code = subprocess.call(args, shell=True)
        except Exception:
            traceback.print_exc()

    def info_panel_link_delete_file(self):
        ret = WarnDialogConfirm(
            self.lang['Library']['DialogConfirmDeleteBookWindowTitle2'],
            self.lang['Library']['DialogConfirmDeleteBookWindowText2'],
            self.lang['Library']['DialogConfirmDeleteBookBtnYes'],
            self.lang['Library']['DialogConfirmDeleteBookBtnNo'],
            self
        )

        if ret is True:
            self.BDD.delete_book(None, self.info_panel_current_link)
            self.set_info_panel(self.BDD.get_books(self.current_book)[0])

    def info_panel_link_delete_book(self):
        ret = WarnDialogConfirm(
            self.lang['Library']['DialogConfirmDeleteBookWindowTitle'],
            self.lang['Library']['DialogConfirmDeleteBookWindowText'],
            self.lang['Library']['DialogConfirmDeleteBookBtnYes'],
            self.lang['Library']['DialogConfirmDeleteBookBtnNo'],
            self
        )

        if ret is True:
            self.BDD.delete_book(self.current_book)
            self.load_books(self.BDD.get_books())

