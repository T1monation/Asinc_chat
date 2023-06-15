import sys
from PySide6.QtWidgets import QWidget, QApplication, QMainWindow, QMessageBox
from PySide6.QtGui import QStandardItemModel, QStandardItem, QBrush, QColor
from PySide6 import QtWidgets
from PySide6.QtCore import Slot, Qt, Signal, Slot, QThread
from time import sleep
import time
from client import Client
from ChatWindow.ui_form import Ui_ChatWindow
from client_gui import Client


client = Client()


class My_Window(QMainWindow):
    list_m = list()
    msg_list = None
    new_message = Signal(dict)
    start_flag = False
    # Переменная-хранилище QStandardItemModel
    clients_list_online_qt = None
    # Список клиентов онлайн
    clients_online_list = list()
    # Cписок друзей
    frends_list = list()
    # Переменная-хранилище QStandardItemModel
    frends_list_qt = None
    # Переменная - название текущего чата
    current_chat = str()
    # Хранилище непрочитанных сообщений для чатов
    chat_dict = dict()
    # словарь ключ - название чата, значение - индекс QComBox
    name_index_dict = dict()
    # "коробка" сообщений
    message_box = QMessageBox

    def __init__(self):
        super().__init__()
        self.ui = Ui_ChatWindow()
        self.ui.setupUi(self)

        self.ui.set_name_button.clicked.connect(self.clicked_set_client_name)
        self.ui.connect_button.clicked.connect(self.clicked_connect_button)
        self.ui.name_input.textChanged.connect(self.set_client)
        self.ui.disconnect_button.clicked.connect(
            self.clicked_disconnect_button)
        self.ui.send_to_chat_button.clicked.connect(
            self.clicked_send_to_chat_button)
        self.ui.input_msg_list.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.ui.input_msg_list.setWordWrap(True)
        self.ui.new_message.setEnabled(False)
        self.ui.frends_list.doubleClicked.connect(self.del_frend)
        self.ui.clients_online_list.doubleClicked.connect(self.add_frend)
        self.ui.comboBox.currentIndexChanged.connect(self.active_chat)
        self.ui.new_message.clicked.connect(self.upload_message)

        self.show()

    def clicked_set_client_name(self):
        self.ui.set_name_button.setEnabled(False)
        self.ui.connect_button.setEnabled(True)
        self.ui.name_input.setEnabled(False)
        client.client_name = self.client_text_name

    def clicked_connect_button(self):

        self.ui.connect_button.setEnabled(False)
        self.ui.disconnect_button.setEnabled(True)
        client.start_chat
        sleep(0.2)
        client.presense
        sleep(0.2)

    def set_client(self, name):
        self.client_text_name = name

    def clicked_disconnect_button(self):
        client.close_connection()
        self.ui.disconnect_button.setEnabled(False)
        self.ui.connect_button.setEnabled(True)

    def clicked_send_to_chat_button(self):
        client.send_message(self.ui.msg_to_chat.text())
        self.ui.msg_to_chat.clear()

    @Slot(dict)
    def get_new_message(self, message):
        if not self.msg_list:
            self.msg_list = QStandardItemModel()
            self.ui.input_msg_list.setModel(self.msg_list)
        if message["action"] == "msg":
            if message["name"] == "server":
                self.message_box.question(
                    self, "message", f"{message['name']}:\n{message['msg']}", QMessageBox.StandardButton.Ok)

            elif message["name"] == self.current_chat:
                self.message_writher(message)
            else:
                try:
                    self.chat_dict[message["name"]].append(message)
                except KeyError:
                    if message["name"] == "server":
                        pass
                    else:
                        if self.message_box.question(self, "Добавить в друзья?", f"Пользователь {message['name']} прислал сообщение", QMessageBox.StandardButton.Yes, QMessageBox.StandardButton.No) == QMessageBox.StandardButton.Yes:
                            print(type(message["name"]))
                            self.add_frend(message["name"])
                            sleep(0.5)
                            self.chat_dict[message["name"]] = []
                            self.chat_dict[message["name"]].append(message)
                            self.ui.new_message.setEnabled(True)
                        else:
                            pass
                else:
                    self.ui.new_message.setEnabled(True)
        if message["action"] == "get_contacts":
            if not self.clients_list_online_qt:
                self.clients_list_online_qt = QStandardItemModel()
            self.ui.clients_online_list.setModel(self.clients_list_online_qt)
            if not self.frends_list_qt:
                self.frends_list_qt = QStandardItemModel()
            self.ui.frends_list.setModel(self.frends_list_qt)
            clients_online_list = message["cli_online"]
            frends_list = message["frends"]
            for el in frends_list:
                self.chat_dict.setdefault(el, [])

            if clients_online_list == self.clients_online_list:
                pass
            else:
                self.clients_list_online_qt.clear()
                self.clients_online_list = clients_online_list
                for el in clients_online_list:
                    mess = QStandardItem(el)
                    mess.setEditable(False)
                    mess.setBackground(QBrush(QColor(0, 139, 139)))
                    mess.setTextAlignment(Qt.AlignHCenter)
                    self.clients_list_online_qt.appendRow(mess)
            if frends_list == self.frends_list:
                pass
            else:
                self.frends_list_qt.clear()
                self.frends_list = frends_list
                self.ui.comboBox.clear()
                # self.ui.comboBox.addItems(self.frends_list)
                i = 0
                for el in self.frends_list:
                    self.ui.comboBox.addItem(el)
                    self.name_index_dict[el] = i
                    i += 1
                for el in frends_list:
                    mess = QStandardItem(el)
                    mess.setEditable(False)
                    if el in self.clients_online_list:
                        mess.setBackground(QBrush(QColor(0, 139, 139)))
                    else:
                        mess.setBackground(QBrush(QColor(119, 136, 153)))
                    mess.setTextAlignment(Qt.AlignHCenter)
                    self.frends_list_qt.appendRow(mess)

    def message_writher(self, message):
        if message["name"] == self.client_text_name:
            mess = QStandardItem(
                f'Я:\n{message["msg"]}')
            mess.setEditable(False)
            mess.setBackground(QBrush(QColor(0, 255, 127)))
            mess.setTextAlignment(Qt.AlignRight)
        elif message["name"] == 'server':
            mess = QStandardItem(
                f'server:\n{message["msg"]}')
            mess.setEditable(False)
            mess.setBackground(QBrush(QColor(0, 255, 255)))
            mess.setTextAlignment(Qt.AlignHCenter)
        else:
            mess = QStandardItem(
                f'{message["name"]}:\n{message["msg"]}')
            mess.setEditable(False)
            mess.setBackground(QBrush(QColor(255, 213, 213)))
            mess.setTextAlignment(Qt.AlignLeft)
        self.msg_list.appendRow(mess)

    def del_frend(self, item):
        if isinstance(item, QStandardItem):
            client_to_del = item.data()
        if isinstance(item, str):
            client_to_del = item
        client.client_to_del(client_to_del)
        sleep(0.2)
        client.client_online_list

    def add_frend(self, item):
        if isinstance(item, QStandardItem):
            client_to_add = item.data()
        elif isinstance(item, str):
            client_to_add = item
        else:
            print(item, "\n", type(item))
            raise TypeError
        client.client_to_add(client_to_add)
        sleep(0.2)
        client.client_online_list

    def active_chat(self, el):
        self.current_chat = self.ui.comboBox.currentText()
        for el in self.chat_dict[self.ui.comboBox.currentText()]:
            self.message_writher(el)
        self.chat_dict[self.ui.comboBox.currentText()].clear()

    @property
    def new_mesage_finder(self):
        """
        метод-поисковик непросмотренных сообщений
        """
        self.find_flag = False
        update_chtat = None
        for el in self.chat_dict:
            if len(self.chat_dict[el]) != 0:
                self.find_flag = True
                self.ui.new_message.setEnabled(True)
                update_chtat = el
            else:
                self.ui.new_message.setEnabled(False)
        if update_chtat:
            self.upload_message(self.name_index_dict[update_chtat])

    def upload_message(self, index):
        """
        метод принимает индекс для comboBox, и переключает вкладку 
        """
        self.ui.comboBox.setCurrentIndex(index)
        self.new_mesage_finder


class MsgUpdater(QThread):
    """
    Класс, который в фоне проверяет наличие новых сообщений у клиента
    """
    new_message = Signal(dict)

    def run(self):
        while True:
            if not client.queue_read.empty():
                msg = client.queue_read.get()
                client.queue_read.task_done()
                self.new_message.emit(msg)


class OnlineListUpdater(QThread):
    """
    класс, суть которого запрашивать в фоне от сервера актуальную информацию о клиентах онлайн
    с интервалом времени в 10 секунд
    """
    online_list = Signal(list)
    temp_list = []

    def run(self):
        while True:
            sleep(2)
            client.client_online_list
            sleep(8)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = My_Window()
    msg_updater = MsgUpdater()
    online_status = OnlineListUpdater()
    window.ui.connect_button.clicked.connect(msg_updater.start)
    window.ui.connect_button.clicked.connect(online_status.start)
    msg_updater.new_message.connect(window.get_new_message)
    sys.exit(app.exec())
