import sys
from PySide6.QtWidgets import QWidget, QApplication, QMainWindow, QLabel, QDialog, QPushButton, QLineEdit


class AddToFrend(QDialog):
    def __init__(self, name):
        super().__init__()
        self.new_client_name = name
        print('dialog')
        self.ok_pressed = False

        self.setWindowTitle('Алярм!')
        self.setFixedSize(250, 140)

        self.label = QLabel(
            f'Полученно сообщенее от пользователя {self.new_client_name}\nдобавим в список друзей?', self)
        self.label.move(10, 10)
        self.label.setFixedSize(150, 10)

        self.client_name = QLineEdit(self)
        self.client_name.setFixedSize(154, 20)
        self.client_name.move(10, 30)

        self.btn_ok = QPushButton('Да', self)
        self.btn_ok.move(10, 60)
        self.btn_ok.clicked.connect(self.click)

        self.btn_cancel = QPushButton('Нет', self)
        self.btn_cancel.move(90, 60)
        self.btn_cancel.clicked.connect(qApp.exit)

        self.show()

    # Обработчик кнопки ОК, если поле вводе не пустое, ставим флаг и завершаем приложение.
    def click(self):
        if self.client_name.text():
            self.ok_pressed = True
            qApp.exit()


if __name__ == '__main__':
    app = QApplication([])
    dial = AddToFrend()
    app.exec()
