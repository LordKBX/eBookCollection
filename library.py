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
import asyncio
import os
import sys
from threading import Thread

if os.name == 'nt':
    import ctypes

import home
from common.bdd import *
from common.lang import *
from common.dialog import *
import Sync.server


def myexcepthook(type, value, tb):
    print("HAHA!")
    print(value)


if __name__ == "__main__":
    sys.excepthook = myexcepthook
    app = PyQt5.QtWidgets.QApplication([])
    app_icon = PyQt5.QtGui.QIcon()

    bdd = BDD()
    translation = Lang()
    srv = Sync.server.Server(
        bdd.get_param('sync/ip'),
        int(float(bdd.get_param('sync/port'))),
        bdd.get_param('sync/user'),
        bdd.get_param('sync/password'),
        bdd
    )
    thread = Thread(target=srv.Run, args=())
    thread.daemon = True
    thread.start()

    for icon_index in app_icons:
        icon_size = int(float(icon_index.replace('x', '')))
        app_icon.addFile(app_directory + os.sep + app_icons[icon_index], QtCore.QSize(icon_size, icon_size))

    app.setWindowIcon(app_icon)
    if os.name == 'nt':
        myappid = app_id + '.library'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    Home = home.HomeWindow(bdd, translation, sys.argv, env_vars)
    # ret = Home.exec_()

    try:
        Home.show()  # Show the GUI
        Home.info_block.setMinimumHeight(150)
        Home.sorting_block.setMinimumHeight(150)

        if Home.tools['archiver']['path'] is None:
            WarnDialog(Home.lang['Global/ArchiverErrorTitle'], Home.lang['Global/ArchiverErrorText'])
            Home.header_block_btn_settings_clicked()
        if "settings" in Home.argv:
            Home.header_block_btn_settings_clicked()
            Home.close()
        if "metadata" in Home.argv:
            Home.metadata_window_load()
            Home.close()
    except Exception:
        traceback.print_exc()

    ret = 0
    try:
        ret = app.exec_()
        srv.Close()
    except Exception as err:
        traceback.print_exc()
    print("The End")
    sys.exit(ret)
