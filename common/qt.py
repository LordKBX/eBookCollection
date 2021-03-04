import os, sys
import enum

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
from common.vars import *


class QtQIconEnum(enum.Enum):
    folder = env_vars['styles']['Dark']['icons']['folder']
    file = env_vars['styles']['Dark']['icons']['file']
    lock = env_vars['styles']['Dark']['icons']['lock']
    unlock = env_vars['styles']['Dark']['icons']['unlock']


def setQTreeItemIcon(item: QtWidgets.QTreeWidgetItem, icon_ref: QtQIconEnum = QtQIconEnum.folder):
    icon = QtGui.QIcon()
    image = QtGui.QPixmap()
    image.load(icon_ref.value)
    icon.addPixmap(image, QtGui.QIcon.Normal, QtGui.QIcon.Off)
    item.setIcon(0, icon)


def setQTreeItemFolderIcon(item: QtWidgets.QTreeWidgetItem):
    setQTreeItemIcon(item, QtQIconEnum.folder)


def setQTreeItemLockIcon(item: QtWidgets.QTreeWidgetItem):
    setQTreeItemIcon(item, QtQIconEnum.lock)

