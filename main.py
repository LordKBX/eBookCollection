# This Python file uses the following encoding: utf-8
import os
if os.name == 'nt':
    import ctypes
# sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
from bdd import *
from lang import *
from home.home import *

if __name__ == "__main__":
    bdd = BDD()
    translation = Lang()

    app = QApplication([])
    app_icon = QtGui.QIcon()
    app_icon.addFile(app_directory + '/icons/app_icon16x16.png', QtCore.QSize(16, 16))
    app_icon.addFile(app_directory + '/icons/app_icon24x24.png', QtCore.QSize(24, 24))
    app_icon.addFile(app_directory + '/icons/app_icon32x32.png', QtCore.QSize(32, 32))
    app_icon.addFile(app_directory + '/icons/app_icon48x48.png', QtCore.QSize(48, 48))
    app_icon.addFile(app_directory + '/icons/app_icon256x256.png', QtCore.QSize(256, 256))
    app.setWindowIcon(app_icon)
    if os.name == 'nt':
        myappid = 'lordkbx.ebook_collection'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    Home = HomeWindow(bdd, translation, sys.argv)
    Home.show()
    sys.exit(app.exec_())
