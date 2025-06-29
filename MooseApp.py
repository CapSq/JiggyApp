import sys
import moose_move as move_mouse
import GenerateSysTray as systrays
from PyQt5.QtCore import Qt, QObject, QEvent, QThread
from PyQt5.QtWidgets import QApplication, QWidget, QSystemTrayIcon, QMenu, QSlider, QPushButton, QVBoxLayout, QHBoxLayout, QLabel
import sys
import inspect
import time
import random

Jiggy = QApplication(sys.argv)


def printlog():
    frame = inspect.currentframe()
    if frame is not None and frame.f_back is not None:
        caller_name = frame.f_back.f_code.co_name
        print(f"Called from function: {caller_name}\n")
    else:
        print("Caller frame not found")

def init_layout(Jiggy):
    printlog()

    window = QWidget()
    window.setWindowTitle("Jiggy")
    window.resize(250, 100)
    
    APP_NAME = "Jiggy"
    #systrays.create_systray(Jiggy, window, "SysTray")
    tray_icon = systrays.create_systray(Jiggy, window, APP_NAME)

    column = QVBoxLayout()
    row1 = QHBoxLayout()
    row2 = QHBoxLayout()

    #add buttons
    interval_slider = create_Slider(row2)
    start_button = create_Start_Button(window, row1, interval_slider,tray_icon)
    exit_button = create_Exit_Button(row1)
    move_thread = JiggyThreader(interval_slider)

    #add columns
    column.addLayout(row1)
    column.addLayout(row2)
                    
    window.setLayout(column)
    window.show()

    sys.exit(Jiggy.exec_())
    return window


def create_Start_Button(window,row,interval_slider,tray_icon):
    printlog()
    start_button = QPushButton("Start")
    start_button.clicked.connect(lambda: on_Click_Start_Button(window, interval_slider, start_button, tray_icon))
    row.addWidget(start_button,stretch=0)
    start_button.setFixedSize(100, 40)
    #return start_button

def create_Exit_Button(row):
    printlog()
    exit_button = QPushButton("Quit")
    exit_button.clicked.connect(on_Click_Exit_Button)
    row.addWidget(exit_button,stretch=0)
    exit_button.setFixedSize(100, 40)
    #return exit_button

def create_Slider(row):
    printlog()

    slider = QSlider(Qt.Orientation.Horizontal) # Or Qt.Vertical
    slider.setMinimum(1)
    slider.setMaximum(60)
    slider.setValue(10)

    slider_label = QLabel(f"Interval(Min): {slider.value()}")
    slider.valueChanged.connect(lambda value: slider_label.setText(f"Interval(Min): {value}"))

    row.addWidget(slider)
    row.addWidget(slider_label)
    return slider

def on_Click_Start_Button(window, interval_slider, start_button, tray_icon):
    printlog()
    if not hasattr(window, "move_thread"):
        window.move_thread = JiggyThreader(interval_slider)
    if start_button.text() == "Start":
        if not hasattr(window, "move_thread") or not window.move_thread.isRunning():
            window.move_thread = JiggyThreader(interval_slider)
        print(start_button.text())
        start_button.setText("Paused")
        window.hide()
        tray_icon.showMessage("Minimized", "App minimized to tray", QSystemTrayIcon.MessageIcon.Information, 500)
        window.move_thread.start()
        

    elif start_button.text() == "Paused":
        print(start_button.text())
        window.move_thread.stop()
        window.move_thread.wait()
        start_button.setText("Start")

def on_Click_Exit_Button():
    printlog()
    QApplication.quit()

def test_Button(row,window,tray_icon):
    printlog()
    test_button = QPushButton("Test")
    test_button.clicked.connect(lambda: systrays.minimize_systray(window, tray_icon))
    row.addWidget(test_button,stretch=0)
    test_button.setFixedSize(100, 40)
    #return test_button

def on_Click_Test_Button(window,tray_icon):
    window.hide()
    tray_icon.showMessage("Minimized", "Check systray",QSystemTrayIcon.MessageIcon.Information, 1000)

class JiggyThreader(QThread):
    def __init__(self, interval_slider ):
        super().__init__()
        self.interval_slider = interval_slider
        self.running = True

    def run(self):
        MINUTE = 60
        while self.running:
            interval = int(self.interval_slider.value())
            move_mouse.jiggy()
            
            total_wait = random.uniform(MINUTE * interval/2, MINUTE * interval)
            waited = 0
            wait_interval = 0.1 #100ms at a time

            while self.running and waited < total_wait:
                time.sleep(wait_interval)
                waited = waited + wait_interval
            #time.sleep(random.uniform(MINUTE * interval/2, MINUTE * interval))
    
    def stop(self):
        self.running = False

init_layout(Jiggy)


