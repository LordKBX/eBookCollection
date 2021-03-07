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
    for icon_index in app_icons:
        icon_size = int(float(icon_index.replace('x', '')))
        app_icon.addFile(app_directory + os.sep + app_icons[icon_index], QtCore.QSize(icon_size, icon_size))

    app.setWindowIcon(app_icon)
    if os.name == 'nt':
        myappid = app_id + '.library'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        if 'debug' not in sys.argv:
            the_program_to_hide = win32gui.GetForegroundWindow()
            win32gui.ShowWindow(the_program_to_hide, win32con.SW_HIDE)

    Home = home.HomeWindow(bdd, translation, sys.argv, env_vars)
    Home.show()
    sys.exit(app.exec_())
