import os
import sys
if os.name == 'nt':
	import ctypes
	import win32gui, win32con

import PyQt5.QtGui
import PyQt5.QtCore
from PyQt5.uic import *
from window import *

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from common.dialog import *
from common.archive import *
from common import lang

if __name__ == "__main__":
	lng = lang.Lang()

	previousEvent = ''
	app = QtWidgets.QApplication(sys.argv)
	print(sys.argv)
	bdd = BDD()

	app_icon = PyQt5.QtGui.QIcon()
	for icon_index in app_icons:
		icon_size = int(float(icon_index.replace('x', '')))
		app_icon.addFile(app_directory + os.sep + app_icons[icon_index], QtCore.QSize(icon_size, icon_size))

	app.setWindowIcon(app_icon)
	if os.name == 'nt':
		myappid = app_id + '.editor'
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
			WarnDialog(lng['Editor']['DialogInfoNoFileWindowTitle'], lng['Editor']['DialogInfoNoFileWindowText'], None)
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
