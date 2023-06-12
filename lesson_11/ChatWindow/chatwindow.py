# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys

from PySide2.QtWidgets import QApplication, QWidget
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader, loadUiType

from client import Client


client = Client()

class ChatWindow(QWidget):
    def __init__(self):
        super(ChatWindow, self).__init__()
        self.load_ui()

S


    def load_ui(self):
        loader = QUiLoader()
        path = os.fspath(Path(__file__).resolve().parent / "form.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        loader.load(ui_file, self)
        ui_file.close()


    def get_name(self, name):
        client.client_name = name
        pass

if __name__ == "__main__":
    app = QApplication([])
    widget = ChatWindow()
    widget.show()
    sys.exit(app.exec_())
