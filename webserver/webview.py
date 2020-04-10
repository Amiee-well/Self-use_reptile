# -*- coding: utf-8 -*-
import sys,os
from PyQt5 import QtCore, QtGui, QtWidgets
from qtmodern import styles,windows
from PyQt5.QtCore import pyqtSlot, QUrl, QEvent, Qt, QObject
from PyQt5.QtWidgets import QMainWindow, QApplication, QTabWidget, QMessageBox, QWidget, QVBoxLayout, QCompleter
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
try:
    import file.webserver.res_rc
except:
    import res_rc
if getattr(sys, 'frozen', False):
    cur_path = sys._MEIPASS
else:
    cur_path = os.path.dirname(__file__)
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.resize(1001, 658)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralWidget)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.pb_new = QtWidgets.QPushButton(self.centralWidget)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(cur_path +"/file/webserver/images/new.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pb_new.setIcon(icon)
        self.pb_new.setText("新页面")
        self.horizontalLayout.addWidget(self.pb_new)
        self.pb_home = QtWidgets.QPushButton(self.centralWidget)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(cur_path +"/file/webserver/images/home.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pb_home.setIcon(icon1)
        self.pb_home.setText("主页")
        self.horizontalLayout.addWidget(self.pb_home)
        self.pb_forward = QtWidgets.QPushButton(self.centralWidget)
        self.pb_forward.setEnabled(False)
        self.pb_forward.setText("前进")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(cur_path +"/file/webserver/images/forward.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pb_forward.setIcon(icon2)
        self.horizontalLayout.addWidget(self.pb_forward)
        self.pb_back = QtWidgets.QPushButton(self.centralWidget)
        self.pb_back.setEnabled(False)
        self.pb_back.setText("后退")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(cur_path +"/file/webserver/images/back.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pb_back.setIcon(icon3)
        self.horizontalLayout.addWidget(self.pb_back)
        self.pb_refresh = QtWidgets.QPushButton(self.centralWidget)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(cur_path +"/file/webserver/images/reload.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pb_refresh.setIcon(icon4)
        self.pb_refresh.setText("刷新")
        self.horizontalLayout.addWidget(self.pb_refresh)
        self.pb_stop = QtWidgets.QPushButton(self.centralWidget)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(cur_path +"/file/webserver/images/stop.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pb_stop.setIcon(icon5)
        self.pb_stop.setText("停止")
        self.horizontalLayout.addWidget(self.pb_stop)
        self.lineEdit = QtWidgets.QLineEdit(self.centralWidget)
        self.horizontalLayout.addWidget(self.lineEdit)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        self.progressBar = QtWidgets.QProgressBar(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.progressBar.sizePolicy().hasHeightForWidth())
        self.progressBar.setSizePolicy(sizePolicy)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setTextVisible(False)
        self.horizontalLayout_2.addWidget(self.progressBar)
        self.pb_go = QtWidgets.QPushButton(self.centralWidget)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(cur_path +"/file/webserver/images/go.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pb_go.setIcon(icon6)
        self.pb_go.setText("GO")
        self.horizontalLayout_2.addWidget(self.pb_go)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.tabWidget = QtWidgets.QTabWidget(self.centralWidget)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Triangular)
        self.tabWidget.setDocumentMode(True)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setMovable(True)
        self.verticalLayout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralWidget)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusBar)
        self.tabWidget.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
class NewWebView(QWebEngineView):
    def __init__(self, tabWidget):
        super().__init__()
        self.tabWidget = tabWidget
    def createWindow(self, WebWindowType):
        new_webview = NewWebView(self.tabWidget)
        self.tabWidget.newTab(new_webview)
        return new_webview
class WebView(QMainWindow, Ui_MainWindow):
    def __init__(self,web, parent=None):
        super(WebView, self).__init__(parent)
        self.web = web
        self.setupUi(self)
        self.initUi()
    def initUi(self):
        self.progressBar.hide()
        self.showMaximized()
        self.tabWidget.tabCloseRequested.connect(self.closeTab)
        self.tabWidget.currentChanged.connect(self.tabChange)
        self.view = NewWebView(self)
        self.view.load(QUrl("{}".format(self.web)))
        self.newTab(self.view)
        self.lineEdit.installEventFilter(self)
        self.lineEdit.setMouseTracking(True)
        settings = QWebEngineSettings.defaultSettings()
        settings.setAttribute(QWebEngineSettings.PluginsEnabled, True)
        self.getModel()
    def getModel(self):
        self.m_model = QStandardItemModel(0, 1, self)
        m_completer = QCompleter(self.m_model, self)
        self.lineEdit.setCompleter(m_completer)
        m_completer.activated[str].connect(self.onUrlChoosed)
    def newTab(self, view):
        self.pb_forward.setEnabled(False)
        self.pb_back.setEnabled(False)
        view.titleChanged.connect(self.webTitle)
        view.iconChanged.connect(self.webIcon)
        view.loadProgress.connect(self.webProgress)
        view.loadFinished.connect(self.webProgressEnd)
        view.urlChanged.connect(self.webHistory)
        view.page().linkHovered.connect(self.showUrl)
        currentUrl = self.getUrl(view)
        self.lineEdit.setText(currentUrl)
        self.tabWidget.addTab(view, "新标签页")
        self.tabWidget.setCurrentWidget(view)
    def getUrl(self, webview):
        url = webview.url().toString()
        return url
    def closeTab(self, index):
        if self.tabWidget.count() > 1:
            self.tabWidget.widget(index).deleteLater()
            self.tabWidget.removeTab(index)
        elif self.tabWidget.count() == 1:
            self.tabWidget.removeTab(0)
            self.on_pb_new_clicked()
    def tabChange(self, index):
        currentView = self.tabWidget.widget(index)
        if currentView:
            currentViewUrl = self.getUrl(currentView)
            self.lineEdit.setText(currentViewUrl)
    def closeEvent(self, event):
        tabNum = self.tabWidget.count()
        closeInfo = "你打开了{}个标签页，现在确认关闭？".format(tabNum)
        if tabNum > 1:
            r = QMessageBox.question(self, "关闭浏览器", closeInfo, QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Cancel)
            if r == QMessageBox.Ok:
                event.accept()
            elif r == QMessageBox.Cancel:
                event.ignore()
        else:
            event.accept()
    def eventFilter(self, object, event):
        if object == self.lineEdit:
            if event.type() == QEvent.MouseButtonRelease:
                self.lineEdit.selectAll()
            elif event.type() == QEvent.KeyPress:
                if event.key() == Qt.Key_Return:
                    self.on_pb_go_clicked()
        return QObject.eventFilter(self, object, event)
    def webTitle(self, title):
        index = self.tabWidget.currentIndex()
        if len(title) > 16:
            title = title[0:17]
        self.tabWidget.setTabText(index, title)
    def webIcon(self, icon):
        index = self.tabWidget.currentIndex()
        self.tabWidget.setTabIcon(index, icon)
    def webProgress(self, progress):
        self.progressBar.show()
        self.progressBar.setValue(progress)
    def webProgressEnd(self, isFinished):
        if isFinished:
            self.progressBar.setValue(100)
            self.progressBar.hide()
            self.progressBar.setValue(0)
    def webHistory(self, url):
        self.lineEdit.setText(url.toString())
        index = self.tabWidget.currentIndex()
        currentView = self.tabWidget.currentWidget()
        history = currentView.history()
        if history.count() > 1:
            if history.currentItemIndex() == history.count()-1:
                self.pb_back.setEnabled(True)
                self.pb_forward.setEnabled(False)
            elif history.currentItemIndex() == 0:
                self.pb_back.setEnabled(False)
                self.pb_forward.setEnabled(True)
            else:
                self.pb_back.setEnabled(True)
                self.pb_forward.setEnabled(True)
    def showUrl(self, url):
        self.statusBar.showMessage(url)
    def onUrlChoosed(self, url):
        self.lineEdit.setText(url)
    @pyqtSlot(str)
    def on_lineEdit_textChanged(self, text):
        urlGroup = text.split(".")
        if len(urlGroup) == 3 and urlGroup[-1]:
            return
        elif len(urlGroup) == 3 and not(urlGroup[-1]):
            wwwList = [ "com", "cn", "net", "org", "gov", "cc" ]
            self.m_model.removeRows(0, self.m_model.rowCount())
            for i in range(0, len(wwwList)):
                self.m_model.insertRow(0)
                self.m_model.setData(self.m_model.index(0, 0), text + wwwList[i])
    @pyqtSlot()
    def on_pb_new_clicked(self):
        newView = NewWebView(self)
        self.newTab(newView)
        newView.load(QUrl(""))
    @pyqtSlot()
    def on_pb_forward_clicked(self):
        self.tabWidget.currentWidget().forward()
    @pyqtSlot()
    def on_pb_back_clicked(self):
        self.tabWidget.currentWidget().back()
    @pyqtSlot()
    def on_pb_refresh_clicked(self):
        self.tabWidget.currentWidget().reload()
    @pyqtSlot()
    def on_pb_stop_clicked(self):
        self.tabWidget.currentWidget().stop()
    @pyqtSlot()
    def on_pb_go_clicked(self):
        url = self.lineEdit.text()
        if url[0:12] == "http://www." or url[0:13] == "https://www.":
            qurl = QUrl(url)
        elif url[0:5] == "www.":
            qurl = QUrl("http://" + url)
        else:
            qurl = QUrl("http://www." + url)
        self.tabWidget.currentWidget().load(qurl)
    @pyqtSlot()
    def on_pb_home_clicked(self):
        homeurl = QUrl("http://www.xdbcb8.com")
        if self.tabWidget.currentWidget().title() == "about:blank":
            self.tabWidget.currentWidget().load(homeurl)
        else:
            newView = NewWebView(self)
            self.newTab(newView)
            newView.load(homeurl)
    def __del__(self):
        self.view.deleteLater()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mv = windows.ModernWindow(WebView("https://www.baidu.com"))
    mv.showFullScreen()
    sys.exit(app.exec_())
