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


if __name__ == "__main__":
	lng = Lang()

	previousEvent = ''
	app = QtWidgets.QApplication(sys.argv)
	print(sys.argv)
	lang = Lang()
	bdd = BDD()

	app_icon = QtGui.QIcon()
	app_icon.addFile(app_directory + '/icons/app_icon16x16.png', QtCore.QSize(16, 16))
	app_icon.addFile(app_directory + '/icons/app_icon24x24.png', QtCore.QSize(24, 24))
	app_icon.addFile(app_directory + '/icons/app_icon32x32.png', QtCore.QSize(32, 32))
	app_icon.addFile(app_directory + '/icons/app_icon48x48.png', QtCore.QSize(48, 48))
	app_icon.addFile(app_directory + '/icons/app_icon256x256.png', QtCore.QSize(256, 256))
	app.setWindowIcon(app_icon)
	if os.name == 'nt':
		myappid = 'lordkbx.ebook_collection.editor'
		ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
	try:
		file = sys.argv[1]

		if len(sys.argv) < 2:
			WarnDialog(lang['Editor']['DialogInfoNoFileWindowTitle'], lang['Editor']['DialogInfoNoFileWindowText'], ui)
			exit(0)

		ui = EditorWindow(None, file)
		ui.show()

		# données de test
		# ui.tabWidget.create_pane("metadata.opf", app_directory + os.sep + 'editor' + os.sep + 'tmp' + os.sep + 'current' + os.sep + 'metadata.opf')

		app.exec_()
		# rmDir(destDir)  # disable for debug purpose
	except Exception:
		traceback.print_exc()
	sys.exit(0)
