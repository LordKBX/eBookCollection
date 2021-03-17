import traceback
import re
from PyQt5 import QtCore, QtGui, QtWidgets


class HomeWindowSortingBlockTree:
    sorting_block_tree_actual_filter = 'all'

    def sorting_block_tree_init(self):
        self.sorting_block_tree.itemClicked.connect(self.sorting_block_tree_item_activated)
        self.sorting_block_search_button.clicked.connect(self.sorting_block_tree_toogle_search_zone)
        self.sorting_block_search_edit.setMaximumWidth(0)
        self.sorting_block_search_edit.returnPressed.connect(self.sorting_block_tree_research)

    def sorting_block_tree_load_data(self):
        # Clean sub-tree Authors ans Series
        while self.sorting_block_tree.topLevelItem(1).childCount() > 0:
            self.sorting_block_tree.topLevelItem(1).removeChild(self.sorting_block_tree.topLevelItem(1).child(0))
        while self.sorting_block_tree.topLevelItem(2).childCount() > 0:
            self.sorting_block_tree.topLevelItem(2).removeChild(self.sorting_block_tree.topLevelItem(2).child(0))
        authors = self.BDD.get_authors()
        series = self.BDD.get_series()
        for author in authors:
            item = QtWidgets.QTreeWidgetItem(self.sorting_block_tree.topLevelItem(1))
            item.setText(0, author)
            item.setText(1, 'authors:'+author)
        for serie in series:
            item = QtWidgets.QTreeWidgetItem(self.sorting_block_tree.topLevelItem(2))
            item.setText(0, serie)
            item.setText(1, 'series:{}'.format(serie))

    def sorting_block_tree_item_activated(self, item, column):
        try:
            self.sorting_block_tree_set_filter(item.text(1))
        except Exception:
            traceback.print_exc()

    def sorting_block_tree_set_filter(self, filter):
        try:
            self.central_block_table.clearSelection()
            if filter == 'all' or filter == '*':
                filter = '*'
                self.load_books(self.BDD.get_books())
            elif re.search("^authors:", filter) or re.search("^series:", filter):
                self.load_books(self.BDD.get_books(None, filter))
            elif re.search("^search:", filter):
                self.load_books(self.BDD.get_books(None, filter))
            else:
                return
            self.sorting_block_tree_actual_filter = filter
            # self.sorting_block_search_value.setText(filter)

            alayout = QtWidgets.QHBoxLayout()
            alabel = QtWidgets.QLabel()
            alabel.setText(filter)
            alabel.setMaximumHeight(20)
            alayout.addWidget(alabel)
            if filter != '*':
                abutton = QtWidgets.QPushButton()
                abutton.setText("X")
                abutton.setMinimumSize(20, 20)
                abutton.setMaximumSize(20, 20)
                abutton.clicked.connect(lambda: self.sorting_block_tree_set_filter('all'))
                alayout.addWidget(abutton)
            self.clearLayout(self.sorting_block_search_zone)
            self.sorting_block_search_zone.addLayout(alayout)
        except Exception:
            traceback.print_exc()

    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())

    def sorting_block_tree_toogle_search_zone(self):
        w = self.sorting_block_search_edit.width()
        if w <= 0:
            self.sorting_block_search_edit.setMaximumWidth(999999)
            self.sorting_block_search_edit.setFocus()
        else:
            self.sorting_block_search_edit.setMaximumWidth(0)

    def sorting_block_tree_research(self):
        text = self.sorting_block_search_edit.text()
        self.sorting_block_search_edit.setMaximumWidth(0)
        self.sorting_block_search_edit.setText('')
        self.sorting_block_tree_set_filter('search:'+text)
