from checkpoint import *
from files import *
from content_table_editor import *

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from common.dialog import *
from common.books import *
from common.files import *
from common.archive import *
from common.vars import *
import common.qt
import common.dialog


class EditorWindow(QtWidgets.QMainWindow):
    default_page = ''
    ebook_info = None

    def __init__(self, parent: QtWidgets.QMainWindow, opened_file, lang, bdd):
        super(EditorWindow, self).__init__(parent)
        PyQt5.uic.loadUi(os.path.dirname(os.path.realpath(__file__)) + os.sep + 'editor.ui'.replace('/', os.sep), self)
        self.opened_file = opened_file
        self.tmpDir = app_user_directory + os.sep + 'editor' + os.sep + 'tmp'
        self.lang = lang
        self.BDD = bdd
        self.app_style = self.BDD.get_param('style')
        self.apply_translation()
        self.apply_style()

        # ui.tabWidget
        ad = app_directory.replace(os.sep, '/')
        self.tabWidget.clear()
        self.tabWidget.setStyleSheet(
            """
            QFrame {  background: rgb(50, 50, 50); }
            QTabWidget::pane { }
            QTabWidget::tab-bar { }
            QTabBar::tab {
                background: rgb(80, 80, 80) !important;
                color: white; padding: 5px;
                margin-right:2px; border-color:rgb(0,0,0); border-width:1px; border-style:solid;
            }
            QTabBar::tab:selected { background: rgb(0, 135, 202) !important; }
            QTabBar::close-button {  border-image: none; image: url('""" + ad + """/icons/white/close.png'); }
            QTabBar::close-button:hover {  border-image: none; image: url('""" + ad + """/icons/black/close.png'); }
            """
        )
        self.tabWidget.set_preview_webview(self.webView, self.default_page)
        self.tabWidget.tabCloseRequested.connect(self.on_close_tab)
        self.tabWidget.currentChanged.connect(self.on_change_tab)

        # Processing File Table
        self.treeFileTable.clear()
        self.treeFileTable.itemDoubleClicked.connect(self.file_table_item_double_clicked)
        self.treeFileTable.setIndentation(10)
        self.treeFileTable.setCursor(QtCore.Qt.PointingHandCursor)
        self.treeFileTable.setStyleSheet(env_vars['styles'][self.app_style]['fullTreeView'])

        # Processing Content Table
        self.treeContentTable.clear()
        self.treeContentTable.currentItemChanged.connect(self.content_table_current_item_changed)
        self.treeContentTable.itemDoubleClicked.connect(self.file_table_item_double_clicked)
        self.treeContentTable.setIndentation(0)
        self.treeContentTable.setCursor(QtCore.Qt.PointingHandCursor)

        # Toolbar buttons
        self.button_save.clicked.connect(self.save_ebook)
        self.button_load_checkpoint.clicked.connect(self.load_check_point)
        self.button_create_checkpoint.clicked.connect(self.create_check_point)
        self.button_file_manager.clicked.connect(self.load_file_managment)
        self.button_edit_content_table.clicked.connect(self.load_content_table_managment)

        self.webView.setHtml(self.default_page)

        filepath, ext = os.path.splitext(self.opened_file)
        mappdir = app_directory.replace(os.sep, '/') + '/data/'
        self.setWindowTitle(
            self.lang['Editor']['WindowTitle'] + ' - ' + self.opened_file.replace(os.sep, '/')
            .replace(mappdir, '').replace('/', ' / ').replace(ext, '')
        )
        # EditorWindow.show()
        try:
            rmDir(self.tmpDir)
        except Exception:
            ""
        if os.path.isdir(self.tmpDir) is not True:
            os.makedirs(self.tmpDir + os.sep + 'original')
            os.makedirs(self.tmpDir + os.sep + 'current')

        if ext in ['.epub', '.epub2', '.epub3']:
            self.ebook_info = get_epub_info(self.opened_file)
            ret = inflate(self.opened_file, self.tmpDir + os.sep + 'original')
            ret = inflate(self.opened_file, self.tmpDir + os.sep + 'current')

        elif ext in ['.cbz', '.cbr']:
            ret = inflate(self.opened_file, self.tmpDir + os.sep + 'original')
            ret = inflate(self.opened_file, self.tmpDir + os.sep + 'current')
        else:
            WarnDialog(
                self.lang['Editor']['DialogInfoBadFileWindowTitle'],
                self.lang['Editor']['DialogInfoBadFileWindowText'], self)
            exit(0)

        self.file_table_load()
        self.load_content_table()

    def apply_translation(self):
        self.default_page = "".join(self.lang['Editor']['WebViewDefaultPageContent'])

        # Blocks title
        self.dockTop.setWindowTitle(self.lang['Editor/BlockToolbar/Header'])
        self.dockFiles.setWindowTitle(self.lang['Editor/BlockFileListHeader'])
        self.dockContentTable.setWindowTitle(self.lang['Editor/BlockContentTableHeader'])
        self.dockPreview.setWindowTitle(self.lang['Editor/BlockPreviewHeader'])

        # Toolbar buttons
        self.button_save.setText(self.lang['Editor/BlockToolbar/Save'])
        self.button_load_checkpoint.setText(self.lang['Editor/BlockToolbar/CheckPointLoad'])
        self.button_create_checkpoint.setText(self.lang['Editor/BlockToolbar/CheckPointCreate'])
        self.button_file_manager.setText(self.lang['Editor/BlockToolbar/FileManager'])
        self.button_edit_content_table.setText(self.lang['Editor/BlockToolbar/EditContentTable'])

    def apply_style(self):
        self.setStyleSheet(env_vars['styles'][self.app_style]['QMainWindow'])
        self.dockTopContents.setStyleSheet(env_vars['styles'][self.app_style]['QMainWindow'])

        icon_names_list = ['save', 'checkpoint_load', 'checkpoint_create', 'file_manager', 'content_table']
        icon_dir = {}

        for name in icon_names_list:
            icon_dir[name] = QtGui.QIcon()
            icon_dir[name].addPixmap(
                QtGui.QPixmap(
                    get_style_var(self.app_style, 'icons/'+name)
                        .replace('{APP_DIR}', app_directory)
                        .replace('/', os.sep)
                ),
                QtGui.QIcon.Normal, QtGui.QIcon.Off
            )

        self.button_save.setIcon(icon_dir['save'])
        self.button_load_checkpoint.setIcon(icon_dir['checkpoint_load'])
        self.button_create_checkpoint.setIcon(icon_dir['checkpoint_create'])
        self.button_file_manager.setIcon(icon_dir['file_manager'])
        self.button_edit_content_table.setIcon(icon_dir['content_table'])

        tmpcss = self.tmpDir + os.sep + "tmp.css"
        with open(tmpcss, "w", encoding="utf8") as file_page:
            file_page.write(get_style_var(self.app_style, 'QWebViewPreview'))
        self.webView.page().settings().setUserStyleSheetUrl(QtCore.QUrl.fromLocalFile(tmpcss))
        # self.webView.page().mainFrame().setScrollBarPolicy(QtCore.Qt.Vertical, QtCore.Qt.ScrollBarAlwaysOff)
        self.webView.setContextMenuPolicy(QtCore.Qt.NoContextMenu)

    def content_table_current_item_changed(self, current: QTreeWidgetItem, previous: QTreeWidgetItem):
        data = current.data(0, 99)
        print(data)

    def file_table_item_double_clicked(self, current: QTreeWidgetItem, previous: QTreeWidgetItem):
        try:
            data = current.data(0, 99)
            text = current.data(0, 98)
            print(text)
            if data != ':dir:':
                self.tabWidget.create_pane(text, data)
        except Exception:
            traceback.print_exc()

    def file_table_load(self):
        self.treeFileTable.clear()
        liste = listDirTree(self.tmpDir + os.sep + 'current', None)
        # print(liste)
        for index in liste:
            item = QtWidgets.QTreeWidgetItem(self.treeFileTable)
            item.setText(0, index)
            item.setData(0, 98, index)
            if isinstance(liste[index], dict):
                item.setData(0, 99, ':dir:')
                common.qt.setQTreeItemFolderIcon(item)
                item = self.recur_file_table_insert(item, liste[index])
            else:
                item.setData(0, 99, liste[index])
            self.treeFileTable.insertTopLevelItem(0, item)

    def recur_file_table_insert(self, base_item: QtWidgets.QTreeWidgetItem, tree: dict):
        for indexr in tree:
            itemr = QtWidgets.QTreeWidgetItem(base_item)
            itemr.setText(0, indexr)
            itemr.setData(0, 98, indexr)
            if isinstance(tree[indexr], dict):
                itemr.setData(0, 99, ':dir:')
                common.qt.setQTreeItemFolderIcon(itemr)

                itemr = self.recur_file_table_insert(itemr, tree[indexr])
            else:
                itemr.setData(0, 99, tree[indexr])
            base_item.addChild(itemr)
        return base_item

    def on_close_tab(self, index_tab: int):
        if self.tabWidget.count() == 0: 
            return
        print('on_close_tab')
        if self.tabWidget.count() > index_tab >= 0:
            self.tabWidget.removeTab(index_tab)

    def on_change_tab(self, index_tab: int):
        self.tabWidget.draw_preview()

    def create_check_point(self):
        try:
            print("create_check_point")
            stime = unixtime_to_string(time.time(), template='%Y-%m-%d_%H-%M-%S', is_utc=False)
            shutil.copytree(self.tmpDir + os.sep + 'current', self.tmpDir + os.sep + stime)
            InfoDialog(
                self.lang['Editor']['DialogCreateCheckpointWindowTitle'], 
                self.lang['Editor']['DialogCreateCheckpointWindowText'].format(stime), 
                self
            )
        except Exception:
            traceback.print_exc()

    def load_check_point(self):
        try:
            wl = CheckpointWindow(self, self.tmpDir)
            ret = wl.openExec()
            if ret is not None:
                if os.path.isdir(self.tmpDir + os.sep + ret) is True:
                    common.files.rmDir(self.tmpDir + os.sep + 'current')
                    common.files.copyDir(self.tmpDir + os.sep + ret, self.tmpDir + os.sep + 'current')
                    self.tabWidget.reload_contents()
        except Exception:
            traceback.print_exc()

    def save_ebook(self):
        try:
            ret = common.dialog.InfoDialogConfirm(
                self.lang['Editor']['DialogConfirmSaveWindowTitle'],
                self.lang['Editor']['DialogConfirmSaveWindowText'],
                self.lang['Generic']['DialogBtnYes'],
                self.lang['Generic']['DialogBtnNo'], self.parent()
            )
            if ret is True:
                os.remove(self.opened_file)
                deflate(self.tmpDir + os.sep + 'current' + os.sep + '*', self.opened_file)
        except Exception:
            traceback.print_exc()

    def load_file_managment(self):
        try:
            wl = FilesWindow(self, self.tmpDir + os.sep + 'current')
            ret = wl.open_exec()
            # print(ret)
            if ret is not None:
                for file in ret['delete']:
                    if ret['delete'][file]['type'] == 'deleteFile':
                        os.remove(self.tmpDir + os.sep + 'current' + ret['delete'][file]['innerPath'])
                    elif ret['delete'][file]['type'] == 'deleteFolder':
                        rmDir(self.tmpDir + os.sep + 'current' + ret['delete'][file]['innerPath'])
                for file in ret['rename']:
                    if ret['rename'][file]['type'] == 'renameFile':
                        rename(
                            self.tmpDir + os.sep + 'current' + ret['rename'][file]['original'],
                            self.tmpDir + os.sep + 'current' + ret['rename'][file]['newPath']
                        )
                    elif ret['rename'][file]['type'] == 'renameFolder':
                        rename(
                            self.tmpDir + os.sep + 'current' + ret['rename'][file]['original'],
                            self.tmpDir + os.sep + 'current' + ret['rename'][file]['newPath']
                        )
                for file in ret['new']:
                    # print(file)
                    if ret['new'][file]['type'] == 'new_file':
                        f = open(self.tmpDir + os.sep + 'current' + ret['new'][file]['innerPath'], 'w', encoding="utf8")
                        f.write(' ')
                        f.close()
                    elif ret['new'][file]['type'] == 'new_folder':
                        os.makedirs(self.tmpDir + os.sep + 'current' + ret['new'][file]['innerPath'])
                    elif ret['new'][file]['type'] == 'import':
                        copyFile(
                            ret['new'][file]['original'],
                            self.tmpDir + os.sep + 'current' + ret['new'][file]['innerPath']
                        )

                self.file_table_load()
        except Exception:
            traceback.print_exc()

    def load_content_table_managment(self):
        try:
            wl = ContentTableWindow(self, self.tmpDir + os.sep + 'current')
            ret = wl.open_exec()

            if ret is not None:
                li = common.files.listDir(self.tmpDir + os.sep + 'current', "ncx")
                if len(li) > 0:
                    file = open(li[0], "r", encoding="utf8")
                    content = file.read()
                    file.close()
                    mydoc = minidom.parseString(content.replace("  ", "").replace("\t", ""))
                    map = mydoc.getElementsByTagName('navMap')[0]
                    points = mydoc.getElementsByTagName('navPoint')
                    for i in range(0, len(points)):
                        map.removeChild(points[i])

                    i = 0
                    for obj in ret:
                        i += 1
                        point = mydoc.createElement('navPoint')
                        point.setAttribute('id', 'num_{}'.format(i))
                        point.setAttribute('playOrder', "{}".format(i))
                        label = mydoc.createElement('navLabel')
                        tx = mydoc.createElement('text')
                        text_node = minidom.Text()
                        text_node.data = obj['name']
                        tx.appendChild(text_node)
                        label.appendChild(tx)
                        point.appendChild(label)
                        content = mydoc.createElement('content')
                        content.setAttribute('src', obj['url'])
                        point.appendChild(content)
                        map.appendChild(point)

                    mydoc.toprettyxml()
                    file = open(li[0], "wt", encoding="utf8")
                    file.write(mydoc.toprettyxml().replace("\r", "").replace("\n", "").replace(">\t", ">\n\t"))
                    file.close()

                self.load_content_table()
        except Exception:
            traceback.print_exc()

    def load_content_table(self):
        directory = self.tmpDir + os.sep + 'current' + os.sep
        li = common.files.listDir(directory, "opf")
        file_name = li[0][li[0].rindex(os.sep)+1:]
        data = ''
        with open(li[0]) as myfile:
            data = myfile.read()

        chapters = parse_content_table(
            data,
            li[0].replace(directory, '').replace(file_name, '').replace(os.sep, '/'),
            directory
        )
        print(chapters)
        for index in chapters:
            last_slash = index['src'].rindex('/') + 1
            item = QtWidgets.QTreeWidgetItem(self.treeContentTable)
            item.setText(0, index['name'])
            item.setData(0, 98, index['src'][last_slash:])
            item.setData(0, 99, directory + index['src'].replace('/', os.sep))
            common.qt.setQTreeItemIcon(item, common.qt.QtQIconEnum.file)
            self.treeContentTable.insertTopLevelItem(0, item)
