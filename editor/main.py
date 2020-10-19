import os
import sys
if os.name == 'nt':
	import ctypes
import subprocess
import shutil
import re
from pprint import pprint

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtWebKitWidgets
import PyQt5.uic
from PyQt5.uic import *

try:
	# Line written for IDE import scraping
	from editor.editing_pane import *
except Exception:
	sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
	from editing_pane import *
from vars import *
from lang import *
from bdd import *
from dialog import *
from common import *
from booksTools import *

EditorWindow = None
ui = None


def ContentTableCurrentItemChanged(current: QtWidgets.QTreeWidgetItem, previous: QtWidgets.QTreeWidgetItem):
	print(current.data(0, 99))
	data = current.data(0, 99)


def fileTableItemDoubleClicked(current: QtWidgets.QTreeWidgetItem, previous: QtWidgets.QTreeWidgetItem):
	data = current.data(0, 99)
	text = current.text(0)
	if data != ':dir:':
		print(data)
		print(text)
		ui.tabWidget.createPane(text, data)


def eventHandler(event: dict):
	global previousEvent, ui
	print(event)


def recurFileTableInsert(baseItem: QtWidgets.QTreeWidgetItem, tree: dict):
	for indexr in tree:
		itemr = QtWidgets.QTreeWidgetItem(baseItem)
		itemr.setText(0, indexr)
		if isinstance(tree[indexr], dict):
			itemr.setData(0, 99, ':dir:')
			itemr = recurFileTableInsert(itemr, tree[indexr])
		else:
			itemr.setData(0, 99, tree[indexr])
		baseItem.addChild(itemr)
	return baseItem


def onCloseTab(indexTab: int):
	global ui
	if ui.tabWidget.count() == 0: return
	print('onCloseTab')
	if ui.tabWidget.count() > indexTab >= 0:
		ui.tabWidget.removeTab(indexTab)

def onChangeTab(indexTab: int):
	ui.tabWidget.drawPreview()


class editorWindow(QtWidgets.QMainWindow):
	def __init__(self, parent: QtWidgets.QMainWindow):
		super(editorWindow, self).__init__(parent)
		PyQt5.uic.loadUi(appDir + '/editor/editor.ui'.replace('/', os.sep), self)
		self.show()


