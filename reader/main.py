import os
import sys
if os.name == 'nt':
	import ctypes

from PyQt5 import QtCore, QtGui, QtWidgets, QtWebKitWidgets
from reader_ui import *

if __name__ == "__main__":
	import sys
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
	ReaderWindow.show()
	
	ui.webView.setUrl(QtCore.QUrl("file:///C:/Users/KevBo/wuxiaworld_export_ebook/tmp/toc.xhtml"))
	
	sys.exit(app.exec_())
