import os, sys
import enum

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
from common.vars import *


class QtQIconEnum(enum.Enum):
    folder = env_vars['styles']['Dark']['icons']['folder']
    file = env_vars['styles']['Dark']['icons']['file']
    lock = env_vars['styles']['Dark']['icons']['lock']
    unlock = env_vars['styles']['Dark']['icons']['unlock']


def setQTreeItemIcon(item: QtWidgets.QTreeWidgetItem, icon_ref: str = QtQIconEnum.folder.value):
    icon = QtGui.QIcon()
    image = QtGui.QPixmap()
    image.load(icon_ref)
    icon.addPixmap(image, QtGui.QIcon.Normal, QtGui.QIcon.Off)
    item.setIcon(0, icon)


def setQTreeItemFileIcon(item: QtWidgets.QTreeWidgetItem, style='Dark'):
    setQTreeItemIcon(item, get_style_var(style, 'icons/file'))


def setQTreeItemFolderIcon(item: QtWidgets.QTreeWidgetItem, style='Dark'):
    setQTreeItemIcon(item, get_style_var(style, 'icons/folder'))


def setQTreeItemLockIcon(item: QtWidgets.QTreeWidgetItem, style='Dark'):
    setQTreeItemIcon(item, get_style_var(style, 'icons/lock'))

