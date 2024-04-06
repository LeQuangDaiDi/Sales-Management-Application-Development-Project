import pyodbc
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon
class DeleteFrame(QWidget):
    data_deleted = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Xoá Sản Phẩm")
        self.setWindowIcon(QIcon("C:/Users/0x000000000000/Desktop/Python/images/logo.png"))
        self.setGeometry(760, 480, 400, 120)

        self.setStyleSheet("""
            background-color: #0b2a52;
            color: #FFF;
            font-weight: bold;
            font-size: 10pt;
        """)

        self.label_id = QLabel("ID Sản Phẩm:")
        self.lineedit_id = QLineEdit()
        self.lineedit_id.setPlaceholderText("Nhập ID Sản Phẩm")
        self.lineedit_id.setEchoMode(QLineEdit.Normal)
        gradient_color = "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #07f5f1, stop:0.5 #15074a, stop:1 #f70576);"
        self.button_delete = QPushButton("Xoá")
        self.button_delete.setStyleSheet(f"""
            QPushButton {{ 
                background-color: {gradient_color}; 
                color: #FFF; 
                border-radius: 10px; 
                font-weight: bold; 
                font-size: 15pt;
            }} 
            QPushButton:hover {{ border: 2px solid #FFF; }} 
            QPushButton:pressed {{ border: 4px solid #FFF; }}
        """)
        self.button_delete.clicked.connect(self.delete_data)

        layout = QVBoxLayout()
        layout.addWidget(self.label_id)
        layout.addWidget(self.lineedit_id)
        layout.addWidget(self.button_delete)

        self.setLayout(layout)

    def delete_data(self):
        server = 'DESKTOP-BHR2OIT\\GUNX'
        database = 'menu'
        username = 'sa'
        password = 'abc@123'

        conn_str = f'DRIVER=ODBC Driver 17 for SQL Server;SERVER={server};DATABASE={database};UID={username};PWD={password}'
        conn = pyodbc.connect(conn_str)

        cursor = conn.cursor()

        id_san_pham = self.lineedit_id.text()

        try:
            id_san_pham = int(id_san_pham)  # Chuyển đổi ID sang kiểu số nguyên
        except ValueError:
            QMessageBox.warning(self, "Cảnh Báo", "ID Sản Phẩm phải là số nguyên!")
            return

        query = "DELETE FROM dbo.products WHERE ID = ?"
        cursor.execute(query, (id_san_pham,))
        conn.commit()

        if cursor.rowcount > 0:
            QMessageBox.information(self, "Thông Báo", "Đã xoá sản phẩm thành công!")
            self.data_deleted.emit()  # Phát tín hiệu đã xoá dữ liệu thành công
        else:
            QMessageBox.warning(self, "Cảnh Báo", "Không tìm thấy sản phẩm có ID này!")

        conn.close()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DeleteFrame()
    window.show()
    sys.exit(app.exec_())
