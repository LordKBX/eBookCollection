import os
import sys
if os.name == 'nt':
	import ctypes

import PyQt5.uic
from PyQt5.uic import *

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from editor.editing_pane import *
from editor.window import *
from bdd import *
from common.dialog import *
from common.books import *
from common.files import *
from common.archive import *

ui = None


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
	lng = Lang()

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
		ui = editorWindow(None)

		if len(sys.argv) < 2:
			WarnDialog(lang['Editor']['DialogInfoNoFileWindowTitle'], lang['Editor']['DialogInfoNoFileWindowText'], ui)
			exit(0)

		file = sys.argv[1]

		mappdir = appDir.replace(os.sep, '/')+'/data/'
		filepath, ext = os.path.splitext(file)
		ui.setWindowTitle(
			lang['Editor']['WindowTitle'] + ' - ' + file.replace(os.sep, '/')
				.replace(mappdir, '').replace('/', ' / ').replace(ext, '')
		)
		# EditorWindow.show()
		destDir = appDir + os.sep + 'editor' + os.sep + 'tmp'
		print(destDir)
		rmDir(destDir)
		if os.path.isdir(destDir) is not True:
			os.makedirs(destDir + os.sep + 'original')
			os.makedirs(destDir + os.sep + 'current')
		page = 'file:///C:/Users/KevBo/wuxiaworld_export_ebook/tmp/toc.xhtml'

		if ext in ['.epub', '.epub2', '.epub3']:
			ret = inflate(file, destDir + os.sep + 'original')
			ret = inflate(file, destDir + os.sep + 'current')
			liste = listDirTree(destDir + os.sep + 'current', None)
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
			ret = inflate(file, destDir + os.sep + 'original')
			ret = inflate(file, destDir + os.sep + 'current')
			liste = listDir(destDir + os.sep + 'current', 'jpg|jpeg|png').sort()
		else:
			WarnDialog(lang['Editor']['DialogInfoBadFileWindowTitle'], lang['Editor']['DialogInfoBadFileWindowText'], ui)
			exit(0)

		ui.show()
		ui.webView.setHtml(lang['Editor']['WebViewDefaultPageContent'])
		tmpcss = destDir + "/tmp.css"
		filePage = open(tmpcss, "w", encoding="utf8")
		filePage.write("body { background:#999999;color:#ffffff; }")
		filePage.close()
		ui.webView.page().settings().setUserStyleSheetUrl(QtCore.QUrl.fromLocalFile(tmpcss))
		# ui.webView.page().mainFrame().setScrollBarPolicy(QtCore.Qt.Vertical, QtCore.Qt.ScrollBarAlwaysOff)
		ui.webView.setContextMenuPolicy(QtCore.Qt.NoContextMenu)

		# données de test
		ui.tabWidget.createPane("metadata.opf", appDir + os.sep + 'editor' + os.sep + 'tmp' + os.sep + 'current' + os.sep + 'metadata.opf')

		app.exec_()
		# rmDir(destDir)
	except Exception:
		traceback.print_exc()
	sys.exit(0)
