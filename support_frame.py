import pyodbc
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

class SupportFrame(QWidget):
    data_support = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Thông Tin Liên Hệ Hỗ Trợ")
        self.setWindowIcon(QIcon("C:/Users/0x000000000000/Desktop/Python/images/logo.png"))
        self.setGeometry(760, 480, 400, 120)

        self.setStyleSheet("""
            background-color: #0b2a52;
            color: #FFF;
            font-weight: bold;
            font-size: 10pt;
        """)

        self.label_id = QLabel("Thông Tin Hỗ Trợ Qua Discord ChungLinhNhi:<br> https://...")
        layout = QVBoxLayout()
        layout.addWidget(self.label_id)  
        self.setLayout(layout)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = SupportFrame()
    window.show()
    sys.exit(app.exec_())
