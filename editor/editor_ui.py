# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\CODES\Python\EbookCollection\editor\editor.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(QtWidgets.QMainWindow):
    def setupUi(self, MainWindow: QtWidgets.QMainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(930, 600)
        MainWindow.setMinimumSize(QtCore.QSize(900, 400))
        MainWindow.setStyleSheet("QWidget{\n"
" background: rgba(63, 63, 63);\n"
"color:white;\n"
"}\n"
"QDockWidget {\n"
"    border: 0;\n"
"margin:0;\n"
"padding:0;\n"
"}\n"
"\n"
"QDockWidget::title {\n"
"    text-align: left; /* align the text to the left */\n"
"    background: #333333;\n"
"    padding-left: 5px;\n"
"}\n"
"\n"
"QPushButton{\n"
"    background:transparent;\n"
"}\n"
"QPushButton:hover{\n"
"    background-color:rgb(120, 120, 120);\n"
"}\n"
"QPushButton:pressed{\n"
"    background-color:rgb(120, 120, 120);\n"
"}\n"
"QPushButton:checked{\n"
"    background-color:rgb(150, 150, 150);\n"
"}")
        MainWindow.setDockOptions(QtWidgets.QMainWindow.AllowNestedDocks|QtWidgets.QMainWindow.AnimatedDocks)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setAutoFillBackground(False)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_4.setContentsMargins(1, 0, 1, 1)
        self.verticalLayout_4.setSpacing(1)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.voidLabel = QtWidgets.QLabel(self.centralwidget)
        self.voidLabel.setMinimumSize(QtCore.QSize(0, 40))
        self.voidLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.voidLabel.setWordWrap(True)
        self.voidLabel.setObjectName("voidLabel")
        self.verticalLayout_4.addWidget(self.voidLabel)
        self.tabWidget = EditorTabManager(self.centralwidget)
        self.tabWidget.setMinimumSize(QtCore.QSize(320, 0))
        self.tabWidget.setFocusPolicy(QtCore.Qt.TabFocus)
        self.tabWidget.setElideMode(QtCore.Qt.ElideNone)
        self.tabWidget.setUsesScrollButtons(True)
        self.tabWidget.setDocumentMode(True)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setMovable(True)
        self.tabWidget.setTabBarAutoHide(False)
        self.tabWidget.setObjectName("tabWidget")
        self.verticalLayout_4.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.dockFiles = QtWidgets.QDockWidget(MainWindow)
        self.dockFiles.setMinimumSize(QtCore.QSize(160, 89))
        self.dockFiles.setFeatures(QtWidgets.QDockWidget.DockWidgetMovable)
        self.dockFiles.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea|QtCore.Qt.RightDockWidgetArea)
        self.dockFiles.setWindowTitle("Explorateur de fichiers")
        self.dockFiles.setObjectName("dockFiles")
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.treeFileTable = QtWidgets.QTreeWidget(self.dockWidgetContents)
        self.treeFileTable.setStyleSheet("")
        self.treeFileTable.setDragEnabled(True)
        self.treeFileTable.setDragDropMode(QtWidgets.QAbstractItemView.DragOnly)
        self.treeFileTable.setObjectName("treeFileTable")
        self.treeFileTable.headerItem().setText(0, "1")
        item_0 = QtWidgets.QTreeWidgetItem(self.treeFileTable)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeFileTable)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeFileTable)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeFileTable)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        self.treeFileTable.header().setVisible(False)
        self.verticalLayout.addWidget(self.treeFileTable)
        self.dockFiles.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dockFiles)
        self.dockContentTable = QtWidgets.QDockWidget(MainWindow)
        self.dockContentTable.setMinimumSize(QtCore.QSize(160, 89))
        self.dockContentTable.setFeatures(QtWidgets.QDockWidget.DockWidgetMovable)
        self.dockContentTable.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea|QtCore.Qt.RightDockWidgetArea)
        self.dockContentTable.setWindowTitle("Table des matières")
        self.dockContentTable.setObjectName("dockContentTable")
        self.dockWidgetContents_2 = QtWidgets.QWidget()
        self.dockWidgetContents_2.setObjectName("dockWidgetContents_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.dockWidgetContents_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.treeContentTable = QtWidgets.QListWidget(self.dockWidgetContents_2)
        self.treeContentTable.setObjectName("treeContentTable")
        self.verticalLayout_2.addWidget(self.treeContentTable)
        self.dockContentTable.setWidget(self.dockWidgetContents_2)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dockContentTable)
        self.dockPreview = QtWidgets.QDockWidget(MainWindow)
        self.dockPreview.setFloating(False)
        self.dockPreview.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)
        self.dockPreview.setAllowedAreas(QtCore.Qt.RightDockWidgetArea)
        self.dockPreview.setWindowTitle("Aperçu")
        self.dockPreview.setObjectName("dockPreview")
        self.dockWidgetContents_3 = QtWidgets.QWidget()
        self.dockWidgetContents_3.setObjectName("dockWidgetContents_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.dockWidgetContents_3)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.webView = QtWebKitWidgets.QWebView(self.dockWidgetContents_3)
        self.webView.setMinimumSize(QtCore.QSize(300, 0))
        self.webView.setObjectName("webView")
        self.verticalLayout_3.addWidget(self.webView)
        self.dockPreview.setWidget(self.dockWidgetContents_3)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.dockPreview)
        self.dockTop = QtWidgets.QDockWidget(MainWindow)
        self.dockTop.setMinimumSize(QtCore.QSize(774, 79))
        self.dockTop.setMaximumSize(QtCore.QSize(524287, 100))
        self.dockTop.setFeatures(QtWidgets.QDockWidget.DockWidgetMovable)
        self.dockTop.setAllowedAreas(QtCore.Qt.BottomDockWidgetArea|QtCore.Qt.TopDockWidgetArea)
        self.dockTop.setWindowTitle("ToolBar")
        self.dockTop.setObjectName("dockTop")
        self.dockTopContents = QtWidgets.QWidget()
        self.dockTopContents.setObjectName("dockTopContents")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.dockTopContents)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.button_save = QtWidgets.QToolButton(self.dockTopContents)
        self.button_save.setMinimumSize(QtCore.QSize(130, 60))
        self.button_save.setMaximumSize(QtCore.QSize(130, 16777215))
        self.button_save.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_save.setText("Save Ebook")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../ressources/icons/white/save.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_save.setIcon(icon)
        self.button_save.setIconSize(QtCore.QSize(30, 30))
        self.button_save.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.button_save.setObjectName("button_save")
        self.horizontalLayout.addWidget(self.button_save)
        self.button_load_checkpoint = QtWidgets.QToolButton(self.dockTopContents)
        self.button_load_checkpoint.setMinimumSize(QtCore.QSize(130, 60))
        self.button_load_checkpoint.setMaximumSize(QtCore.QSize(130, 16777215))
        self.button_load_checkpoint.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_load_checkpoint.setText("Load session checkpoint")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("../ressources/icons/tmp/catalog.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_load_checkpoint.setIcon(icon1)
        self.button_load_checkpoint.setIconSize(QtCore.QSize(30, 30))
        self.button_load_checkpoint.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.button_load_checkpoint.setObjectName("button_load_checkpoint")
        self.horizontalLayout.addWidget(self.button_load_checkpoint)
        self.button_create_checkpoint = QtWidgets.QToolButton(self.dockTopContents)
        self.button_create_checkpoint.setMinimumSize(QtCore.QSize(130, 60))
        self.button_create_checkpoint.setMaximumSize(QtCore.QSize(130, 16777215))
        self.button_create_checkpoint.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_create_checkpoint.setText("Create session checkpoint")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("../ressources/icons/tmp/bookmarks.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_create_checkpoint.setIcon(icon2)
        self.button_create_checkpoint.setIconSize(QtCore.QSize(30, 30))
        self.button_create_checkpoint.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.button_create_checkpoint.setObjectName("button_create_checkpoint")
        self.horizontalLayout.addWidget(self.button_create_checkpoint)
        self.button_file_manager = QtWidgets.QToolButton(self.dockTopContents)
        self.button_file_manager.setMinimumSize(QtCore.QSize(130, 60))
        self.button_file_manager.setMaximumSize(QtCore.QSize(130, 16777215))
        self.button_file_manager.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_file_manager.setText("Files Managment")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("../ressources/icons/tmp/tb_folder.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_file_manager.setIcon(icon3)
        self.button_file_manager.setIconSize(QtCore.QSize(30, 30))
        self.button_file_manager.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.button_file_manager.setObjectName("button_file_manager")
        self.horizontalLayout.addWidget(self.button_file_manager)
        self.button_edit_content_table = QtWidgets.QToolButton(self.dockTopContents)
        self.button_edit_content_table.setMinimumSize(QtCore.QSize(130, 60))
        self.button_edit_content_table.setMaximumSize(QtCore.QSize(130, 16777215))
        self.button_edit_content_table.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_edit_content_table.setText("Edit Content Table")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("../ressources/icons/white/content_table.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_edit_content_table.setIcon(icon4)
        self.button_edit_content_table.setIconSize(QtCore.QSize(30, 30))
        self.button_edit_content_table.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.button_edit_content_table.setObjectName("button_edit_content_table")
        self.horizontalLayout.addWidget(self.button_edit_content_table)
        spacerItem = QtWidgets.QSpacerItem(737, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.dockTop.setWidget(self.dockTopContents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(4), self.dockTop)
        self.actionRe_test = QtWidgets.QAction(MainWindow)
        self.actionRe_test.setObjectName("actionRe_test")

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow: QtWidgets.QMainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.voidLabel.setText(_translate("MainWindow", "Mama Mia"))
        __sortingEnabled = self.treeFileTable.isSortingEnabled()
        self.treeFileTable.setSortingEnabled(False)
        self.treeFileTable.topLevelItem(0).setText(0, _translate("MainWindow", "aaa"))
        self.treeFileTable.topLevelItem(0).child(0).setText(0, _translate("MainWindow", "bbbb"))
        self.treeFileTable.topLevelItem(1).setText(0, _translate("MainWindow", "hhhh"))
        self.treeFileTable.topLevelItem(2).setText(0, _translate("MainWindow", "ljljl"))
        self.treeFileTable.topLevelItem(3).setText(0, _translate("MainWindow", "è_yohp"))
        self.treeFileTable.topLevelItem(3).child(0).setText(0, _translate("MainWindow", "uohohoh"))
        self.treeFileTable.setSortingEnabled(__sortingEnabled)
        self.actionRe_test.setText(_translate("MainWindow", "Re test"))
from PyQt5 import QtWebKitWidgets
from editor.editing_pane import EditorTabManager


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
