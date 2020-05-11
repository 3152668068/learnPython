import sys, os, webbrowser
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from earthWallpaper import *
from datetime import datetime
from PyQt5 import sip

class SetGUI(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUi()


    def initUi(self):

        #设置窗口居中显示
        self.resize(600,500)
        screenSize=QDesktopWidget().screenGeometry()
        self.move((screenSize.width()-500)/2,(screenSize.height()-500)/2)

        #设置图标以及标题
        self.setWindowTitle("地球壁纸")
        self.setWindowIcon(QIcon('planet_earth.ico'))

        #设置布局，添加button
        layout = QHBoxLayout()
        runButton=self.getButton("设置壁纸",1)
        runButton.clicked.connect(self.runInfo)

        aboutButton=self.getButton("关于软件", 2)
        aboutButton.clicked.connect(self.aboutInfo)

        connectButton=self.getButton("联系作者", 3)
        connectButton.clicked.connect(self.connectInfo)

        layout.addWidget(runButton)
        layout.addWidget(aboutButton)
        layout.addWidget(connectButton)

        self.setLayout(layout)

        self.statusBar().showMessage('图像来源：日本himawari-8气象卫星官网，因此连接较慢，可能会出现未响应，请稍等')

        #主循环，显示
        self.show()


    def runInfo(self):

        status=imgDown()
        if status==False:
            QMessageBox.information(self, "获取失败", "下载图像失败，请稍后重试")
            return False
        path=os.getcwd()
        status=setWallpaper(os.path.join(os.getcwd(),"earth.png"))
        if status:
            self.statusBar().showMessage('设置壁纸成功  时间: '+str(datetime.now()))
        else:
            QMessageBox.information(self,"运行错误","未知错误，请稍后重试，或者联系作者")

    def aboutInfo(self):
        QMessageBox.information(self,"软件说明","Version: 1.0\n\nAuthor: Foryatto\n\n本软件仅供学习交流，切勿用作非法用途！")

    def connectInfo(self):
        webbrowser.open_new_tab("https://github.com/foryatto")

    #创建button
    def getButton(self, buttonName,th):
        button=QPushButton(buttonName,self)
        button.resize(button.sizeHint())
        button.move((600-button.width())//2,80*th)
        return button




if __name__=='__main__':

    # 关闭所有窗口,也不关闭应用程序
    QApplication.setQuitOnLastWindowClosed(False)

    app=QApplication(sys.argv)
    window=SetGUI() #初始化程序

    #设置系统托盘
    tp = QSystemTrayIcon(window)
    tp.setIcon(QIcon('planet_earth.ico'))
    a1 = QAction('&设置壁纸',triggered=window.runInfo)
    a2 = QAction('&结束程序', triggered=qApp.quit)  # 直接退出可以用qApp.quit
    tpMenu = QMenu()
    tpMenu.addAction(a1)
    tpMenu.addAction(a2)
    tp.setContextMenu(tpMenu)
    # 不调用show不会显示系统托盘
    tp.show()
    def act(reason):
        # 鼠标点击icon传递的信号会带有一个整形的值，1是表示单击右键，2是双击，3是单击左键，4是用鼠标中键点击
        if reason == 3 or reason == 2:
            window.show()
    tp.activated.connect(act)

    sys.exit(app.exec_())



