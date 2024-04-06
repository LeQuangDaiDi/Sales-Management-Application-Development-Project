import pyodbc
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox
from PyQt5.QtCore import pyqtSignal, QSize
from PyQt5.QtGui import QIcon

class EditFrame(QWidget):
    data_updated = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Chỉnh Sửa Sản Phẩm")
        self.setWindowIcon(QIcon("C:/Users/0x000000000000/Desktop/Python/images/logo.png"))
        self.setGeometry(750, 340, 400, 200)

        self.setStyleSheet("""
            background-color: #0b2a52;
            color: #FFF;
            font-weight: bold;
            font-size: 10pt;
        """)
        gradient_color = "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #07f5f1, stop:0.5 #15074a, stop:1 #f70576);"
        self.label_id = QLabel("ID Sản Phẩm:")
        self.lineedit_id = QLineEdit()
        self.lineedit_id.setPlaceholderText("Nhập ID Sản Phẩm")
        self.lineedit_id.setEchoMode(QLineEdit.Normal)

        self.label_san_pham = QLabel("Sản Phẩm:")
        self.lineedit_san_pham = QLineEdit()
        self.lineedit_san_pham.setPlaceholderText("Nhập Sản Phẩm")
        self.lineedit_san_pham.setEchoMode(QLineEdit.Normal)

        self.label_gia_tien = QLabel("Giá Tiền:")
        self.lineedit_gia_tien = QLineEdit()
        self.lineedit_gia_tien.setPlaceholderText("Nhập Giá Tiền")
        self.lineedit_gia_tien.setEchoMode(QLineEdit.Normal)

        self.button_load = QPushButton("Tìm")
        self.button_load.setStyleSheet(f"""
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
        self.button_load.clicked.connect(self.load_data)

        self.button_save = QPushButton("Lưu")
        self.button_save.setStyleSheet(f"""
            QPushButton {{ 
                background-color: {gradient_color}; 
                color: #FFF; 
                border-radius: 10px; 
                font-weight: bold; 
                font-size: 14pt;
            }} 
            QPushButton:hover {{ border: 2px solid #FFF; }} 
            QPushButton:pressed {{ border: 4px solid #FFF; }}
        """)
        self.button_save.clicked.connect(self.save_data)

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.lineedit_id)
        input_layout.addWidget(self.button_load)

        layout = QVBoxLayout()
        layout.addWidget(self.label_id)
        layout.addLayout(input_layout)
        layout.addWidget(self.label_san_pham)
        layout.addWidget(self.lineedit_san_pham)
        layout.addWidget(self.label_gia_tien)
        layout.addWidget(self.lineedit_gia_tien)
        layout.addWidget(self.button_save)

        self.setLayout(layout)

    def load_data(self):
        server = 'DESKTOP-BHR2OIT\\GUNX'
        database = 'menu'
        username = 'sa'
        password = 'abc@123'

        conn_str = f'DRIVER=ODBC Driver 17 for SQL Server;SERVER={server};DATABASE={database};UID={username};PWD={password}'
        conn = pyodbc.connect(conn_str)

        cursor = conn.cursor()

        id_san_pham = self.lineedit_id.text()

        try:
            id_san_pham = int(id_san_pham)
        except ValueError:
            QMessageBox.warning(self, "Cảnh Báo", "ID Sản Phẩm phải là số nguyên!")
            return

        query = "SELECT San_Pham, Gia_Tien FROM dbo.products WHERE ID = ?"
        cursor.execute(query, (id_san_pham,))
        row = cursor.fetchone()

        if row:
            self.lineedit_san_pham.setText(row[0])
            self.lineedit_gia_tien.setText(str(row[1]))
        else:
            QMessageBox.warning(self, "Cảnh Báo", "Không tìm thấy sản phẩm có ID này!")

        conn.close()

    def save_data(self):
        server = 'DESKTOP-BHR2OIT\\GUNX'
        database = 'menu'
        username = 'sa'
        password = 'abc@123'

        conn_str = f'DRIVER=ODBC Driver 17 for SQL Server;SERVER={server};DATABASE={database};UID={username};PWD={password}'
        conn = pyodbc.connect(conn_str)

        cursor = conn.cursor()

        id_san_pham = self.lineedit_id.text()
        san_pham = self.lineedit_san_pham.text()
        gia_tien = self.lineedit_gia_tien.text()

        try:
            id_san_pham = int(id_san_pham)
        except ValueError:
            QMessageBox.warning(self, "Cảnh Báo", "ID Sản Phẩm phải là số nguyên!")
            return

        try:
            gia_tien = float(gia_tien)
            if gia_tien <= 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Cảnh Báo", "Giá Tiền phải là số dương!")
            return

        query = "UPDATE dbo.products SET San_Pham = ?, Gia_Tien = ? WHERE ID = ?"
        cursor.execute(query, (san_pham, gia_tien, id_san_pham))
        conn.commit()

        if cursor.rowcount > 0:
            QMessageBox.information(self, "Thông Báo", "Đã cập nhật thông tin sản phẩm!")
            self.data_updated.emit()
        else:
            QMessageBox.warning(self, "Cảnh Báo", "Không tìm thấy sản phẩm có ID này!")

        conn.close()
