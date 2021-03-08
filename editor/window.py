from checkpoint import *
from files import *
from content_table_editor import *
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

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
    tmpcss = ''
    toc_type = ''

    def __init__(self, parent: QtWidgets.QMainWindow, opened_file, lang, bdd):
        super(EditorWindow, self).__init__(parent)
        PyQt5.uic.loadUi(os.path.dirname(os.path.realpath(__file__)) + os.sep + 'editor.ui'.replace('/', os.sep), self)
        self.opened_file = opened_file
        self.tmpDir = app_user_directory + os.sep + 'editor' + os.sep + 'tmp'
        try:
            rmDir(self.tmpDir)
            if os.path.isdir(self.tmpDir) is not True:
                os.makedirs(self.tmpDir + os.sep + 'original')
                os.makedirs(self.tmpDir + os.sep + 'current')
        except Exception:
            ""
        self.lang = lang
        self.BDD = bdd

        # load window size
        size_tx = self.BDD.get_param('editor/windowSize')
        if size_tx is not None and size_tx != '':
            size = eval(size_tx)
            self.resize(size[0], size[1])
        # load window position
        pos_tx = self.BDD.get_param('editor/windowPos')
        if pos_tx is not None and pos_tx != '':
            pos = eval(pos_tx)
            self.move(pos[0], pos[1])
            self.pos()

        self.app_style = self.BDD.get_param('style')
        self.apply_translation()
        self.apply_style()

        # ui.tabWidget
        ad = app_directory.replace(os.sep, '/')
        self.tabWidget.clear()
        self.voidLabel.setVisible(True)
        self.tabWidget.setVisible(False)
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
        self.webView.page().settings().setUserStyleSheetUrl(QtCore.QUrl.fromLocalFile(self.tmpcss))
        self.webView.setContextMenuPolicy(QtCore.Qt.NoContextMenu)

        filepath, ext = os.path.splitext(self.opened_file)
        mappdir = app_directory.replace(os.sep, '/') + '/data/'
        self.setWindowTitle(
            self.lang['Editor']['WindowTitle'] + ' - ' + self.opened_file.replace(os.sep, '/')
            .replace(mappdir, '').replace('/', ' / ').replace(ext, '')
        )
        # EditorWindow.show()

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

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        size = self.size()
        tx = [size.width(), size.height()].__str__()
        self.BDD.set_param('editor/windowSize', tx)

    def moveEvent(self, a0: QtGui.QMoveEvent) -> None:
        pos = self.pos()
        tx = [pos.x(), pos.y()].__str__()
        self.BDD.set_param('editor/windowPos', tx)

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

        self.voidLabel.setText(self.lang['Editor/CentralZoneEmpty'])

    def apply_style(self):
        self.setStyleSheet(get_style_var(self.app_style, 'QMainWindow'))
        self.dockTopContents.setStyleSheet(get_style_var(self.app_style, 'QMainWindow'))
        self.voidLabel.setStyleSheet(get_style_var(self.app_style, 'EditorCentralLabel'))

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

        self.tmpcss = self.tmpDir + os.sep + "tmp.css"
        with open(self.tmpcss, "w", encoding="utf8") as file_page:
            print('tmpcss = ' + get_style_var(self.app_style, 'QWebViewPreview'))
            file_page.write(get_style_var(self.app_style, 'QWebViewPreview'))

        self.tabWidget.setStyleSheet(get_style_var(self.app_style, 'QTabWidgetHorizontal'))
        self.tabWidget.setBackgroundRole(QtGui.QPalette.ColorRole(QtGui.QPalette.Light))

    def content_table_current_item_changed(self, current: QTreeWidgetItem, previous: QTreeWidgetItem):
        data = current.data(0, 99)
        print(data)

    def file_table_item_double_clicked(self, current: QTreeWidgetItem, previous: QTreeWidgetItem):
        try:
            data = current.data(0, 99)
            text = current.data(0, 98)
            print(text)
            if data != ':dir:':
                icon = self.file_icon(data)
                self.tabWidget.create_pane(text, icon, data, self.tmpcss)
                self.voidLabel.setVisible(False)
                self.tabWidget.setVisible(True)
        except Exception:
            traceback.print_exc()

    def file_table_load(self):
        self.treeFileTable.clear()
        liste = list_directory_tree(self.tmpDir + os.sep + 'current', None)
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
                self.icon_file_item(item, liste[index])
                item.setData(0, 99, liste[index])
            self.treeFileTable.insertTopLevelItem(0, item)

    def recur_file_table_insert(self, base_item: QtWidgets.QTreeWidgetItem, tree: dict):
        for indexr in tree:
            itemr = QtWidgets.QTreeWidgetItem(base_item)
            itemr.setText(0, indexr)
            itemr.setData(0, 98, indexr)
            if isinstance(tree[indexr], dict):
                itemr.setData(0, 99, ':dir:')
                common.qt.setQTreeItemIcon(itemr, get_style_var(self.app_style, 'icons/folder'))

                itemr = self.recur_file_table_insert(itemr, tree[indexr])
            else:
                self.icon_file_item(itemr, tree[indexr])
                itemr.setData(0, 99, tree[indexr])
            base_item.addChild(itemr)
        return base_item

    def file_icon(self, file_path: str):
        file_type = get_file_type(file_path)
        if file_type.startswith('image/'):
            return get_style_var(self.app_style, 'icons/image')
        elif file_type.startswith('text/css'):
            return get_style_var(self.app_style, 'icons/style')
        elif file_type.startswith('application/oebps-package+xml'):  # .opf
            return get_style_var(self.app_style, 'icons/info')
        elif file_type.startswith('application/x-dtbncx+xml'):  # .ncx
            return get_style_var(self.app_style, 'icons/content_table')
        elif file_type.startswith('application/xml'):
            return get_style_var(self.app_style, 'icons/xml')
        elif file_type.startswith('application/x-font-truetype'):
            return get_style_var(self.app_style, 'icons/font')
        elif file_type.startswith('application/xhtml+xml'):
            return get_style_var(self.app_style, 'icons/page')
        else:
            return get_style_var(self.app_style, 'icons/file')

    def icon_file_item(self, item: QTreeWidgetItem, file_path: str):
        icon = self.file_icon(file_path)
        file_type = get_file_type(file_path)
        common.qt.setQTreeItemIcon(item, icon)

    def on_close_tab(self, index_tab: int):
        if self.tabWidget.count() == 0:
            return
        print('on_close_tab')
        if self.tabWidget.count() > index_tab >= 0:
            self.tabWidget.removeTab(index_tab)
        if self.tabWidget.count() == 0:
            self.voidLabel.setVisible(True)
            self.tabWidget.setVisible(False)

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
                chapters = []
                for obj in ret:
                    chapters.append(obj['url'][1:])
                self.save_metada(chapters)

                if self.toc_type == 'NCX':
                    li = common.files.list_directory(self.tmpDir + os.sep + 'current', "ncx")
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
                        file.write(mydoc.toprettyxml().replace("\r", "").replace("\n", "").replace("  ", "").replace(">\t", ">\n\t"))
                        file.close()
                self.load_content_table()
        except Exception:
            traceback.print_exc()

    def load_content_table(self):
        self.treeContentTable.clear()
        directory = self.tmpDir + os.sep + 'current' + os.sep
        li = common.files.list_directory(directory, "opf")
        file_name = li[0][li[0].rindex(os.sep)+1:]
        data = ''
        with open(li[0]) as myfile:
            data = myfile.read()

        self.toc_type, chapters = parse_content_table(
            data,
            li[0].replace(directory, '').replace(file_name, '').replace(os.sep, '/'),
            directory
        )
        for chapter in chapters:
            try:
                try:
                    last_slash = chapter['src'].rindex('/')
                except ValueError:
                    last_slash = - 1
                item = QtWidgets.QTreeWidgetItem(self.treeContentTable)
                item.setText(0, chapter['name'])
                item.setData(0, 98, chapter['src'][last_slash+1:])
                item.setData(0, 99, directory + chapter['src'].replace('/', os.sep))
                common.qt.setQTreeItemIcon(item, get_style_var(self.app_style, 'icons/page'))
                self.treeContentTable.insertTopLevelItem(0, item)
            except Exception:
                traceback.print_exc()

    def save_metada(self, chapters: list = None):
        li = common.files.list_directory(self.tmpDir + os.sep + 'current', "opf")
        if len(li) > 0:
            file = open(li[0], "r", encoding="utf8")
            content = file.read()
            file.close()
            print(content)
            mydoc = minidom.parseString(content)

            manifest = mydoc.getElementsByTagName('manifest')[0]
            items = mydoc.getElementsByTagName('item')
            for i in range(0, len(items)):
                manifest.removeChild(items[i])

            spine = mydoc.getElementsByTagName('spine')[0]
            toc = None
            try:
                toc = spine.attributes['toc'].value
            except Exception:
                ""
            refs_list = mydoc.getElementsByTagName('item')
            for i in range(0, len(refs_list)):
                spine.removeChild(refs_list[i])

            files = common.files.list_directory(self.tmpDir + os.sep + 'current')
            idno = 1
            list_refs = {}
            for file in files:
                path = file.replace(self.tmpDir + os.sep + 'current' + os.sep, '')
                tp = path.split('.')
                ext = None
                if len(tp) > 1 and "META-INF" not in path:
                    ext = tp[len(tp) - 1].lower()
                    mtype = 'text/plain'
                    try:
                        mtype = mediatypes[ext]
                    except Exception:
                        ""
                    item = mydoc.createElement('item')
                    item.setAttribute('id', 'id{}'.format(idno))
                    item.setAttribute('href', path)
                    item.setAttribute('media-type', mtype)
                    manifest.appendChild(item)

                    if ext in ['ncx']:
                        spine.attributes['toc'].value = 'id{}'.format(idno)
                    if ext in ['xhtml', 'html']:
                        itemref = mydoc.createElement('itemref')
                        itemref.setAttribute('idref', 'id{}'.format(idno))
                        if chapters is None:
                            spine.appendChild(itemref)
                        else:
                            list_refs[path] = itemref

                    idno += 1
            if chapters is not None:
                print(list_refs)
                for chapter in chapters:
                    if chapter in list_refs:
                        spine.appendChild(list_refs[chapter])

            mydoc.toprettyxml()
            file = open(li[0], "wt", encoding="utf8")
            file.write(mydoc.toprettyxml().replace("\r", "").replace("\n", "").replace("  ", "").replace(">\t", ">\n\t"))
            file.close()
