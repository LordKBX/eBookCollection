import os
import sys
if os.name == 'nt':
	import ctypes

import PyQt5.uic
from PyQt5.uic import *

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from vars import *
import lang
from bdd import *
from common.dialog import *
from common.books import *
from common.archive import *
from reader.CustomQWebView import *

ui = None


class ReaderWindow(QtWidgets.QMainWindow):
	previousEvent = ''

	def __init__(self, parent: QtWidgets.QMainWindow):
		super(ReaderWindow, self).__init__(parent)
		PyQt5.uic.loadUi(app_directory + '/reader/reader2.ui'.replace('/', os.sep), self)
		self.show()

	def toogle_full_screen(self):
		icon_1 = QtGui.QIcon()
		if self.isFullScreen() is True:
			self.showNormal()
			icon_1.addPixmap(QtGui.QPixmap("../ressources/icons/white/full_screen.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		else:
			self.showFullScreen()
			icon_1.addPixmap(QtGui.QPixmap("../ressources/icons/white/normal_screen.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.buttonFullScreen.setIcon(icon_1)

	def display_tree_content_table(self):
		size_int = 0
		if self.buttonContentTable.isChecked():
			size_int = 180
		self.treeContentTable.setMinimumWidth(size_int)
		self.treeContentTable.setMaximumWidth(size_int)

	def content_table_current_item_changed(self, current: QtWidgets.QTreeWidgetItem, previous: QtWidgets.QTreeWidgetItem):
		data = current.data(0, 99)
		if appMode.value == QwwMode.CBZ.value:
			if data == 'cover':
				self.webView.updatePositionCbzStart()
			elif data == 'end':
				self.webView.updatePositionCbzEnd()
			elif re.search('^page:', data) is not None:
				td = data.split(':')
				self.webView.updatePositionCbzByPage(int(float(td[1])))
		elif appMode.value == QwwMode.EPUB.value:
			if re.search('^chapter:', data) is not None:
				td = data.split(':')
				page_url = destDir + "/" + td[1]
				page_url = 'file:///' + page_url.replace("\\", '/')
				self.webView.setUrl(QtCore.QUrl(page_url))

	def event_andler(self, event: dir):
		try:
			evt = '{}'.format(event)
			if event['type'] == 'pageChange':
				if self.webView.mode.value == QwwMode.CBZ.value:
					self.treeContentTable.setCurrentItem(self.treeContentTable.topLevelItem(event['index']), 0)
			if evt == self.previousEvent:
				if event['type'] == 'chapterChange':
					if self.webView.mode.value == QwwMode.EPUB.value:
						local_index = 0
						try:
							local_index = self.treeContentTable.currentIndex().row()
						except Exception:
							""
						if event['value'] == 'prev':
							if local_index - 1 >= 0:
								self.treeContentTable.setCurrentItem(self.treeContentTable.topLevelItem(local_index - 1), 0)
								timer = QtCore.QTimer()
								timer.singleShot(100, self.webView.updatePositionCbzEnd)
						if event['value'] == 'next':
							if local_index + 1 < self.treeContentTable.topLevelItemCount():
								self.treeContentTable.setCurrentItem(self.treeContentTable.topLevelItem(local_index + 1), 0)
			self.previousEvent = evt
		except Exception:
			traceback.print_exc()


if __name__ == "__main__":
	translation = lang.Lang()
	bdd = BDD()

	app = QtWidgets.QApplication([])
	app_icon = QtGui.QIcon()
	app_icon.addFile(app_directory + '/ressources/icons/app_icon16x16.png'.replace('/', os.sep), QtCore.QSize(16, 16))
	app_icon.addFile(app_directory + '/ressources/icons/app_icon24x24.png'.replace('/', os.sep), QtCore.QSize(24, 24))
	app_icon.addFile(app_directory + '/ressources/icons/app_icon32x32.png'.replace('/', os.sep), QtCore.QSize(32, 32))
	app_icon.addFile(app_directory + '/ressources/icons/app_icon48x48.png'.replace('/', os.sep), QtCore.QSize(48, 48))
	app_icon.addFile(app_directory + '/ressources/icons/app_icon256x256.png'.replace('/', os.sep), QtCore.QSize(256, 256))
	app.setWindowIcon(app_icon)
	if os.name == 'nt':
		myappid = 'lordkbx.ebook_collection.reader'
		ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

	ui = ReaderWindow(None)
	ui.show()

	# Button FullScreen
	icon1 = QtGui.QIcon()
	icon1.addPixmap(QtGui.QPixmap(app_directory + "/ressources/icons/white/full_screen.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
	ui.buttonFullScreen.setIcon(icon1)
	ui.buttonFullScreen.clicked.connect(ui.toogle_full_screen)

	# Button Content Table
	icon2 = QtGui.QIcon()
	icon2.addPixmap(QtGui.QPixmap(app_directory + "/ressources/icons/white/content_table.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
	ui.buttonContentTable.setIcon(icon2)
	ui.buttonContentTable.clicked.connect(ui.display_tree_content_table)
	ui.treeContentTable.setMinimumWidth(180)
	ui.treeContentTable.setMaximumWidth(180)

	# Button Info
	icon3 = QtGui.QIcon()
	icon3.addPixmap(QtGui.QPixmap(app_directory + "/ressources/icons/white/info.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
	ui.buttonInfo.setIcon(icon3)
	# ui.buttonInfo.clicked.connect(ui.display_tree_content_table)

	# Processing Content Table
	ui.treeContentTable.clear()
	ui.treeContentTable.headerItem().setText(0, translation['Reader']['ContentTableHeader'])
	ui.treeContentTable.currentItemChanged.connect(ui.content_table_current_item_changed)
	ui.treeContentTable.setIndentation(0)
	ui.treeContentTable.setCursor(QtCore.Qt.PointingHandCursor)

	if len(sys.argv) < 2:
		WarnDialog(translation['Reader']['DialogInfoNoFileWindowTitle'], translation['Reader']['DialogInfoNoFileWindowText'], ui)
		exit(0)

	file = sys.argv[1]

	to_hide_dir = app_directory.replace(os.sep, '/') + '/data/'
	filepath, ext = os.path.splitext(file)
	ui.setWindowTitle(
		translation['Reader']['WindowTitle'] + ' - ' + file.replace(os.sep, '/')
		.replace(to_hide_dir, '').replace('/', ' / ').replace(ext, '')
	)
	destDir = app_directory + '/reader/tmp'
	rmDir(destDir)
	if os.path.isdir(destDir) is not True: os.mkdir(destDir)
	page = ''

	appMode = QwwMode.CBZ
	if ext in ['.epub', '.epub2', '.epub3']:
		appMode = QwwMode.EPUB
		bookData = get_epub_info(file)
		winTitle = translation['Reader']['WindowTitle'] + ' - '
		first = True
		for index in ['authors', 'serie', 'title']:
			try:
				if bookData[index] is not None:
					if bookData[index].strip() != '':
						if first is False:
							winTitle += ' / '
						else: first = False
						winTitle += bookData[index]
			except Exception:
				""

		ui.setWindowTitle(winTitle)
		try:
			ret = inflate(file, destDir)
		except Exception:
			WarnDialog("Error", "File not found")

		page = destDir + "/" + bookData['chapters'][0]['src']
		page = 'file:///' + page.replace("\\", '/')
		i = 0
		max_chapters = len(bookData['chapters'])
		while i < max_chapters:
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
		file_page = open(page, "w", encoding="utf8")
		imgStyle = 'img{ max-width:100%; max-height:100%; display:block; margin: 0 auto; }'
		# imgStyle = 'img{ display:block; margin: 0 auto; }'

		file_page.write("\n".join([
			'<html xmlns="http://www.w3.org/1999/xhtml">',
			'<head>',
			'	<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>',
			'	<title>' + file + '</title>',
			'	<link href="common.css" rel="stylesheet" type="text/css"/>',
			'	<style>*{ margin:0; padding:0; border:0; } html, body, section, div{ height:100%; }' + imgStyle + '</style>',
			'</head>',
			'<body>',
			'	<section>'
		]))
		for img in imgList:
			file_page.write("\n\t\t<img src=\"" + 'file:///' + img.replace("\\", '/') + "\"/>")
		file_page.write("\n".join([
			'\n\t</section>',
			'	<script type="text/javascript">',
			'		function imgResize(){',
			'			height = window.innerHeight;',
			'			list = document.querySelectorAll(\'img\')',
			'			for(id in list){',
			'				list[id].style.height = "" + height + "px";',
			'			}',
			'		}',
			'		imgResize();',
			'	</script>',
			'</body>',
			'</html>'
		]))
		file_page.close()
		page = 'file:///' + page.replace("\\", '/')

		item = QtWidgets.QTreeWidgetItem(ui.treeContentTable)
		item.setText(0, translation['Reader']['ContentTableTxtCover'])
		item.setData(0, 99, "cover")
		ui.treeContentTable.insertTopLevelItem(0, item)

		i = 1
		max_pages = len(imgList)
		while i < max_pages - 1:
			item = QtWidgets.QTreeWidgetItem(ui.treeContentTable)
			item.setText(0, translation['Reader']['ContentTableTxtPageX'].format(i))
			item.setData(0, 99, "page:{}".format(i))
			ui.treeContentTable.insertTopLevelItem(0, item)
			i += 1

		item = QtWidgets.QTreeWidgetItem(ui.treeContentTable)
		item.setText(0, translation['Reader']['ContentTableTxtEnd'])
		item.setData(0, 99, "end")
		ui.treeContentTable.insertTopLevelItem(0, item)
		ui.treeContentTable.setCurrentItem(ui.treeContentTable.topLevelItem(0), 0)
	else:
		WarnDialog(
			translation['Reader']['DialogInfoBadFileWindowTitle'],
			translation['Reader']['DialogInfoBadFileWindowText'],
			ui
		)
		exit(0)

	ui.webView.setMode(appMode)
	ui.webView.setEventHandler(ui.event_andler)
	ui.webView.setUrl(QtCore.QUrl(page))
	tmp_css = destDir + "/tmp.css"
	file_page = open(tmp_css, "w", encoding="utf8")
	file_page.write("body { -webkit-user-select: none; }")
	file_page.close()
	# ui.webView.page().settings().setUserStyleSheetUrl(QtCore.QUrl.fromLocalFile(tmpcss))
	ui.webView.page().mainFrame().setScrollBarPolicy(QtCore.Qt.Vertical, QtCore.Qt.ScrollBarAlwaysOff)
	ui.webView.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
	app.exec_()
	rmDir(destDir)
	sys.exit(0)
