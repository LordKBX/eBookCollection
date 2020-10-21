import os
import sys
if os.name == 'nt':
	import ctypes

import PyQt5.uic
from PyQt5.uic import *

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from bdd import *
from common.dialog import *
from common.books import *
from common.archive import *
from reader.CustomQWebView import *

ui = None


def toogleFullScreen():
	if ui.isFullScreen() is True:
		ui.showNormal()
		icon1 = QtGui.QIcon()
		icon1.addPixmap(QtGui.QPixmap("../icons/white/full_screen.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		ui.buttonFullScreen.setIcon(icon1)
	else:
		ui.showFullScreen()
		icon1 = QtGui.QIcon()
		icon1.addPixmap(QtGui.QPixmap("../icons/white/normal_screen.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		ui.buttonFullScreen.setIcon(icon1)


def DisplayTreeContentTable():
	if ui.buttonContentTable.isChecked():
		ui.treeContentTable.setMinimumWidth(180)
		ui.treeContentTable.setMaximumWidth(180)
	else:
		ui.treeContentTable.setMinimumWidth(0)
		ui.treeContentTable.setMaximumWidth(0)


def ContentTableCurrentItemChanged(current: QtWidgets.QTreeWidgetItem, previous: QtWidgets.QTreeWidgetItem):
	print(appMode)
	print(current.data(0, 99))
	data = current.data(0, 99)
	if appMode.value == QwwMode.CBZ.value:
		if data == 'cover':
			ui.webView.updatePositionCbzStart()
		elif data == 'end':
			ui.webView.updatePositionCbzEnd()
		elif re.search('^page:', data) is not None:
			td = data.split(':')
			ui.webView.updatePositionCbzByPage(int(float(td[1])))
	elif appMode.value == QwwMode.EPUB.value:
		if re.search('^chapter:', data) is not None:
			td = data.split(':')
			page = destDir + "/" + td[1]
			page = 'file:///' + page.replace("\\", '/')
			ui.webView.setUrl(QtCore.QUrl(page))


def eventHandler(event: dir):
	global previousEvent, ui
	try:
		evt = '{}'.format(event)
		if event['type'] == 'pageChange':
			if ui.webView.mode.value == QwwMode.CBZ.value:
				ui.treeContentTable.setCurrentItem(ui.treeContentTable.topLevelItem(event['index']), 0)
		if evt == previousEvent:
			if event['type'] == 'chapterChange':
				if ui.webView.mode.value == QwwMode.EPUB.value:
					index = 0
					try: index = ui.treeContentTable.currentIndex().row()
					except Exception: {}
					if event['value'] == 'prev':
						if index - 1 >= 0:
							ui.treeContentTable.setCurrentItem(ui.treeContentTable.topLevelItem(index - 1), 0)
							timer = QtCore.QTimer()
							timer.singleShot(100, ui.webView.updatePositionCbzEnd)
					if event['value'] == 'next':
						if index + 1 < ui.treeContentTable.topLevelItemCount():
							ui.treeContentTable.setCurrentItem(ui.treeContentTable.topLevelItem(index + 1), 0)
		previousEvent = evt
		# print(event)
	except Exception:
		traceback.print_exc()


class readerWindow(QtWidgets.QMainWindow):
	def __init__(self, parent: QtWidgets.QMainWindow):
		super(readerWindow, self).__init__(parent)
		PyQt5.uic.loadUi(appDir + '/reader/reader2.ui'.replace('/', os.sep), self)
		self.show()


if __name__ == "__main__":
	previousEvent = ''
	print(sys.argv)
	print(env_vars)
	lang = Lang()
	bdd = BDD()

	print(appDir + '/icons/app_icon16x16.png'.replace('/', os.sep))

	app = QtWidgets.QApplication([])
	app_icon = QtGui.QIcon()
	app_icon.addFile(appDir + '/icons/app_icon16x16.png'.replace('/', os.sep), QtCore.QSize(16, 16))
	app_icon.addFile(appDir + '/icons/app_icon24x24.png'.replace('/', os.sep), QtCore.QSize(24, 24))
	app_icon.addFile(appDir + '/icons/app_icon32x32.png'.replace('/', os.sep), QtCore.QSize(32, 32))
	app_icon.addFile(appDir + '/icons/app_icon48x48.png'.replace('/', os.sep), QtCore.QSize(48, 48))
	app_icon.addFile(appDir + '/icons/app_icon256x256.png'.replace('/', os.sep), QtCore.QSize(256, 256))
	app.setWindowIcon(app_icon)
	if os.name == 'nt':
		myappid = 'lordkbx.ebook_collection.reader'
		ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

	ui = readerWindow(None)
	ui.show()

	
	# Button FullScreen
	icon1 = QtGui.QIcon()
	icon1.addPixmap(QtGui.QPixmap(appDir+"/icons/white/full_screen.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
	ui.buttonFullScreen.setIcon(icon1)
	ui.buttonFullScreen.clicked.connect(toogleFullScreen)

	# Button Content Table
	icon2 = QtGui.QIcon()
	icon2.addPixmap(QtGui.QPixmap(appDir+"/icons/white/content_table.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
	ui.buttonContentTable.setIcon(icon2)
	ui.buttonContentTable.clicked.connect(DisplayTreeContentTable)
	ui.treeContentTable.setMinimumWidth(180)
	ui.treeContentTable.setMaximumWidth(180)

	# Button Info
	icon3 = QtGui.QIcon()
	icon3.addPixmap(QtGui.QPixmap(appDir+"/icons/white/info.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
	ui.buttonInfo.setIcon(icon3)
	# ui.buttonInfo.clicked.connect(DisplayTreeContentTable)

	# Processing Content Table
	ui.treeContentTable.clear()
	ui.treeContentTable.headerItem().setText(0, lang['Reader']['ContentTableHeader'])
	ui.treeContentTable.currentItemChanged.connect(ContentTableCurrentItemChanged)
	ui.treeContentTable.setIndentation(0)
	ui.treeContentTable.setCursor(QtCore.Qt.PointingHandCursor)

	if len(sys.argv) < 2:
		WarnDialog(lang['Reader']['DialogInfoNoFileWindowTitle'], lang['Reader']['DialogInfoNoFileWindowText'], ui)
		exit(0)

	file = sys.argv[1]

	mappdir = appDir.replace(os.sep, '/')+'/data/'
	filepath, ext = os.path.splitext(file)
	ui.setWindowTitle(
		lang['Reader']['WindowTitle'] + ' - ' + file.replace(os.sep, '/')
			.replace(mappdir, '').replace('/', ' / ').replace(ext, '')
	)
	destDir = appDir + '/reader/tmp'
	rmDir(destDir)
	if os.path.isdir(destDir) is not True: os.mkdir(destDir)
	page = ''

	appMode = QwwMode.CBZ
	if ext in ['.epub', '.epub2', '.epub3']:
		appMode = QwwMode.EPUB
		bookData = getEpubIfo(file)
		winTitle = lang['Reader']['WindowTitle'] + ' - '
		first = True
		for index in ['authors', 'serie', 'title']:
			if bookData[index] is not None:
				if bookData[index].strip() != '':
					if first is False:
						winTitle += ' / '
					else: first = False
					winTitle += bookData[index]

		ui.setWindowTitle(winTitle)
		ret = inflate(file, destDir)
		page = destDir + "/" + bookData['chapters'][0]['src']
		page = 'file:///' + page.replace("\\", '/')
		i = 0
		max = len(bookData['chapters'])
		while i < max:
			item = QtWidgets.QTreeWidgetItem(ui.treeContentTable)
			item.setText(0, bookData['chapters'][i]['name'])
			item.setData(0, 99, "chapter:{}".format(bookData['chapters'][i]['src']))
			ui.treeContentTable.insertTopLevelItem(0, item)
			i += 1
		ui.treeContentTable.setCurrentItem(ui.treeContentTable.topLevelItem(0), 0)

	elif ext in ['.cbz', '.cbr']:
		appMode = QwwMode.CBZ
		ret = inflate(file, destDir)
		print(ret)
		imgList = listDir(destDir, 'jpg|jpeg|png')
		page = destDir + "/page.xhtml"
		filePage = open(page, "w", encoding="utf8")
		imgStyle = 'img{ max-width:100%; max-height:100%; display:block; margin: 0 auto; }'
		imgStyle = 'img{ display:block; margin: 0 auto; }'

		filePage.write("""<html xmlns="http://www.w3.org/1999/xhtml">
		<head>
			<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
			<title>""" + file + """</title>
			<link href="common.css" rel="stylesheet" type="text/css"/>
			<style>
				*{ margin:0; padding:0; border:0; } 
				html, body, section, div{ height:100%; }
				""" + imgStyle + """
			</style>
		</head>
		<body>
			<section>"""
		)
		for img in imgList:
			filePage.write("\n<img src=\"" + 'file:///' + img.replace("\\", '/') + "\"/>")
		filePage.write("""\t\t\t</section>
			<script type="text/javascript">
				function imgResize(){
					height = window.innerHeight;
					list = document.querySelectorAll('img')
					for(id in list){
						list[id].style.height = '' + height + 'px';
					}
				}
				
				imgResize();
			</script>
		</body></html>""")
		filePage.close()
		page = 'file:///' + page.replace("\\", '/')

		item = QtWidgets.QTreeWidgetItem(ui.treeContentTable)
		item.setText(0, lang['Reader']['ContentTableTxtCover'])
		item.setData(0, 99, "cover")
		ui.treeContentTable.insertTopLevelItem(0, item)

		i = 1
		max = len(imgList)
		while i < max - 1:
			item = QtWidgets.QTreeWidgetItem(ui.treeContentTable)
			item.setText(0, lang['Reader']['ContentTableTxtPageX'].format(i))
			item.setData(0, 99, "page:{}".format(i))
			ui.treeContentTable.insertTopLevelItem(0, item)
			i += 1

		item = QtWidgets.QTreeWidgetItem(ui.treeContentTable)
		item.setText(0, lang['Reader']['ContentTableTxtEnd'])
		item.setData(0, 99, "end")
		ui.treeContentTable.insertTopLevelItem(0, item)
		ui.treeContentTable.setCurrentItem(ui.treeContentTable.topLevelItem(0), 0)
	else:
		WarnDialog(lang['Reader']['DialogInfoBadFileWindowTitle'], lang['Reader']['DialogInfoBadFileWindowText'], ui)
		exit(0)

	ui.webView.setMode(appMode)
	ui.webView.setEventHandler(eventHandler)
	ui.webView.setUrl(QtCore.QUrl(page))
	tmpcss = destDir + "/tmp.css"
	filePage = open(tmpcss, "w", encoding="utf8")
	filePage.write("body { -webkit-user-select: none; }")
	filePage.close()
	# ui.webView.page().settings().setUserStyleSheetUrl(QtCore.QUrl.fromLocalFile(tmpcss))
	ui.webView.page().mainFrame().setScrollBarPolicy(QtCore.Qt.Vertical, QtCore.Qt.ScrollBarAlwaysOff)
	ui.webView.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
	app.exec_()
	rmDir(destDir)
	sys.exit(0)