if __name__ == "__main__":
	lng = Lang()
	destDir = appDir + '/editor/tmp'.replace('/', os.sep)
	default_page = lng['Editor']['WebViewDefaultPageContent']
	previousEvent = ''
	app = QtWidgets.QApplication(sys.argv)
	print(sys.argv)
	print(env_vars)
	lang = Lang()
	bdd = BDD()

	app_icon = QtGui.QIcon()
	app_icon.addFile(appDir + '/icons/app_icon16x16.png', QtCore.QSize(16, 16))
	app_icon.addFile(appDir + '/icons/app_icon24x24.png', QtCore.QSize(24, 24))
	app_icon.addFile(appDir + '/icons/app_icon32x32.png', QtCore.QSize(32, 32))
	app_icon.addFile(appDir + '/icons/app_icon48x48.png', QtCore.QSize(48, 48))
	app_icon.addFile(appDir + '/icons/app_icon256x256.png', QtCore.QSize(256, 256))
	app.setWindowIcon(app_icon)
	if os.name == 'nt':
		myappid = 'lordkbx.ebook_collection.editor'
		ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

	try:
		EditorWindow = QtWidgets.QMainWindow()
		ui = editorWindow(EditorWindow)
		for attr in dir(ui):
			print("obj.%s = %r" % (attr, getattr(ui, attr)))

		# ui.tabWidget
		ui.tabWidget.clear()
		ui.tabWidget.setStyleSheet(
			"""
			QFrame { 
				background: rgb(50, 50, 50);
			}
			QTabWidget::pane { 
			}
			QTabWidget::tab-bar { }
			QTabBar::tab {
				background: rgb(80, 80, 80) !important;
				color: white;
				padding: 5px;
				margin-right:2px;
				border-color:rgb(0,0,0);
				border-width:1px;
				border-style:solid;
			}
			QTabBar::tab:selected { background: rgb(0, 135, 202) !important; }
			QTabBar::close-button { 
				border-image: none;
				image: url('"""+appDir.replace(os.sep, '/')+"""/icons/white/close.png');
				cursor: pointer;
			}
			QTabBar::close-button:hover { 
				border-image: none;
				image: url('"""+appDir.replace(os.sep, '/')+"""/icons/black/close.png');
			}
			"""
		)
		ui.tabWidget.setPreviewWebview(ui.webView, default_page)
		ui.tabWidget.tabCloseRequested.connect(onCloseTab)
		ui.tabWidget.currentChanged.connect(onChangeTab)


		# Button connec signals to slots
		# ui.buttonFullScreen.clicked.connect(toogleFullScreen)

		# Processing File Table
		ui.treeFileTable.clear()
		ui.treeFileTable.headerItem().setText(0, lang['Editor']['FileTableHeader'])
		ui.treeFileTable.itemDoubleClicked.connect(fileTableItemDoubleClicked)
		ui.treeFileTable.setIndentation(10)
		ui.treeFileTable.setCursor(QtCore.Qt.PointingHandCursor)
		ui.treeFileTable.setStyleSheet(
			"""
			QTreeView::branch:has-siblings:!adjoins-item { }
			QTreeView::branch:has-siblings:adjoins-item { }
			QTreeView::branch:!has-children:!has-siblings:adjoins-item { }
			
			QTreeView::branch:has-children:!has-siblings:closed, QTreeView::branch:closed:has-children:has-siblings {
				border-image: none;
				image: url('"""+appDir.replace(os.sep, '/')+"""/icons/white/tree_closed.png');
			}

			QTreeView::branch:open:has-children:!has-siblings,
			QTreeView::branch:open:has-children:has-siblings  {
				border-image: none;
				image: url('"""+appDir.replace(os.sep, '/')+"""/icons/white/tree_opened.png');
			}
			"""
		)

		# Processing Content Table
		ui.treeContentTable.clear()
		ui.treeContentTable.headerItem().setText(0, lang['Editor']['ContentTableHeader'])
		ui.treeContentTable.currentItemChanged.connect(ContentTableCurrentItemChanged)
		ui.treeContentTable.setIndentation(0)
		ui.treeContentTable.setCursor(QtCore.Qt.PointingHandCursor)

		if len(sys.argv) < 2:
			WarnDialog(lang['Editor']['DialogInfoNoFileWindowTitle'], lang['Editor']['DialogInfoNoFileWindowText'], EditorWindow)
			exit(0)

		file = sys.argv[1]

		mappdir = appDir.replace(os.sep, '/')+'/data/'
		filepath, ext = os.path.splitext(file)
		ui.setWindowTitle(
			lang['Editor']['WindowTitle'] + ' - ' + file.replace(os.sep, '/')
				.replace(mappdir, '').replace('/', ' / ').replace(ext, '')
		)
		# EditorWindow.show()
		print(destDir)
		rmDir(destDir)
		if os.path.isdir(destDir) is not True: os.mkdir(destDir)
		page = 'file:///C:/Users/KevBo/wuxiaworld_export_ebook/tmp/toc.xhtml'

		if ext in ['.epub', '.epub2', '.epub3']:
			ret = deflate(file, destDir)
			print(ret)
			liste = listDirTree(destDir, None)
			print(liste)
			for index in liste:
				item = QtWidgets.QTreeWidgetItem(ui.treeFileTable)
				item.setText(0, index)
				if isinstance(liste[index], dict):
					item.setData(0, 99, ':dir:')
					item = recurFileTableInsert(item, liste[index])
				else:
					item.setData(0, 99, liste[index])
				ui.treeFileTable.insertTopLevelItem(0, item)

		elif ext in ['.cbz', '.cbr']:
			deflate(file, destDir)
			liste = listDir(destDir, 'jpg|jpeg|png').sort()
		else:
			WarnDialog(lang['Editor']['DialogInfoBadFileWindowTitle'], lang['Editor']['DialogInfoBadFileWindowText'], EditorWindow)
			exit(0)

		ui.webView.setHtml(default_page)
		tmpcss = destDir + "/tmp.css"
		filePage = open(tmpcss, "w", encoding="utf8")
		filePage.write("body { background:#999999;color:#ffffff; }")
		filePage.close()
		ui.webView.page().settings().setUserStyleSheetUrl(QtCore.QUrl.fromLocalFile(tmpcss))
		# ui.webView.page().mainFrame().setScrollBarPolicy(QtCore.Qt.Vertical, QtCore.Qt.ScrollBarAlwaysOff)
		ui.webView.setContextMenuPolicy(QtCore.Qt.NoContextMenu)

		# données de test
		# ui.tabWidget.createPane("test", "D:\\CODES\\Python\\EbookCollection\\editor\\tmp\\OEBPS\\content.opf")

		app.exec_()
		# rmDir(destDir)
	except Exception:
		traceback.print_exc()
	sys.exit(0)
