# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\CODES\Python\EbookCollection\reader\reader.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(QtWidgets.QMainWindow):
    def setupUi(self, MainWindow: QtWidgets.QMainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(966, 784)
        MainWindow.setAutoFillBackground(True)
        MainWindow.setDockNestingEnabled(True)
        MainWindow.setDockOptions(QtWidgets.QMainWindow.AllowNestedDocks|QtWidgets.QMainWindow.AllowTabbedDocks|QtWidgets.QMainWindow.AnimatedDocks|QtWidgets.QMainWindow.GroupedDragging)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.webView = CustomQWebView(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.webView.sizePolicy().hasHeightForWidth())
        self.webView.setSizePolicy(sizePolicy)
        self.webView.setMinimumSize(QtCore.QSize(500, 720))
        self.webView.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.webView.setStyleSheet("background-color: rgb(230, 230, 230);")
        self.webView.setProperty("url", QtCore.QUrl("about:blank"))
        self.webView.setObjectName("webView")
        self.horizontalLayout.addWidget(self.webView)
        MainWindow.setCentralWidget(self.centralwidget)
        self.dockWidgetInfo = QtWidgets.QDockWidget(MainWindow)
        self.dockWidgetInfo.setFeatures(QtWidgets.QDockWidget.DockWidgetClosable|QtWidgets.QDockWidget.DockWidgetMovable)
        self.dockWidgetInfo.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea|QtCore.Qt.RightDockWidgetArea)
        self.dockWidgetInfo.setObjectName("dockWidgetInfo")
        self.dockWidgetContentsInfo = QtWidgets.QWidget()
        self.dockWidgetContentsInfo.setObjectName("dockWidgetContentsInfo")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.dockWidgetContentsInfo)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.infoTextBrowser = QtWidgets.QTextBrowser(self.dockWidgetContentsInfo)
        self.infoTextBrowser.setObjectName("infoTextBrowser")
        self.verticalLayout_3.addWidget(self.infoTextBrowser)
        self.dockWidgetInfo.setWidget(self.dockWidgetContentsInfo)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dockWidgetInfo)
        self.dockWidgetContentTable = QtWidgets.QDockWidget(MainWindow)
        self.dockWidgetContentTable.setFeatures(QtWidgets.QDockWidget.DockWidgetClosable|QtWidgets.QDockWidget.DockWidgetMovable)
        self.dockWidgetContentTable.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea|QtCore.Qt.RightDockWidgetArea)
        self.dockWidgetContentTable.setObjectName("dockWidgetContentTable")
        self.dockWidgeContentstContentTable = QtWidgets.QWidget()
        self.dockWidgeContentstContentTable.setObjectName("dockWidgeContentstContentTable")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.dockWidgeContentstContentTable)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.treeContentTable = QtWidgets.QTreeWidget(self.dockWidgeContentstContentTable)
        self.treeContentTable.setMinimumSize(QtCore.QSize(180, 0))
        self.treeContentTable.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.treeContentTable.setStyleSheet("::section{\n"
"background-color:#4B4B4B;\n"
"}\n"
"QTreeWidget::item { \n"
"    padding-left:2px;\n"
"}\n"
"QTreeWidget::item:hover, QTreeWidget::branch:hover\n"
"{\n"
"    color: rgb(43, 179, 246);\n"
"    cursor: pointer;\n"
"}\n"
"QTreeWidget::item:selected { \n"
"    background-color: rgb(0, 85, 255);\n"
"color:white; \n"
"}")
        self.treeContentTable.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.treeContentTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.treeContentTable.setProperty("showDropIndicator", False)
        self.treeContentTable.setIndentation(0)
        self.treeContentTable.setUniformRowHeights(True)
        self.treeContentTable.setExpandsOnDoubleClick(False)
        self.treeContentTable.setObjectName("treeContentTable")
        self.treeContentTable.headerItem().setTextAlignment(0, QtCore.Qt.AlignCenter)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeContentTable)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeContentTable)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeContentTable)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeContentTable)
        self.treeContentTable.header().setVisible(False)
        self.treeContentTable.header().setCascadingSectionResizes(False)
        self.treeContentTable.header().setSortIndicatorShown(False)
        self.verticalLayout_4.addWidget(self.treeContentTable)
        self.dockWidgetContentTable.setWidget(self.dockWidgeContentstContentTable)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dockWidgetContentTable)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow: QtWidgets.QMainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Ebook Collection - Reader"))
        self.dockWidgetInfo.setWindowTitle(_translate("MainWindow", "Infos"))
        self.infoTextBrowser.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">TEST</p></body></html>"))
        self.dockWidgetContentTable.setWindowTitle(_translate("MainWindow", "Content Table"))
        self.treeContentTable.headerItem().setText(0, _translate("MainWindow", "1"))
        __sortingEnabled = self.treeContentTable.isSortingEnabled()
        self.treeContentTable.setSortingEnabled(False)
        self.treeContentTable.topLevelItem(0).setText(0, _translate("MainWindow", "Cover"))
        self.treeContentTable.topLevelItem(1).setText(0, _translate("MainWindow", "Index"))
        self.treeContentTable.topLevelItem(2).setText(0, _translate("MainWindow", "Chapter 1"))
        self.treeContentTable.topLevelItem(3).setText(0, _translate("MainWindow", "Chapter 2"))
        self.treeContentTable.setSortingEnabled(__sortingEnabled)
from CustomQWebView import CustomQWebView


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
