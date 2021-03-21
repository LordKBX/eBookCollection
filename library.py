# This Python file uses the following encoding: utf-8
#             _______                       __               ______             __  __                        __      __                     
#            /       \                     /  |             /      \           /  |/  |                      /  |    /  |                    
#    ______  $$$$$$$  |  ______    ______  $$ |   __       /$$$$$$  |  ______  $$ |$$ |  ______    _______  _$$ |_   $$/   ______   _______  
#   /      \ $$ |__$$ | /      \  /      \ $$ |  /  |      $$ |  $$/  /      \ $$ |$$ | /      \  /       |/ $$   |  /  | /      \ /       \ 
#  /$$$$$$  |$$    $$< /$$$$$$  |/$$$$$$  |$$ |_/$$/       $$ |      /$$$$$$  |$$ |$$ |/$$$$$$  |/$$$$$$$/ $$$$$$/   $$ |/$$$$$$  |$$$$$$$  |
#  $$    $$ |$$$$$$$  |$$ |  $$ |$$ |  $$ |$$   $$<        $$ |   __ $$ |  $$ |$$ |$$ |$$    $$ |$$ |        $$ | __ $$ |$$ |  $$ |$$ |  $$ |
#  $$$$$$$$/ $$ |__$$ |$$ \__$$ |$$ \__$$ |$$$$$$  \       $$ \__/  |$$ \__$$ |$$ |$$ |$$$$$$$$/ $$ \_____   $$ |/  |$$ |$$ \__$$ |$$ |  $$ |
#  $$       |$$    $$/ $$    $$/ $$    $$/ $$ | $$  |      $$    $$/ $$    $$/ $$ |$$ |$$       |$$       |  $$  $$/ $$ |$$    $$/ $$ |  $$ |
#   $$$$$$$/ $$$$$$$/   $$$$$$/   $$$$$$/  $$/   $$/        $$$$$$/   $$$$$$/  $$/ $$/  $$$$$$$/  $$$$$$$/    $$$$/  $$/  $$$$$$/  $$/   $$/ 
#                                                                                                                                            

import os, sys
if os.name == 'nt':
    import ctypes

import PyQt5.QtCore
import PyQt5.QtGui
import PyQt5.QtWidgets
import home
from common.vars import *
from common.bdd import *
from common.lang import *

if __name__ == "__main__":
    app = PyQt5.QtWidgets.QApplication([])
    app_icon = PyQt5.QtGui.QIcon()

    bdd = BDD()
    translation = Lang()

    for icon_index in app_icons:
        icon_size = int(float(icon_index.replace('x', '')))
        app_icon.addFile(app_directory + os.sep + app_icons[icon_index], QtCore.QSize(icon_size, icon_size))

    app.setWindowIcon(app_icon)
    if os.name == 'nt':
        myappid = app_id + '.library'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    Home = home.HomeWindow(bdd, translation, sys.argv, env_vars)
    Home.show()
    sys.exit(app.exec_())
