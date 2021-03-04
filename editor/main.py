import os
import sys
if os.name == 'nt':
	import ctypes
	import win32gui, win32con

from PyQt5.uic import *

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from editor.window import *
from common.dialog import *
from common.archive import *
from common import lang

ui = None


def eventHandler(event: dict):
	global previousEvent, ui
	print(event)


if __name__ == "__main__":
	lng = lang.Lang()

	previousEvent = ''
	app = QtWidgets.QApplication(sys.argv)
	print(sys.argv)
	bdd = BDD()

	app_icon = QtGui.QIcon()
	app_icon.addFile(app_directory + '/ressources/icons/app_icon16x16.png', QtCore.QSize(16, 16))
	app_icon.addFile(app_directory + '/ressources/icons/app_icon24x24.png', QtCore.QSize(24, 24))
	app_icon.addFile(app_directory + '/ressources/icons/app_icon32x32.png', QtCore.QSize(32, 32))
	app_icon.addFile(app_directory + '/ressources/icons/app_icon48x48.png', QtCore.QSize(48, 48))
	app_icon.addFile(app_directory + '/ressources/icons/app_icon256x256.png', QtCore.QSize(256, 256))
	app.setWindowIcon(app_icon)
	if os.name == 'nt':
		myappid = 'lordkbx.ebook_collection.editor'
		ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
		if 'debug' not in sys.argv:
			the_program_to_hide = win32gui.GetForegroundWindow()
			win32gui.ShowWindow(the_program_to_hide, win32con.SW_HIDE)
	try:
		file = ''
		for index in range(1, len(sys.argv)):
			if sys.argv[index] != 'debug':
				file = sys.argv[index]

		if len(sys.argv) < 2:
			WarnDialog(lng['Editor']['DialogInfoNoFileWindowTitle'], lng['Editor']['DialogInfoNoFileWindowText'], ui)
			exit(0)

		ui = EditorWindow(None, file, lng, bdd)
		ui.show()

		# données de test
		# ui.tabWidget.create_pane("metadata.opf", app_directory + os.sep + 'editor' + os.sep + 'tmp' + os.sep + 'current' + os.sep + 'metadata.opf')

		app.exec_()
		# rmDir(destDir)  # disable for debug purpose
	except Exception:
		traceback.print_exc()
	sys.exit(0)
