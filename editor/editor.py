import os
import sys
if os.name == 'nt':
	import ctypes

import PyQt5.QtGui
import PyQt5.QtCore
from PyQt5.uic import *

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from common.dialog import *
from common.archive import *
from common import lang
from editor.window import *

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
