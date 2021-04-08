from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
import sys
import msg_form
import msg


class Win(QMainWindow):
    def __init__(self):
        QWidget.__init__(self, None)
        self.ui = msg_form.Ui_Dialog()
        self.ui.setupUi(self)

        self.clear()

        # Назначение функций кнопкам
        self.ui.pushButton_send.clicked.connect(self.send)
        self.ui.pushButton_clear.clicked.connect(self.clear)
        self.ui.pushButton_ok.clicked.connect(self.close)

    # Извлечение сообщения из поля ввода и его отправка
    def send(self):
        inp_msg = self.ui.textEdit.toPlainText()
        char_len = len(inp_msg)
        if 0 < char_len < 250:
            received_msg, output = msg.start_transfer(inp_msg)
            self.show_all()
            self.ui.textEdit_2.setText(output)
            self.ui.textEdit_3.setText(received_msg)
        elif char_len > 0:
            self.show_all()
            self.ui.textEdit_2.setText('Вы ввели ' + str(char_len) + ' символов!\n' +
                                       'Количество символов в сообщении должно быть в ределах (0, 250)')
            self.ui.textEdit_3.setText('Сообщение не было передано')

    # Очистка текстовых полей и скрытие лишних элементов
    def clear(self):
        self.ui.textEdit.setText('')
        self.ui.textEdit_2.setText('')
        self.ui.textEdit_3.setText('')

        self.ui.textEdit_2.hide()
        self.ui.textEdit_3.hide()
        self.ui.label.hide()
        self.ui.label_2.hide()

        self.ui.pushButton_ok.setDisabled(True)

    # Отображение всех элементов
    def show_all(self):
        self.ui.textEdit_2.setText('')
        self.ui.textEdit_3.setText('')

        self.ui.textEdit_2.show()
        self.ui.textEdit_3.show()
        self.ui.label.show()
        self.ui.label_2.show()

        self.ui.pushButton_ok.setDisabled(False)


# Инициализация окна приложения
app = QApplication(sys.argv)
win = Win()
win.setWindowTitle('Msg')
win.show()
win.move(650, 200)
sys.exit(app.exec_())

