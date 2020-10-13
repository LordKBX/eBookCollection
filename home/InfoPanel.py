import json
import re
import base64
import traceback
from PyQt5 import QtCore, QtGui, QtWidgets
from common import *


class HomeWindowInfoPanel:
    def setInfoPanel(self, book: dict = None):
        """
        Insert into the info pannel the details values of the book

        :param book: dict of the spécified book
        :return: void
        """
        print('setInfoPanel')
        # print(book)
        passed = True
        if book is None: passed = False
        else:
            if not is_in(book, ['title', 'serie', 'authors', 'files', 'synopsis']):
                passed = False

        if passed is True:
            self.InfoBlockTitleValue.setText(book['title'])
            self.InfoBlockSerieValue.setText(book['serie'])
            self.InfoBlockAuthorsValue.setText(book['authors'])
            formats = ''
            sizes = ''
            for file in book['files']:
                if formats != '':
                    formats += ' / '
                    sizes += ' / '
                link = file['link']
                if re.search("^data/", link):
                    link = 'file:///' + self.appDir.replace(os.sep, '/') + '/' + link
                    # link = self.appDir.replace(os.sep, '/') + '/' + link
                # elif re.search("^(http|https)://", link): {}
                # else: link = 'file:///' + link
                link = link.replace(' ', '%20')
                formats += '<a href="' + link + '" style="color: rgb(255, 255, 255);">' + file['format'] + '</a>'
                sizes += file['size']
            self.InfoBlockFileFormatsValue.setText(formats)
            self.InfoBlockFileFormatsValue.setOpenExternalLinks(True)
            self.InfoBlockSizeValue.setText(sizes)
            self.InfoBlockSynopsisValue.setText(book['synopsis'])
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
                self.InfoBlockCover.setIcon(icon)
                self.InfoBlockCover.setIconSize(QtCore.QSize(160, 160))
            except Exception:
                traceback.print_exc()
        else:
            self.InfoBlockTitleValue.setText("")
            self.InfoBlockSerieValue.setText("")
            self.InfoBlockAuthorsValue.setText("")
            self.InfoBlockFileFormatsValue.setText("")
            self.InfoBlockSizeValue.setText("")
            self.InfoBlockSynopsisValue.setText("")

            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(self.appDir+'/icons/white_book.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.InfoBlockCover.setIcon(icon)
            self.InfoBlockCover.setIconSize(QtCore.QSize(130, 130))
