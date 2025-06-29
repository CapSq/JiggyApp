import sys, os
from PyQt5.QtWidgets import QApplication, QWidget, QMenu, QAction, QPushButton, QVBoxLayout, QSystemTrayIcon

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QObject, QEvent


_systray_refs = {}

def minimize_systray(window,tray_icon):
    window.hide()
    tray_icon.showMessage("Minimized", "App is minimized to tray", QSystemTrayIcon.MessageIcon.Information, 500)

def create_systray(app, window, tray_tooltip):
    basedir = getattr(sys, "_MEIPASS", os.path.abspath("."))
    ICON_NAME = os.path.join(basedir, "icon.ico")
    tray_icon = QSystemTrayIcon(QIcon(ICON_NAME),parent=app) 
    tray_icon.setToolTip(tray_tooltip)
    tray_icon.setVisible(True)
    window.setWindowIcon(QIcon(ICON_NAME))
    
    #add systray menu
    tray_menu = QMenu(window)

    restore_option = QAction("Restore")
    tray_menu.addAction(restore_option)

    quit_option = QAction("Quit")
    tray_menu.addAction(quit_option)

    tray_icon.setContextMenu(tray_menu)

    #show systray icon
    tray_icon.show()

    #restore from tray
    restore_option.triggered.connect(lambda: window.showNormal())
    quit_option.triggered.connect(app.quit)

    #restore on double click
    def restore_On__DoubleClick(reason):
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            window.showNormal()
    tray_icon.activated.connect(restore_On__DoubleClick)

    # autohide on minimize
    class MinimizeEventFilter(QObject):
        def eventFilter(self, obj, event):
            if event.type() == QEvent.Type.WindowStateChange:
                if obj.isMinimized():
                    obj.hide()
                    tray_icon.showMessage("Minimized", "App minimized to tray", QSystemTrayIcon.MessageIcon.Information, 500)
            return False

    filter = MinimizeEventFilter(tray_icon)
    window.installEventFilter(filter)

    # tray_icon.tray_menu = tray_menu
    # tray_icon.restore_option = restore_option
    # tray_icon.quit_option = quit_option
    # tray_icon.minimize_filter = filter

    _systray_refs [tray_icon] = {
        "tray_menu": tray_menu,
        "restore_option": restore_option,
        "quit_option": quit_option,
        "minimize_filter": filter,
    }

    return tray_icon


