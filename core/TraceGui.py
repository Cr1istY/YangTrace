import sys
import socket
from PySide6.QtWidgets import QWidget, QApplication, QTableWidgetItem, QHeaderView, QMessageBox
from YangTrace import Ui_Form
from YangTraceCore import get_address

class MainWindow(QWidget, Ui_Form):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.resultOutput.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.resultOutput.setRowCount(0)
        self.bind()

    def bind(self):
        self.getStart.clicked.connect(self.traceroute)

    def traceroute(self):
        target = self.webInput.text()
        if len(target) <= 3:
            self.show_dialog("输入的网址长度过小，请重新输入！")
            return
        max_ttl = 30
        try:
            target_ip = socket.gethostbyname(target)
        except socket.gaierror:
            print(f"Could not resolve {target}")
            self.show_dialog("输入的网址错误，找不到对应的IP地址！")
            return
        for ttl in range(1, max_ttl + 1):
            result = get_address(target_ip, ttl)
            print(result)
            self.add_row(result)
            if result[1] == target_ip:
                self.show_dialog(f"已到达目标 {target} ，ip：{target_ip}")
                return


    def add_row(self, result_list):
        row_position = self.resultOutput.rowCount()
        self.resultOutput.insertRow(row_position)
        for col, data in enumerate(result_list):
            item = QTableWidgetItem(str(data))
            self.resultOutput.setItem(row_position, col, item)
        QApplication.processEvents()


    def show_dialog(self, text):
        # 创建一个消息盒（弹窗）
        msg_box = QMessageBox()
        msg_box.setWindowTitle("提示")
        msg_box.setText(text)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()

