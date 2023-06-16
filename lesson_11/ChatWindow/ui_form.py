# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'formNJkxeY.ui'
##
## Created by: Qt User Interface Compiler version 6.2.4
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QLabel, QLineEdit,
    QListView, QPushButton, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_ChatWindow(object):
    def setupUi(self, ChatWindow):
        if not ChatWindow.objectName():
            ChatWindow.setObjectName(u"ChatWindow")
        ChatWindow.resize(871, 600)
        self.verticalLayoutWidget = QWidget(ChatWindow)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(10, 510, 291, 81))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.verticalLayoutWidget)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label, 0, Qt.AlignHCenter)

        self.msg_to_chat = QLineEdit(self.verticalLayoutWidget)
        self.msg_to_chat.setObjectName(u"msg_to_chat")

        self.verticalLayout.addWidget(self.msg_to_chat)

        self.send_to_chat_button = QPushButton(self.verticalLayoutWidget)
        self.send_to_chat_button.setObjectName(u"send_to_chat_button")

        self.verticalLayout.addWidget(self.send_to_chat_button)

        self.verticalLayoutWidget_2 = QWidget(ChatWindow)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(9, 49, 291, 451))
        self.verticalLayout_2 = QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.input_msg_list = QListView(self.verticalLayoutWidget_2)
        self.input_msg_list.setObjectName(u"input_msg_list")

        self.verticalLayout_2.addWidget(self.input_msg_list)

        self.verticalLayoutWidget_3 = QWidget(ChatWindow)
        self.verticalLayoutWidget_3.setObjectName(u"verticalLayoutWidget_3")
        self.verticalLayoutWidget_3.setGeometry(QRect(319, 259, 241, 331))
        self.verticalLayout_3 = QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.clients_online_list = QListView(self.verticalLayoutWidget_3)
        self.clients_online_list.setObjectName(u"clients_online_list")

        self.verticalLayout_3.addWidget(self.clients_online_list)

        self.label_2 = QLabel(ChatWindow)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(370, 230, 151, 21))
        self.frends_list = QListView(ChatWindow)
        self.frends_list.setObjectName(u"frends_list")
        self.frends_list.setGeometry(QRect(590, 260, 239, 329))
        self.label_3 = QLabel(ChatWindow)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(650, 230, 151, 21))
        self.comboBox = QComboBox(ChatWindow)
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setGeometry(QRect(10, 20, 291, 22))
        self.new_message = QPushButton(ChatWindow)
        self.new_message.setObjectName(u"new_message")
        self.new_message.setGeometry(QRect(320, 20, 131, 51))
        self.connect_button = QPushButton(ChatWindow)
        self.connect_button.setObjectName(u"connect_button")
        self.connect_button.setEnabled(True)
        self.connect_button.setGeometry(QRect(650, 90, 174, 24))
        self.disconnect_button = QPushButton(ChatWindow)
        self.disconnect_button.setObjectName(u"disconnect_button")
        self.disconnect_button.setEnabled(False)
        self.disconnect_button.setGeometry(QRect(650, 130, 174, 24))
        self.label_4 = QLabel(ChatWindow)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(580, 30, 61, 16))
        font = QFont()
        font.setPointSize(14)
        self.label_4.setFont(font)
        self.label_4.setLayoutDirection(Qt.LeftToRight)
        self.client_name_label = QLabel(ChatWindow)
        self.client_name_label.setObjectName(u"client_name_label")
        self.client_name_label.setGeometry(QRect(640, 30, 171, 21))
        self.client_name_label.setFont(font)

        self.retranslateUi(ChatWindow)

        QMetaObject.connectSlotsByName(ChatWindow)
    # setupUi

    def retranslateUi(self, ChatWindow):
        ChatWindow.setWindowTitle(QCoreApplication.translate("ChatWindow", u"ChatWindow", None))
        self.label.setText(QCoreApplication.translate("ChatWindow", u"Tipe your message:", None))
        self.send_to_chat_button.setText(QCoreApplication.translate("ChatWindow", u"Send to chat", None))
        self.label_2.setText(QCoreApplication.translate("ChatWindow", u"Clients online list :", None))
        self.label_3.setText(QCoreApplication.translate("ChatWindow", u"Frends list:", None))
        self.new_message.setText(QCoreApplication.translate("ChatWindow", u"Read new message", None))
        self.connect_button.setText(QCoreApplication.translate("ChatWindow", u"Connect", None))
        self.disconnect_button.setText(QCoreApplication.translate("ChatWindow", u"Disconnect", None))
        self.label_4.setText(QCoreApplication.translate("ChatWindow", u"Client:", None))
        self.client_name_label.setText(QCoreApplication.translate("ChatWindow", u"TextLabel", None))
    # retranslateUi

