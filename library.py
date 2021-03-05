# This Python file uses the following encoding: utf-8
import os
if os.name == 'nt':
    import ctypes
    import win32gui, win32con

import PyQt5.QtCore
import PyQt5.QtGui
import PyQt5.QtWidgets
import home
from common.vars import *
from common.bdd import *
from common.lang import *

if __name__ == "__main__":
    bdd = BDD()
    translation = Lang()

    app = PyQt5.QtWidgets.QApplication([])
    app_icon = PyQt5.QtGui.QIcon()
    app_icon.addFile(app_directory + '/ressources/icons/app_icon16x16.png', QtCore.QSize(16, 16))
    app_icon.addFile(app_directory + '/ressources/icons/app_icon24x24.png', QtCore.QSize(24, 24))
    app_icon.addFile(app_directory + '/ressources/icons/app_icon32x32.png', QtCore.QSize(32, 32))
    app_icon.addFile(app_directory + '/ressources/icons/app_icon48x48.png', QtCore.QSize(48, 48))
    app_icon.addFile(app_directory + '/ressources/icons/app_icon256x256.png', QtCore.QSize(256, 256))
    app.setWindowIcon(app_icon)
    if os.name == 'nt':
        myappid = 'lordkbx.ebook_collection'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        if 'debug' not in sys.argv:
            the_program_to_hide = win32gui.GetForegroundWindow()
            win32gui.ShowWindow(the_program_to_hide, win32con.SW_HIDE)

    Home = home.HomeWindow(bdd, translation, sys.argv)
    Home.show()
    sys.exit(app.exec_())
