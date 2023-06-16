import sys
from PySide6.QtWidgets import QApplication, QMessageBox, QDialog, QMainWindow
from ChatWindow.ui_first_form import Ui_Dialog
import hashlib

SALT = b'my_sickret_salt'


class StartWindow(QDialog):
    message_box = QMessageBox()
    register_flag = False

    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        if self.ui.checkBox_exist_user.isChecked():
            self.ui.loginLineEdit.setEnabled(True)
            self.ui.passwordLineEdit.setEnabled(True)
            self.ui.join_chat_button.setEnabled(True)
            self.ui.loginLineEdit_2.setEnabled(False)
            self.ui.passwordLineEdit_2.setEnabled(False)
            self.ui.confrimPasswordLineEdit.setEnabled(False)
            self.ui.register_button.setEnabled(False)

        if self.ui.checkBox_new_user.isChecked():
            self.ui.loginLineEdit_2.setEnabled(True)
            self.ui.passwordLineEdit_2.setEnabled(True)
            self.ui.confrimPasswordLineEdit.setEnabled(True)
            self.ui.register_button.setEnabled(True)
            self.ui.loginLineEdit.setEnabled(False)
            self.ui.passwordLineEdit.setEnabled(False)
            self.ui.join_chat_button.setEnabled(False)

        self.ui.register_button.clicked.connect(self.button_register_clicked)
        self.ui.join_chat_button.clicked.connect(self.button_join_clicked)
        self.ui.pushButton_exit.clicked.connect(self.exit)

        self.show()

    def button_register_clicked(self):
        self.login = self.ui.loginLineEdit_2.text()
        _password = self.ui.passwordLineEdit_2.text()
        _confrim_password = self.ui.confrimPasswordLineEdit.text()

        if _password != _confrim_password:
            self.message_box.critical(self, "Entered passwords do not match!",
                                      QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.NoButton)

        else:
            self.register_flag = True
            self.hashed_password = hashlib.pbkdf2_hmac(
                'sha256', bytes(_password, 'utf-8'), SALT, 10000)
            _password = None
            _confrim_password = None

    def button_join_clicked(self):
        self.login = self.ui.loginLineEdit.text()
        self.hashed_password = hashlib.pbkdf2_hmac(
            'sha256', bytes(self.ui.passwordLineEdit.text(), 'utf-8'), SALT, 10000)

    def exit(self):
        exit(0)


if __name__ == '__main__':
    app = QApplication([])
    dial = StartWindow()
    app.exec()
