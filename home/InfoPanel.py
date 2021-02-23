import os, sys
import base64
import traceback
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from common.common import *


class HomeWindowInfoPanel:
    current_book = None
    
    def set_info_panel(self, book: dict = None):
        """
        Insert into the info pannel the details values of the book

        :param book: dict of the spécified book
        :return: void
        """
        print('set_info_panel')
        # print(book)
        passed = True
        if book is None: 
            passed = False
        else:
            if not is_in(book, ['title', 'serie', 'authors', 'files']):
                passed = False

        if passed is True:
            self.current_book = book['guid']
            self.info_block_title_value.setText(book['title'])
            self.info_block_serie_value.setText(book['serie'])
            self.info_block_authors_value.setText(book['authors'])
            formats = ''
            sizes = ''
            for file in book['files']:
                if formats != '':
                    formats += ' / '
                    sizes += ' / '
                link = file['link']
                if re.search("^data/", link):
                    link = 'file:///' + self.app_directory.replace(os.sep, '/') + '/' + link
                    # link = self.app_directory.replace(os.sep, '/') + '/' + link
                # elif re.search("^(http|https)://", link): {}
                # else: link = 'file:///' + link
                link = link.replace(' ', '%20')
                formats += '<a href="' + link + '" style="color: rgb(255, 255, 255);">' + file['format'] + '</a>'
                sizes += file['size']
            self.info_block_file_formats_value.setText(formats)
            self.info_block_file_formats_value.setOpenExternalLinks(True)
            self.info_block_size_value.setText(sizes)
            try:
                icon = QtGui.QIcon()
                tbimg = book['cover'].split(',')
                by = QtCore.QByteArray()
                by.fromBase64(tbimg[1].encode('utf-8'))
                image = QtGui.QPixmap()
                image.loadFromData(base64.b64decode(tbimg[1]))
                """
                if tbimg[0] == 'data:image/jpeg;base64':
                    image.loadFromData(by, "JPG")
                if tbimg[0] == 'data:image/png;base64':
                    image.loadFromData(by, "PNG")
                """
                icon.addPixmap(image, QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.info_block_cover.setIcon(icon)
                self.info_block_cover.setIconSize(QtCore.QSize(160, 160))
                self.info_block_cover.setToolTip("<img src='{}'/>".format(book['cover']))
            except Exception:
                traceback.print_exc()
                icon = QtGui.QIcon()
                icon.addPixmap(QtGui.QPixmap(self.app_directory + '/icons/white/book.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.info_block_cover.setIcon(icon)
                self.info_block_cover.setIconSize(QtCore.QSize(130, 130))
        else:
            self.info_block_title_value.setText("")
            self.info_block_serie_value.setText("")
            self.info_block_authors_value.setText("")
            self.info_block_file_formats_value.setText("")
            self.info_block_size_value.setText("")

            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(self.app_directory+'/icons/white/book.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.info_block_cover.setIcon(icon)
            self.info_block_cover.setIconSize(QtCore.QSize(130, 130))
