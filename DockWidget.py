import traceback

import PyQt5.QtCore
import PyQt5.QtGui
from PyQt5.QtWidgets import QDockWidget

from common import bdd


class DockWidget(QDockWidget):
    BDD = None

    def __init__(self, name):
        super().__init__()

    def setBDD(self, database: bdd.BDD):
        self.BDD = database
        self.dockLocationChanged.connect(self.LocationChanged)

    def resizeEvent(self, event: PyQt5.QtGui.QResizeEvent):
        try:
            # print("docked item resized")
            self.update()
            self.BDD.set_param('library/BlockSize_'+self.objectName(), '[{},{}]'.format(event.size().width(), event.size().height()))
        except Exception as err:
            traceback.print_exc()

    def LocationChanged(self, area: PyQt5.QtCore.Qt.DockWidgetArea):
        try:
            print("dockLocationChanged")
            self.update()
            self.BDD.set_param('library/BlockArea_'+self.objectName(), area)
        except Exception as err:
            traceback.print_exc()
