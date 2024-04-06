import sys
import pyodbc
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QApplication
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QIcon
class AddFrame(QWidget):
    data_added = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Thêm Sản Phẩm Mới")
        self.setWindowIcon(QIcon("C:/Users/0x000000000000/Desktop/Python/images/logo.png"))
        self.setFixedSize(400, 250)  # Kích thước cửa sổ

        # Thiết lập màu nền và các thuộc tính cho giao diện
        self.setStyleSheet("""
            background-color: #0b2a52;
            color: #FFF;
            font-weight: bold;
            font-size: 10pt;
        """)

        self.label_san_pham = QLabel("Sản Phẩm:")
        self.label_gia_tien = QLabel("Giá Tiền:")
        self.label_so_luong = QLabel("Số Lượng:")

        self.lineedit_san_pham = QLineEdit()
        self.lineedit_gia_tien = QLineEdit()
        self.lineedit_so_luong = QLineEdit()
        self.lineedit_so_luong.setText("1")
        self.lineedit_so_luong.setReadOnly(True)

        self.button_add = QPushButton("Thêm")

        # Thiết lập gợi ý cho phần nhập thông tin
        self.lineedit_san_pham.setPlaceholderText("Nhập Sản Phẩm")
        self.lineedit_gia_tien.setPlaceholderText("Nhập Giá Tiền")
        self.lineedit_so_luong.setPlaceholderText("Nhập Số Lượng")

        # Thiết lập cỡ chữ khi nhập là chữ thường
        self.lineedit_san_pham.setEchoMode(QLineEdit.Normal)
        self.lineedit_gia_tien.setEchoMode(QLineEdit.Normal)
        self.lineedit_so_luong.setEchoMode(QLineEdit.Normal)

        self.button_add.setFixedHeight(40)

        gradient_color = "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #07f5f1, stop:0.5 #15074a, stop:1 #f70576);"
        self.button_add.setStyleSheet(f"""
            QPushButton {{ 
                background-color: {gradient_color}; 
                color: #FFF; 
                border-radius: 20px; 
                font-weight: bold; 
                font-size: 12pt;
            }} 
            QPushButton:hover {{ border: 2px solid #FFF; }} 
            QPushButton:pressed {{ border: 4px solid #FFF; }}
        """)
        
        self.button_add.clicked.connect(self.add_data)

        layout = QVBoxLayout()
        layout.addWidget(self.label_san_pham)
        layout.addWidget(self.lineedit_san_pham)
        layout.addWidget(self.label_gia_tien)
        layout.addWidget(self.lineedit_gia_tien)
        layout.addWidget(self.label_so_luong)
        layout.addWidget(self.lineedit_so_luong)
        layout.addWidget(self.button_add)

        self.setLayout(layout)

    def add_data(self):
        server = 'DESKTOP-BHR2OIT\\GUNX'
        database = 'menu'
        username = 'sa'
        password = 'abc@123'

        conn_str = f'DRIVER=ODBC Driver 17 for SQL Server;SERVER={server};DATABASE={database};UID={username};PWD={password}'
        conn = pyodbc.connect(conn_str)

        cursor = conn.cursor()

        san_pham = self.lineedit_san_pham.text()
        gia_tien = self.lineedit_gia_tien.text()
        so_luong = self.lineedit_so_luong.text()

        try:
            gia_tien = float(gia_tien)
            if gia_tien <= 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Cảnh Báo", "Giá Tiền phải là số dương!")
            return

        query = "INSERT INTO dbo.products (San_Pham, Gia_Tien, So_Luong) VALUES (?, ?, ?)"
        cursor.execute(query, (san_pham, gia_tien, so_luong))

        conn.commit()

        QMessageBox.information(self, "Thông Báo", "Đã thêm sản phẩm mới thành công!")
        self.data_added.emit()

        conn.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AddFrame()
    window.show()
    sys.exit(app.exec_())
