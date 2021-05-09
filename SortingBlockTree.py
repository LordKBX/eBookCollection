import traceback
import re
from PyQt5 import QtCore, QtGui, QtWidgets


class LibrarySortingFilter:
    def __init__(self, filter_type: str = '*', filter_data: str = None):
        self.type = filter_type
        self.data = filter_data

    def __str__(self):
        return self.type+':{}'.format(self.data)

    def __repr__(self):
        return self.__str__()


class HomeWindowSortingBlockTree:
    sorting_block_tree_actual_filter = 'all'
    sorting_block_tree_actual_filters = []

    def sorting_block_tree_init(self) -> None:
        """
        sorting_block_tree_init
        :return: None
        """
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
            item.setText(1, 'authors:{}'.format(author))
        for serie in series:
            item = QtWidgets.QTreeWidgetItem(self.sorting_block_tree.topLevelItem(2))
            item.setText(0, serie)
            item.setText(1, 'series:{}'.format(serie))

    def sorting_block_tree_item_activated(self, item, column):
        try:
            self.sorting_block_tree_set_filter(item.text(1))
        except Exception:
            traceback.print_exc()

    def sorting_block_tree_set_filter(self, filter: str = None) -> None:
        if filter is None or filter.strip() == '':
            return
        filter_tab = [filter]
        if filter == 'all' or filter == '*':
            self.sorting_block_tree_actual_filters.clear()
            self.sorting_block_tree_actual_filters.append(LibrarySortingFilter('*', None))
        else:
            self.sorting_block_tree_del_filter('*', False)
            filter_tab = filter.split(':')
            found = False
            for index in range(0, len(self.sorting_block_tree_actual_filters)):
                if self.sorting_block_tree_actual_filters[index].type == filter_tab[0]:
                    self.sorting_block_tree_actual_filters[index].data = filter_tab[1]
                    found = True
            if found is False:
                self.sorting_block_tree_actual_filters.append(LibrarySortingFilter(filter_tab[0], filter_tab[1]))
        self.sorting_block_tree_parse_filters()

    def sorting_block_tree_del_filter(self, filter: str = None, filter_print: bool = True) -> bool:
        if filter is None or filter.strip() == '':
            return False
        ender = -1
        for index in range(0, len(self.sorting_block_tree_actual_filters)):
            if self.sorting_block_tree_actual_filters[index].type == filter:
                ender = index
                break
        if ender >= 0:
            self.sorting_block_tree_actual_filters.pop(ender)
        if filter_print is True:
            self.sorting_block_tree_parse_filters()
        return True

    def sorting_block_tree_del_filter_button(self) -> None:
        filter = self.sender().property('filter')
        self.sorting_block_tree_del_filter(filter)

    def sorting_block_tree_parse_filters(self) -> None:
        try:
            self.central_block_table.clearSelection()
            all = False
            if len(self.sorting_block_tree_actual_filters) < 1:
                all = True
            else:
                for filter in self.sorting_block_tree_actual_filters:
                    if filter.type == '*':
                        all = True
                        break
            self.clearLayout(self.sorting_block_search_zone)
            if all is True:
                self.load_books(self.BDD.get_books())

                alayout = QtWidgets.QHBoxLayout()
                alabel = QtWidgets.QLabel()
                alabel.setText('*')
                alabel.setMaximumHeight(20)
                alayout.addWidget(alabel)
                self.sorting_block_search_zone.addLayout(alayout)
            else:
                for filter in self.sorting_block_tree_actual_filters:
                    alayout = QtWidgets.QHBoxLayout()
                    alabel = QtWidgets.QLabel()
                    alabel.setText(filter.type + ':' + filter.data)
                    alabel.setMaximumHeight(20)
                    alayout.addWidget(alabel)

                    abutton = QtWidgets.QPushButton()
                    abutton.setText("X")
                    abutton.setProperty('filter', filter.type)
                    abutton.setMinimumSize(20, 20)
                    abutton.setMaximumSize(20, 20)
                    abutton.clicked.connect(self.sorting_block_tree_del_filter_button)
                    alayout.addWidget(abutton)
                    self.sorting_block_search_zone.addLayout(alayout)
                if len(self.sorting_block_tree_actual_filters) < 2:
                    if filter.type == '*':
                        self.load_books(self.BDD.get_books())
                    elif filter.type in ['authors', 'series', 'search']:
                        self.load_books(self.BDD.get_books(None, filter.type + ':' + filter.data))
                    else:
                        return
                else:
                    books = self.BDD.get_books()
                    end_books = []
                    for book in books:
                        ok = True
                        for filter in self.sorting_block_tree_actual_filters:
                            if filter.type == 'authors':
                                if book['authors'] != filter.data: ok = False
                            if filter.type == 'series':
                                if book['series'] != filter.data: ok = False
                            if filter.type == 'search':
                                fd = filter.data.lower()
                                i = book['title'].lower()
                                s = book['series'].lower()
                                a = book['authors'].lower()
                                t = book['tags'].lower()
                                if fd not in i and fd not in s and fd not in a and fd not in t:
                                    ok = False
                        if ok is True:
                            end_books.append(book)
                    self.load_books(end_books)
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

    def sorting_block_tree_toogle_search_zone(self) -> None:
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
