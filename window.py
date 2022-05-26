import PyQt5
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QMovie, QIcon, QCursor
import re
import win32gui, win32con, win32com.client
import threading
import random
import sys
import os
import subprocess


class root(QMainWindow):
    def __init__(self):
        super().__init__()
        self.petList = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16']
        self.is_follow_mouse = True
        self.mouse_drag_pos = self.pos()
        self.petNum = random.randint(1, 16)
        self.setUI()

    def setUI(self):
        self.setWindowFlags(Qt.FramelessWindowHint|Qt.WindowStaysOnTopHint|Qt.SubWindow)
        self.resize(200, 200)
        self.setAutoFillBackground(False)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.repaint()
        # 创建label盛放悬浮窗
        self.label = QLabel('', self)
        self.label.resize(200, 200)
        self.label.move(25, 25)
        self.randomPet()
        # 退出功能的定义
        self.Quit = QAction('Quit', self, triggered = qApp.quit)
        self.Quit_Icon = QIcon('./resourses/exit.png')
        self.Quit.setIcon(self.Quit_Icon)
        # 截图功能的定义
        self.shot = QAction('Screen Shot', self, triggered = self.screenshot)
        self.Shot_Icon = QIcon('./resourses/screenshot.png')
        self.shot.setIcon(self.Shot_Icon)
        # 返回
        self.back = QAction('Back To Menu', self, triggered = self.back)
        self.url_icon = QIcon('./resourses/back.ico')
        self.back.setIcon(self.url_icon)
 
        # Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.randomPet)
        self.timer.start(5000)
        # 最小化到托盘
        self.tray_icon_menu = QMenu(self)
        self.tray_icon_menu.addAction(self.Quit)
        self.tray_icon = QSystemTrayIcon(self)
        self.trayIcon = QIcon('./resourses/ico.png')
        self.tray_icon.setIcon(self.trayIcon)
        self.tray_icon.setContextMenu(self.tray_icon_menu)
        self.tray_icon.show()


        self.show()

    '''def baidu(self):
        client_th = threading.Thread(target = self.wenku_back)
        client_th.setDaemon(True)
        client_th.start()

    def wenku_back(self):
        subprocess.run('wenku.exe')'''

    def back(self):
        self.hide()
        win32gui.EnumWindows(_window_enum_callback, ".*%s.*" % "Rumor Defender")
        

    def randomPet(self):
        self.petNum = random.randint(0, 15)
        print(self.petNum, self.petList[self.petNum])
        self.gif = QMovie('./pics/' + str(self.petList[self.petNum]) + '.gif')
        self.label.setMovie(self.gif)
        self.gif.start()
        self.label.update()

    def contextMenuEvent(self, event):
        cmenu = QMenu(self)
        quitAction = cmenu.addAction(self.Quit)
        shotAction = cmenu.addAction(self.shot)
        backAction = cmenu.addAction(self.back)
        action = cmenu.exec_(self.mapToGlobal(event.pos()))

    def screenshot(self):
        # os.system('screenshot.exe')
        subprocess.run('screenshot.exe')

    '''鼠标左键按下时, 悬浮窗将和鼠标位置绑定'''
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_follow_mouse = True
            self.mouse_drag_pos = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))
    '''鼠标移动, 则悬浮窗也移动'''
    def mouseMoveEvent(self, event):
        if Qt.LeftButton and self.is_follow_mouse:
            self.move(event.globalPos() - self.mouse_drag_pos)
            event.accept()
    '''鼠标释放时, 取消绑定'''
    def mouseReleaseEvent(self, event):
        self.is_follow_mouse = False
        self.setCursor(QCursor(Qt.ArrowCursor))


def _window_enum_callback(hwnd, wildcard):
    if re.match(wildcard, str(win32gui.GetWindowText(hwnd))) is not None:
        win32gui.BringWindowToTop(hwnd)
        # 先发送一个alt事件，否则会报错导致后面的设置无效：pywintypes.error: (0, 'SetForegroundWindow', 'No error message is available')
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.SendKeys('%')
        # 设置为当前活动窗口
        win32gui.SetForegroundWindow(hwnd)
        # normal size 窗口
        win32gui.ShowWindow(hwnd,win32con.SW_NORMAL)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    graph = root()
    sys.exit(app.exec_())
