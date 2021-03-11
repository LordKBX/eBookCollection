import os
import sys
import traceback
if os.name == 'nt':
	import ctypes

import PyQt5.uic
from PyQt5.uic import *
from PyQt5 import QtWebKitWidgets
from PyQt5 import QtCore

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from common import lang
from common.vars import *
from common.dialog import *
from common.books import *
from common.archive import *
from CustomQWebView import *


class ReaderWindow(QtWidgets.QMainWindow):
	previousEvent = ''
	isEpub = False

	def __init__(self, parent: QtWidgets.QMainWindow, bdd):
		super(ReaderWindow, self).__init__(parent)

		if hasattr(sys, 'frozen'):
			basis = sys.executable
		else:
			basis = sys.argv[0]
		baseDir = os.path.split(basis)[0]

		PyQt5.uic.loadUi(baseDir + os.sep + "reader.ui", self)
		self.BDD = bdd
		self.style = self.BDD.get_param('style')
		self.translation = lang.Lang()
		self.translation.set_lang(self.BDD.get_param('lang'))

		# load window size
		size_tx = self.BDD.get_param('reader/windowSize')
		if size_tx is not None and size_tx != '':
			size = eval(size_tx)
			self.resize(size[0], size[1])
		# load window position
		pos_tx = self.BDD.get_param('reader/windowPos')
		if pos_tx is not None and pos_tx != '':
			pos = eval(pos_tx)
			self.move(pos[0], pos[1])
			self.pos()

		QDockStyle = get_style_var(self.style, 'QDockWidget')
		if baseDir.endswith('/reader') is False: QDockStyle = QDockStyle.replace('../', './')
		self.setStyleSheet(get_style_var(self.style, 'QMainWindow') + QDockStyle)

		self.hide_info_text_browser()

		self.show()

	def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
		size = self.size()
		tx = [size.width(), size.height()].__str__()
		self.BDD.set_param('reader/windowSize', tx)

	def moveEvent(self, a0: QtGui.QMoveEvent) -> None:
		pos = self.pos()
		tx = [pos.x(), pos.y()].__str__()
		self.BDD.set_param('reader/windowPos', tx)

	def toogle_full_screen(self):
		icon_1 = QtGui.QIcon()
		if self.isFullScreen() is True:
			self.showNormal()
			icon_1.addPixmap(QtGui.QPixmap(get_style_var(app_style, 'icons/full_screen')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		else:
			self.showFullScreen()
			icon_1.addPixmap(QtGui.QPixmap(get_style_var(app_style, 'icons/normal_screen')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.buttonFullScreen.setIcon(icon_1)

	def display_tree_content_table(self):
		self.dockWidgetContentTable.setVisible(True)

	def display_info_text_browser(self):
		self.dockWidgetInfo.setVisible(True)

	def hide_tree_content_table(self):
		self.dockWidgetContentTable.setVisible(False)

	def hide_info_text_browser(self):
		self.dockWidgetInfo.setVisible(False)

	def content_table_current_item_changed(self, current: QtWidgets.QTreeWidgetItem, previous: QtWidgets.QTreeWidgetItem):
		try:
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
					page_url2 = 'file:///' + page_url.replace("\\", '/')

					# New
					fdata =''
					with open(page_url, 'rt', encoding='utf8') as pfile:
						fdata = pfile.read()
					last_slash = -1
					try: last_slash = td[1].rindex('/')
					except Exception: ""
					file_dir = destDir.replace(os.sep, '/') + '/' + td[1][0:last_slash]
					txe = fdata\
						.replace('<head>', '<head><base href="file:///' + destDir.replace(os.sep, '/') + '">')\
						.replace('="/', '="file:///' + destDir.replace(os.sep, '/') + '/')\
						.replace('="../', '="file:///' + file_dir + '/../')
					self.webView.page().currentFrame().setHtml(txe)

					# OLD
					# self.webView.setUrl(QtCore.QUrl(page_url2))
		except Exception:
			traceback.print_exc()

	def event_handler(self, event: dir):
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
			
	def set_context_menu(self):
		try:
			menu = QtWidgets.QMenu()
			if self.dockWidgetInfo.isVisible() is False:
				action0 = QtWidgets.QAction(self.translation['Reader/ContextMenuInfo'], None)
				action0.triggered.connect(lambda: self.display_info_text_browser())
				menu.addAction(action0)

			if self.dockWidgetContentTable.isVisible() is False:
				action1 = QtWidgets.QAction(self.translation['Reader/ContextMenuCT'], None)
				action1.triggered.connect(lambda: self.display_tree_content_table())
				menu.addAction(action1)
			if self.isEpub is True:
				if len(menu.actions()) > 0:
					menu.addSeparator()
				action2 = QtWidgets.QAction(self.translation['Reader/ContextMenuCopyText'], None)
				action2.triggered.connect(lambda: self.copy_data_to_clipboard())
				menu.addAction(action2)
				action3 = QtWidgets.QAction(self.translation['Reader/ContextMenuCopyHTML'], None)
				action3.triggered.connect(lambda: self.copy_data_to_clipboard(False))
				menu.addAction(action3)
			if len(menu.actions()) > 0:
				menu.exec(PyQt5.QtGui.QCursor.pos())

		except Exception:
			traceback.print_exc()

	def copy_data_to_clipboard(self, text: bool = True):
		cb = QtWidgets.QApplication.clipboard()
		if text is True:
			text = self.webView.page().mainFrame().page().selectedText()
			cb.setText(text, mode=cb.Clipboard)
		else:
			html = self.webView.page().mainFrame().page().selectedHtml()
			cb.setText(html, mode=cb.Clipboard)

	def set_info_text(self, file_path) -> bool:
		file_path = file_path.replace('./', app_directory).replace('/', os.sep)
		if os.path.isfile(file_path) is False:
			return False
		data = self.BDD.get_books(search="file:" + file_path)
		if len(data) > 0:
			infoData = self.translation['Reader/InfoBlockText']\
				.replace('{FILE}', file_path)\
				.replace('{TITLE}', data[0]['title'])\
				.replace('{SERIES}', data[0]['series'])\
				.replace('{AUTHORS}', data[0]['authors'])\
				.replace('{FORMAT}', data[0]['files'][0]['format'])\
				.replace('{SIZE}', data[0]['files'][0]['size'])
			self.infoTextBrowser.setText(infoData)
			return True
		else:
			filepath, ext = os.path.splitext(file_path)
			if ext in ['.epub', '.epub2', '.epub3']:
				self.isEpub = True
				bookData = get_epub_info(file_path, True)
				title = series = authors = ''
				if bookData['title'] is not None and bookData['title'].startswith('??<') is False:
					title = bookData['title']
				if bookData['series'] is not None and bookData['series'].startswith('??<') is False:
					series = bookData['series']
				if bookData['authors'] is not None and bookData['authors'].startswith('??<') is False:
					authors = bookData['authors']
				infoData = self.translation['Reader/InfoBlockText']\
					.replace('{FILE}', file_path)\
					.replace('{TITLE}', title)\
					.replace('{SERIES}', series)\
					.replace('{AUTHORS}', authors)\
					.replace('{FORMAT}', ext[1:].upper())\
					.replace('{SIZE}', get_file_size(file_path))
				self.infoTextBrowser.setText(infoData)
				return True
			else:
				infoData = self.translation['Reader/InfoBlockText']\
					.replace('{FILE}', file_path)\
					.replace('{TITLE}', '')\
					.replace('{SERIES}', '')\
					.replace('{AUTHORS}', '')\
					.replace('{FORMAT}', ext[1:].upper())\
					.replace('{SIZE}', get_file_size(file_path))
				self.infoTextBrowser.setText(infoData)
		return False


if __name__ == "__main__":
	bdd = BDD()
	translation = lang.Lang()
	translation.set_lang(bdd.get_param('lang'))
	app_style = bdd.get_param('style')
	if app_style is None or app_style == '':
		app_style = 'Dark'
	if env_vars['tools']['archiver']['path'] is None:
		WarnDialog(translation['Global/ArchiverErrorTitle'], translation['Global/ArchiverErrorText'])
		sys.exit(0)

	app = QtWidgets.QApplication([])
	app_icon = PyQt5.QtGui.QIcon()
	for icon_index in app_icons:
		icon_size = int(float(icon_index.replace('x', '')))
		app_icon.addFile(app_directory + os.sep + app_icons[icon_index], QtCore.QSize(icon_size, icon_size))

	app.setWindowIcon(app_icon)
	if os.name == 'nt':
		myappid = app_id + '.reader'
		ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

	ui = ReaderWindow(None, bdd)
	ui.show()

	# Processing Content Table
	ui.treeContentTable.clear()
	ui.treeContentTable.currentItemChanged.connect(ui.content_table_current_item_changed)
	ui.treeContentTable.setIndentation(0)
	ui.treeContentTable.setCursor(QtCore.Qt.PointingHandCursor)

	ui.dockWidgetContentTable.setWindowTitle(translation['Reader/ContentTableHeader'])
	ui.dockWidgetInfo.setWindowTitle(translation['Reader/InfoBlockHeader'])

	if len(sys.argv) < 2:
		WarnDialog(translation['Reader/DialogInfoNoFileWindowTitle'], translation['Reader/DialogInfoNoFileWindowText'], ui)
		exit(0)

	file = ''
	for index in range(1, len(sys.argv)):
		if sys.argv[index] != 'debug':
			file = sys.argv[index]

	to_hide_dir = app_directory.replace(os.sep, '/') + '/data/'
	filepath, ext = os.path.splitext(file)
	ui.setWindowTitle(
		translation['Reader/WindowTitle'] + ' - ' + file.replace(os.sep, '/')
		.replace(to_hide_dir, '').replace('/', ' / ').replace(ext, '')
	)
	destDir = app_user_directory + os.sep + 'reader' + os.sep + 'tmp'
	try: rmDir(destDir)
	except Exception: ""
	if os.path.isdir(destDir) is not True: os.makedirs(destDir)
	page = ''
	infoData = ''
	print(file.replace('./', app_directory))
	file = file.replace('./', app_directory)

	ui.set_info_text(file)

	appMode = QwwMode.CBZ
	if ext in ['.epub', '.epub2', '.epub3']:
		ui.isEpub = True
		appMode = QwwMode.EPUB
		bookData = get_epub_info(file, True)
		winTitle = translation['Reader/WindowTitle'] + ' - '
		first = True
		for index in ['authors', 'series', 'title']:
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
		imgList = list_directory(destDir, 'jpg|jpeg|png')
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
		item.setText(0, translation['Reader/ContentTableTxtCover'])
		item.setData(0, 99, "cover")
		ui.treeContentTable.insertTopLevelItem(0, item)

		i = 1
		max_pages = len(imgList)
		while i < max_pages - 1:
			item = QtWidgets.QTreeWidgetItem(ui.treeContentTable)
			item.setText(0, translation['Reader/ContentTableTxtPageX'].format(i))
			item.setData(0, 99, "page:{}".format(i))
			ui.treeContentTable.insertTopLevelItem(0, item)
			i += 1

		item = QtWidgets.QTreeWidgetItem(ui.treeContentTable)
		item.setText(0, translation['Reader/ContentTableTxtEnd'])
		item.setData(0, 99, "end")
		ui.treeContentTable.insertTopLevelItem(0, item)
		ui.treeContentTable.setCurrentItem(ui.treeContentTable.topLevelItem(0), 0)
	else:
		WarnDialog(
			translation['Reader/DialogInfoBadFileWindowTitle'],
			translation['Reader/DialogInfoBadFileWindowText'],
			ui
		)
		exit(0)

	ui.webView.setMode(appMode)
	ui.webView.setEventHandler(ui.event_handler)
	ui.webView.setUrl(QtCore.QUrl(page))

	ui.webView.page().mainFrame().setScrollBarPolicy(QtCore.Qt.Vertical, QtCore.Qt.ScrollBarAlwaysOff)
	ui.webView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
	ui.webView.customContextMenuRequested.connect(ui.set_context_menu)

	# tmp_css = destDir + "/tmp.css"
	# file_page = open(tmp_css, "w", encoding="utf8")
	# file_page.write("body { -webkit-user-select: none; }")
	# file_page.close()
	# ui.webView.page().settings().setUserStyleSheetUrl(QtCore.QUrl.fromLocalFile(tmpcss))
	app.exec_()
	rmDir(destDir)
	sys.exit(0)
