import traceback
from PyQt5 import QtCore, QtGui, QtWidgets


class HomeWindowSortingBlockTree:
    def SortingBlockTreeInit(self):
        # Clean sub-tree Authors ans Series
        while self.SortingBlockTree.topLevelItem(1).childCount() > 0:
            self.SortingBlockTree.topLevelItem(1).removeChild(self.SortingBlockTree.topLevelItem(1).child(0))
        while self.SortingBlockTree.topLevelItem(2).childCount() > 0:
            self.SortingBlockTree.topLevelItem(2).removeChild(self.SortingBlockTree.topLevelItem(2).child(0))