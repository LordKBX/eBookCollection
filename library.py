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

import home
from common.bdd import *
from common.lang import *
from Sync import server

if __name__ == "__main__":
    app = PyQt5.QtWidgets.QApplication([])
    app_icon = PyQt5.QtGui.QIcon()

    bdd = BDD()
    translation = Lang()
    server = server.Server(
        bdd.get_param('sync/ip'),
        int(float(bdd.get_param('sync/port'))),
        bdd.get_param('sync/user'),
        bdd.get_param('sync/password'),
        bdd
    )

    for icon_index in app_icons:
        icon_size = int(float(icon_index.replace('x', '')))
        app_icon.addFile(app_directory + os.sep + app_icons[icon_index], QtCore.QSize(icon_size, icon_size))

    app.setWindowIcon(app_icon)
    if os.name == 'nt':
        myappid = app_id + '.library'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    Home = home.HomeWindow(bdd, translation, sys.argv, env_vars)
    Home.show()
    ret = 0
    try:
        ret = app.exec_()
        server.Close()
    except Exception as err:
        traceback.print_exc()
    print("The End")
    sys.exit(ret)
