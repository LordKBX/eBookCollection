import os
import sys
if os.name == 'nt':
	import ctypes
import subprocess
import shutil
import re

from PyQt5 import QtCore, QtGui, QtWidgets

try:
	# Line written for IDE import scraping
	from editor.mainwindow_ui import *
	from editor.editing_pane import *
except Exception:
	sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
	from mainwindow_ui import *
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


if __name__ == "__main__":
	previousEvent = ''
	app = QtWidgets.QApplication(sys.argv)
	print(sys.argv)
	print(env_vars)
	lang = Lang()
	bdd = BDD()

	app_icon = QtGui.QIcon()
	app_icon.addFile(appDir + '/icons/app_icon16x16.png', QtCore.QSize(16, 16))
	app_icon.addFile(appDir + '/icons/app_24x24.png', QtCore.QSize(24, 24))
	app_icon.addFile(appDir + '/icons/app_32x32.png', QtCore.QSize(32, 32))
	app_icon.addFile(appDir + '/icons/app_48x48.png', QtCore.QSize(48, 48))
	app_icon.addFile(appDir + '/icons/app_256x256.png', QtCore.QSize(256, 256))
	app.setWindowIcon(app_icon)
	if os.name == 'nt':
		myappid = 'lordkbx.ebook_collection.editor'
		ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

	try:
		EditorWindow = QtWidgets.QMainWindow()
		ui = Ui_MainWindow()
		ui.setupUi(EditorWindow)

		# ui.tabWidget
		ui.tabWidget.clear()
		ui.tabWidget.createPane("test", "D:\\CODES\\Python\\EbookCollection\\version.txt")

		# Button connec signals to slots
		# ui.buttonFullScreen.clicked.connect(toogleFullScreen)

		# Processing File Table
		ui.treeFileTable.clear()
		ui.treeFileTable.headerItem().setText(0, lang['Editor']['FileTableHeader'])
		ui.treeFileTable.currentItemChanged.connect(ContentTableCurrentItemChanged)
		ui.treeFileTable.setIndentation(10)
		ui.treeFileTable.setCursor(QtCore.Qt.PointingHandCursor)

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
		EditorWindow.setWindowTitle(
			lang['Editor']['WindowTitle'] + ' - ' + file.replace(os.sep, '/')
				.replace(mappdir, '').replace('/', ' / ').replace(ext, '')
		)
		EditorWindow.show()
		destDir = appDir + '/editor/tmp'.replace('/', os.sep)
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

		# ui.webView.setUrl(QtCore.QUrl(page))
		# tmpcss = destDir + "/tmp.css"
		# filePage = open(tmpcss, "w", encoding="utf8")
		# filePage.write("body { -webkit-user-select: none; }")
		# filePage.close()
		# ui.webView.page().settings().setUserStyleSheetUrl(QtCore.QUrl.fromLocalFile(tmpcss))
		ui.webView.page().mainFrame().setScrollBarPolicy(QtCore.Qt.Vertical, QtCore.Qt.ScrollBarAlwaysOff)
		ui.webView.setContextMenuPolicy(QtCore.Qt.NoContextMenu)

		app.exec_()
		# rmDir(destDir)
	except Exception:
		traceback.print_exc()
	sys.exit(0)
