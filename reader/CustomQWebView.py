from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtWebKitWidgets
import traceback
from enum import Enum
import pyperclip


class QwwMode(Enum):
	CBZ = 1
	EPUB = 2
	PDF = 3


class CustomQWebView(QtWebKitWidgets.QWebView):
	def __init__(self, parent):
		QtWebKitWidgets.QWebView.__init__(self, parent)
		self.nbpage = 0
		self.page = super().page
		self.mode = QwwMode.CBZ
		self.ctrlOn = False
		self.initialized = False
		self.eventHandler = None

	def setMode(self, mode: QwwMode):
		self.mode = mode
		self.initialized = True

	def setEventHandler(self, handler: any):
		self.eventHandler = handler

	# def mouseReleaseEvent(self, event):
	# 	print('mouseReleaseEvent')
	#
	# def mousePressEvent(self, event):
	# 	print('mousePressEvent')
	#
	# def mouseDoubleClickEvent(self, event):
	# 	print('mouseDoubleClickEvent')

	def wheelEvent(self, event: QtGui.QWheelEvent):
		try:
			zoom = super().page().mainFrame().zoomFactor()
			if self.ctrlOn is True:
				event.accept()
				if event.angleDelta().y() > 0:
					zoom += 0.2
				else:
					zoom -= 0.2
				if zoom <= 0.2: zoom = 0.2
				if zoom >= 3: zoom = 3
				print('zoom = {}'.format(zoom))
				super().page().mainFrame().setZoomFactor(zoom)
			# super().page().repaint()
			else:
				if self.mode.value == QwwMode.CBZ.value:
					super().page().mainFrame().setZoomFactor(1)
					event.accept()
					passed = 0
					if event.angleDelta().y() < 0: passed = 1
					elif event.angleDelta().y() > 0: passed = -1
					self.updatePositionCbz(passed)
				else:
					self.updatePositionEpub(event.angleDelta().y() * -1)
					event.ignore()
		except Exception:
			traceback.print_exc()

	# def mouseMoveEvent(self, event):
	# 	print('mouseMoveEvent')

	def keyPressEvent(self, event: QtGui.QKeyEvent):
		if event.type() != QtCore.QEvent.KeyPress: event.ignore()
		else:
			if self.mode.value == QwwMode.EPUB.value:
				event.ignore()
			if event.key() == QtCore.Qt.Key_Control:
				self.ctrlOn = True
				return
			if self.ctrlOn is True:
				print('KeyPress + Ctrl')
				if self.mode.value == QwwMode.CBZ.value:
					if event.key() in [QtCore.Qt.Key_0, QtCore.Qt.Key_Escape]:
						super().page().mainFrame().setZoomFactor(1)
				elif self.mode.value == QwwMode.EPUB.value:
					if event.key() in [QtCore.Qt.Key_C]:
						pyperclip.copy(super().page().selectedText())
			else:
				try:
					if self.mode.value == QwwMode.CBZ.value:
						zoom = super().page().mainFrame().zoomFactor()
						if zoom != 1:
							position = super().page().mainFrame().scrollPosition()
							if event.key() in [QtCore.Qt.Key_PageDown, QtCore.Qt.Key_PageUp]:
								super().page().mainFrame().setZoomFactor(1)
								self.updatePositionCbz(0)
							elif event.key() in [QtCore.Qt.Key_Left]:
								super().page().mainFrame().setScrollPosition(QtCore.QPoint(position.x() - 5, position.y()))
							elif event.key() in [QtCore.Qt.Key_Right]:
								super().page().mainFrame().setScrollPosition(QtCore.QPoint(position.x() + 5, position.y()))
							elif event.key() in [QtCore.Qt.Key_Up]:
								super().page().mainFrame().setScrollPosition(QtCore.QPoint(position.x(), position.y() - 5))
							elif event.key() in [QtCore.Qt.Key_Down]:
								super().page().mainFrame().setScrollPosition(QtCore.QPoint(position.x(), position.y() + 5))
							return
						passed = 0
						if event.key() in [QtCore.Qt.Key_Left, QtCore.Qt.Key_Up, QtCore.Qt.Key_PageUp]: passed = -1
						elif event.key() in [QtCore.Qt.Key_Right, QtCore.Qt.Key_Down, QtCore.Qt.Key_PageDown]: passed = 1
						self.updatePositionCbz(passed)
				except Exception:
					traceback.print_exc()

	def keyReleaseEvent(self, event: QtGui.QKeyEvent):
		try:
			if event.key() == QtCore.Qt.Key_Control:
				self.ctrlOn = False
		except Exception:
			traceback.print_exc()

	def resizeEvent(self, event: QtGui.QResizeEvent):
		super().resizeEvent(event)
		try:
			if self.mode.value == QwwMode.CBZ.value:
				self.updatePositionCbz(0)
				if self.initialized is True:
					super().page().currentFrame().evaluateJavaScript("imgResize();")
		except Exception:
			traceback.print_exc()

	def updatePositionEpub(self, delta: int):
		pos = super().page().mainFrame().scrollPosition()
		calc = pos.y() + delta
		if (super().page().mainFrame().contentsSize().height() - super().height()) >= calc >= 0:
			super().page().mainFrame().setScrollPosition( QtCore.QPoint(pos.x(), calc) )
			self.eventHandler({
				'type': 'scroll',
				'value': (calc > 0)
			})
		else:
			if self.eventHandler is not None:
				if delta < 0:
					super().page().mainFrame().setScrollPosition(QtCore.QPoint(pos.x(), 0))
					self.eventHandler({
						'type': 'chapterChange',
						'value': 'prev'
					})
				else:
					super().page().mainFrame().setScrollPosition(QtCore.QPoint(pos.x(), super().page().mainFrame().contentsSize().height() - super().height()))
					self.eventHandler({
						'type': 'chapterChange',
						'value': 'next'
					})


	def updatePositionCbz(self, passed: int):
		if self.nbpage + passed >= 0:
			if (self.nbpage + passed) * super().height() >= super().page().mainFrame().contentsSize().height(): return
			self.nbpage = self.nbpage + passed
			super().page().mainFrame().setScrollPosition(
				QtCore.QPoint(0, self.nbpage * super().height())
			)
			if passed > 0: self.eventHandler({ 'type': 'pageChange', 'value': 'next', 'index': self.nbpage })
			else: self.eventHandler({ 'type': 'pageChange', 'value': 'prev', 'index': self.nbpage })

	def updatePositionCbzByPage(self, page_index: int):
		max = int(super().page().mainFrame().contentsSize().height() / super().height())
		if page_index < 0 or page_index >= max: return
		if (page_index) * super().height() >= super().page().mainFrame().contentsSize().height(): return
		self.nbpage = page_index
		super().page().mainFrame().setZoomFactor(1)
		super().page().mainFrame().setScrollPosition(
			QtCore.QPoint(0, self.nbpage * super().height())
		)

	def updatePositionCbzEnd(self):
		super().page().mainFrame().setZoomFactor(1)
		super().page().mainFrame().setScrollPosition(
			QtCore.QPoint(0, super().page().mainFrame().contentsSize().height() - super().height())
		)

	def updatePositionCbzStart(self):
		super().page().mainFrame().setZoomFactor(1)
		super().page().mainFrame().setScrollPosition(QtCore.QPoint(0, 0))
