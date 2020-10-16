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
	from reader.reader_ui import *
	from reader.CustomQWebView import *
except Exception:
	sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
	from reader_ui import *
	from CustomQWebView import *
from vars import *
from lang import *
from dialog import *
from common import *

ReaderWindow = None
ui = None


def toogleFullScreen():
	if ReaderWindow.isFullScreen() is True:
		ReaderWindow.showNormal()
		icon1 = QtGui.QIcon()
		icon1.addPixmap(QtGui.QPixmap("../icons/white/full_screen.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		ui.buttonFullScreen.setIcon(icon1)
	else:
		ReaderWindow.showFullScreen()
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
	

def deflate(src: str, dest: str):
	list_args = list()  # create list argument for external command execution
	list_args.append(env_vars['tools']['7zip'][os.name]['path'])  # insert executable path
	temp_args = env_vars['tools']['7zip'][os.name]['params_deflate'].split(' ')  # create table of raw command arguments
	for var in temp_args:  # parse table of raw command arguments
		# insert parsed param
		list_args.append(var.replace('%input%', src).replace('%output%', dest))
	print(list_args)
	return subprocess.check_output(list_args, universal_newlines=True)  # execute the command


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


if __name__ == "__main__":
	print(sys.argv)
	print(env_vars)
	lang = Lang()
	app = QtWidgets.QApplication(sys.argv)
	
	dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
	app_icon = QtGui.QIcon()
	app_icon.addFile(dir + '/icons/app_icon16x16.png', QtCore.QSize(16, 16))
	app_icon.addFile(dir + '/icons/app_24x24.png', QtCore.QSize(24, 24))
	app_icon.addFile(dir + '/icons/app_32x32.png', QtCore.QSize(32, 32))
	app_icon.addFile(dir + '/icons/app_48x48.png', QtCore.QSize(48, 48))
	app_icon.addFile(dir + '/icons/app_256x256.png', QtCore.QSize(256, 256))
	app.setWindowIcon(app_icon)
	if os.name == 'nt':
		myappid = 'lordkbx.ebook_collection.reader'
		ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
	
	ReaderWindow = QtWidgets.QWidget()
	ui = Ui_ReaderWindow()
	ui.setupUi(ReaderWindow)
	
	# Button FullScreen
	icon1 = QtGui.QIcon()
	icon1.addPixmap(QtGui.QPixmap("../icons/white/full_screen.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
	ui.buttonFullScreen.setIcon(icon1)
	ui.buttonFullScreen.clicked.connect(toogleFullScreen)

	# Button Content Table
	icon2 = QtGui.QIcon()
	icon2.addPixmap(QtGui.QPixmap("../icons/white/content_table.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
	ui.buttonContentTable.setIcon(icon2)
	ui.buttonContentTable.clicked.connect(DisplayTreeContentTable)
	ui.treeContentTable.setMinimumWidth(180)
	ui.treeContentTable.setMaximumWidth(180)

	# Button Info
	icon3 = QtGui.QIcon()
	icon3.addPixmap(QtGui.QPixmap("../icons/white/info.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
	ui.buttonInfo.setIcon(icon3)
	# ui.buttonInfo.clicked.connect(DisplayTreeContentTable)

	# Processing Content Table
	ui.treeContentTable.clear()
	ui.treeContentTable.headerItem().setText(0, lang['Reader']['ContentTableHeader'])
	ui.treeContentTable.currentItemChanged.connect(ContentTableCurrentItemChanged)

	if len(sys.argv) < 2:
		WarnDialog(lang['Reader']['DialogInfoNoFileWindowTitle'], lang['Reader']['DialogInfoNoFileWindowText'], ReaderWindow)
		exit(0)
	ReaderWindow.show()
	file = sys.argv[1]
	filepath, ext = os.path.splitext(file)
	destDir = appDir + '/reader/tmp'
	rmDir(destDir)
	if os.path.isdir(destDir) is not True: os.mkdir(destDir)
	page = 'file:///C:/Users/KevBo/wuxiaworld_export_ebook/tmp/toc.xhtml'

	appMode = QwwMode.CBZ
	if ext in ['.epub', '.epub2', '.epub3']:
		ret = deflate(file, destDir)
		print(ret)
		appMode = QwwMode.EPUB
	elif ext in ['.cbz', '.cbr']:
		appMode = QwwMode.CBZ
		ret = deflate(file, destDir)
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
	else:
		WarnDialog(lang['Reader']['DialogInfoBadFileWindowTitle'], lang['Reader']['DialogInfoBadFileWindowText'], ReaderWindow)
		exit(0)

	ui.webView.setMode(appMode)
	ui.webView.setUrl(QtCore.QUrl(page))
	tmpcss = destDir + "/tmp.css"
	filePage = open(tmpcss, "w", encoding="utf8")
	filePage.write("body { -webkit-user-select: none; }")
	filePage.close()
	ui.webView.page().settings().setUserStyleSheetUrl(QtCore.QUrl.fromLocalFile(tmpcss))
	ui.webView.page().mainFrame().setScrollBarPolicy(QtCore.Qt.Vertical, QtCore.Qt.ScrollBarAlwaysOff)
	ui.webView.setContextMenuPolicy(QtCore.Qt.NoContextMenu)

	app.exec_()
	rmDir(destDir)
	sys.exit(0)
