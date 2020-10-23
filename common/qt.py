import os, sys
from PyQt5 import QtCore, QtGui, QtWidgets
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
from vars import *


def setQTreeItemFolderIcon(item: QtWidgets.QTreeWidgetItem):
    icon = QtGui.QIcon()
    image = QtGui.QPixmap()
    image.load(env_vars['styles']['black']['icons']['folder'])
    icon.addPixmap(image, QtGui.QIcon.Normal, QtGui.QIcon.Off)
    item.setIcon(0, icon)

