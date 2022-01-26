#!/usr/bin/env python3

import sys
import os
import threading
from time import strftime, localtime, sleep
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtQml import QQmlApplicationEngine
from PyQt6.QtQuick import QQuickWindow
from PyQt6.QtCore import QObject, pyqtSignal

# tutorial: https://medium.com/analytics-vidhya/how-to-build-your-first-desktop-application-in-python-7568c7d74311

class Backend(QObject):
    updated = pyqtSignal(str, arguments=['updater'])
    def __init__(self):
        QObject.__init__(self)
    def updater(self, curr_time):
        self.updated.emit(curr_time)
    def bootUp(self):
        t_thread = threading.Thread(target=self._bootUp)
        t_thread.daemon = True
        t_thread.start()
    def _bootUp(self):
        while True:
            curr_time = strftime("%I:%M:%S %p", localtime())
            self.updater(curr_time)
            sleep(0.1)




if __name__ == "__main__":
    folder = os.path.join(os.environ['HOME'], 'Desktop', '03-applications', 'desktop_app')
    os.chdir(folder)
    qml_file = './UI/main.qml'

    QQuickWindow.setSceneGraphBackend('software')
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    engine.quit.connect(app.quit)
    engine.load(qml_file)
    back_end = Backend()
    engine.rootObjects()[0].setProperty('backend', back_end)
    back_end.bootUp()
    sys.exit(app.exec())