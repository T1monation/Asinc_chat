import sys
from PyQt6.QtCore import QSize, Qt, QDir
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QLabel, QVBoxLayout, QWidget, QFormLayout
from client import Client

client = Client()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Client")
        self.setMinimumSize((QSize(800, 600)))
        # кнопка Connect
        self.connect_button = QPushButton("Connect")
        self.connect_button.setEnabled(False)
        self.connect_button.setCheckable(True)
        self.connect_button.clicked.connect(self.clicked_connect_button)
        # кнопка disconnect
        self.disconnect_button = QPushButton("Disconnect")
        self.disconnect_button.setEnabled(False)
        self.disconnect_button.setCheckable(True)
        self.disconnect_button.clicked.connect(self.clicked_disconnect_button)

        self.set_name_button = QPushButton("Set client name")
        self.set_name_button.setCheckable(True)
        self.set_name_button.clicked.connect(self.clicked_set_client_name)

        self.name_input = QLineEdit()
        self.name_input.setText('Client name')
        self.name_input.textChanged.connect(self.set_client)

        self.message_label = QLabel('Enter you message:')
        self.message_input = QLineEdit()
        self.send_message_button = QPushButton('Send message')
        self.send_message_button.setCheckable(True)
        self.send_message_button.clicked.connect(self.clicked_send_message_button)



        form = QFormLayout()
        form.addRow(self.name_input, self.set_name_button)
        form.addRow("connect", self.connect_button)
        form.addRow("disconnect", self.disconnect_button)



        # layout = QVBoxLayout()

        # layout.addWidget(self.connect_button)
        # layout.addWidget(self.disconnect_button)
        # layout.addWidget(form)

        container = QWidget()
        container.setLayout(form)

        # Устанавливаем центральный виджет Window.

        self.setCentralWidget(container)

    def clicked_send_message_button(self):
        client.text = self.message_input.textChanged

    def clicked_set_client_name(self):
        self.set_name_button.setEnabled(False)
        self.connect_button.setEnabled(True)
        self.name_input.setEnabled(False)
        client.client_name = self.client_text_name


    def set_client(self, name):
        print(name)
        self.client_text_name = name

    def clicked_connect_button(self):
        self.connect_button.setEnabled(False)
        self.disconnect_button.setEnabled(True)
        client.start_chat

    def clicked_disconnect_button(self):
        client.close_connection
        self.disconnect_button.setEnabled(False)
        self.connect_button.setEnabled(True)



if __name__ == '__main__':


    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec())