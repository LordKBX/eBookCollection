import traceback
import re
from PyQt5 import QtCore, QtGui, QtWidgets


class HomeWindowSortingBlockTree:
    SortingBlockTreeActualFilter = 'all'
    def SortingBlockTreeInit(self):
        self.SortingBlockTree.itemClicked.connect(self.SortingBlockTreeItemActivated)

    def SortingBlockTreeLoadData(self):
        # Clean sub-tree Authors ans Series
        while self.SortingBlockTree.topLevelItem(1).childCount() > 0:
            self.SortingBlockTree.topLevelItem(1).removeChild(self.SortingBlockTree.topLevelItem(1).child(0))
        while self.SortingBlockTree.topLevelItem(2).childCount() > 0:
            self.SortingBlockTree.topLevelItem(2).removeChild(self.SortingBlockTree.topLevelItem(2).child(0))
        authors = self.BDD.getAuthors()
        series = self.BDD.getSeries()
        for author in authors:
            item = QtWidgets.QTreeWidgetItem(self.SortingBlockTree.topLevelItem(1))
            item.setText(0, author)
            item.setText(1, 'authors:'+author)
        for serie in series:
            item = QtWidgets.QTreeWidgetItem(self.SortingBlockTree.topLevelItem(2))
            item.setText(0, serie)
            item.setText(1, 'serie:'+serie)

    def SortingBlockTreeItemActivated(self, item, column):
        try:
            self.SortingBlockTreeSetFilter(item.text(1))
        except Exception:
            traceback.print_exc()

    def SortingBlockTreeSetFilter(self, filter):
        try:
            self.CentralBlockTable.clearSelection()
            if filter == 'all':
                self.loadooks(self.BDD.getBooks())
            elif re.search("^authors:", filter) or re.search("^serie:", filter):
                self.loadooks(self.BDD.getBooks(None, filter))
            else:
                return
            self.SortingBlockTreeActualFilter = filter
            self.SortingBlockSearchValue.setText(filter)
        except Exception:
            traceback.print_exc()
