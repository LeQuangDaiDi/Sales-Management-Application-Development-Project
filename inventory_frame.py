from PyQt5.QtWidgets import QMainWindow, QApplication, QFrame, QPushButton, QVBoxLayout, QTableWidget, QTableWidgetItem, QDialog, QLabel, QLineEdit, QComboBox, QHBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import pyodbc
import random
import string

class StyledButton(QPushButton):
    def __init__(self, text, gradient_color, text_color, font_weight, font_size, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet(f"QPushButton {{ background: {gradient_color}; color: {text_color}; border-radius: 15px; font-weight: {font_weight}; font-size: {font_size}; padding: 10px 20px; }} QPushButton:hover {{ border: 3px solid #FFF; }} QPushButton:pressed {{ border: 5px solid #FFF; }}")


class AddItemDialog(QDialog):
    def __init__(self, cursor):
        super().__init__()
        self.setWindowTitle("Thêm mục mới")

        background_color = "#0b2a52"
        text_color_white = "#FFF"
        font_weight = "bold"
        font_size_large = "12pt"
        gradient_color = "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #07f5f1, stop:0.5 #15074a, stop:1 #f70576);"

        self.setStyleSheet(f"background-color: {background_color}; color: {text_color_white}; font-weight: {font_weight}; font-size: {font_size_large};")

        screen_geometry = QApplication.primaryScreen().geometry()
        dialog_width = 500
        dialog_height = 400
        x = (screen_geometry.width() - dialog_width) / 2
        y = (screen_geometry.height() - dialog_height) / 2
        self.setGeometry(int(x), int(y), int(dialog_width), int(dialog_height))

        layout = QVBoxLayout()

        self.label1 = QLabel("Nguyên Liệu:", self)
        self.label1.setStyleSheet("color: #FFF; font-weight: bold; font-size: 12pt;")
        layout.addWidget(self.label1)
        self.lineEdit1 = QLineEdit(self)
        self.lineEdit1.setStyleSheet("background-color: #FFF; color: #000; border-radius: 15px;")
        self.lineEdit1.setPlaceholderText("Nhập nguyên liệu...")
        layout.addWidget(self.lineEdit1)

        self.label2 = QLabel("Số Lượng:", self)
        self.label2.setStyleSheet("color: #FFF; font-weight: bold; font-size: 12pt;")
        layout.addWidget(self.label2)
        self.lineEdit2 = QLineEdit(self)
        self.lineEdit2.setStyleSheet("background-color: #FFF; color: #000; border-radius: 15px;")
        self.lineEdit2.setPlaceholderText("Nhập số lượng...")
        layout.addWidget(self.lineEdit2)

        self.label3 = QLabel("Đơn Vị:", self)
        self.label3.setStyleSheet("color: #FFF; font-weight: bold; font-size: 12pt;")
        layout.addWidget(self.label3)
        self.comboBox = QComboBox(self)
        self.comboBox.addItems(["Kilogram", "Bịch", "Hộp", "Lít", "Lốc", "Bình"])
        self.comboBox.setStyleSheet("background-color: #FFF; color: #000; border-radius: 15px;")
        layout.addWidget(self.comboBox)

        self.label4 = QLabel("Giá Nhập:", self)
        self.label4.setStyleSheet("color: #FFF; font-weight: bold; font-size: 12pt;")
        layout.addWidget(self.label4)
        self.lineEdit4 = QLineEdit(self)
        self.lineEdit4.setStyleSheet("background-color: #FFF; color: #000; border-radius: 15px;")
        self.lineEdit4.setPlaceholderText("Nhập giá nhập...")
        layout.addWidget(self.lineEdit4)

        layout.addSpacing(30)  

        self.button_save = StyledButton("Lưu", gradient_color, text_color_white, font_weight, font_size_large, self)
        self.button_save.clicked.connect(self.save_item)
        layout.addWidget(self.button_save)

        self.setLayout(layout)

        self.cursor = cursor

    def save_item(self):
        nguyen_lieu = self.lineEdit1.text()
        so_luong = self.lineEdit2.text()
        don_vi = self.comboBox.currentText()
        gia_nhap = self.lineEdit4.text()
        
        if nguyen_lieu and so_luong and don_vi and gia_nhap:
            try:
                item_id = self.generate_unique_id()

                self.cursor.execute("INSERT INTO dbo.inventory (ID, Nguyen_Lieu, So_Luong, Don_Vi, Gia_Nhap) VALUES (?, ?, ?, ?, ?)", 
                                    (item_id, nguyen_lieu, so_luong, don_vi, gia_nhap))
                self.cursor.connection.commit()
                self.accept()
            except Exception as e:
                print("Error saving item:", e)

    def generate_unique_id(self):
        while True:
            item_id = ''.join(random.choices(string.digits, k=6))
            self.cursor.execute("SELECT COUNT(*) FROM dbo.inventory WHERE ID=?", (item_id,))
            count = self.cursor.fetchone()[0]
            if count == 0:
                return item_id

class InventoryFrame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kho Hàng")
        self.setWindowIcon(QIcon("C:/Users/0x000000000000/Desktop/Python/images/logo.png"))
        self.setGeometry(240, 50, 1440, 960)
        self.setStyleSheet("background-color: #0b2a52;")

        self.inner_frame = QFrame(self)
        self.inner_frame.setGeometry(20, 20, 1400, 800)
        self.inner_frame.setStyleSheet("background-color: #e4f7f7;")

        self.layout = QVBoxLayout(self.inner_frame)

        self.table = QTableWidget()
        self.layout.addWidget(self.table)

        self.connect_db()
        self.populate_inventory_table()

        gradient_color = "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #07f5f1, stop:0.5 #15074a, stop:1 #f70576);"

        text_color_white = "#FFF"
        font_weight = "bold"
        font_size_large = "12pt"

        self.button_add = StyledButton("Thêm", gradient_color, text_color_white, font_weight, font_size_large, self)
        self.button_add.setGeometry(20, 840, 460, 100)
        self.button_add.clicked.connect(self.show_add_item_dialog)

        self.button_delete = StyledButton("Xoá", gradient_color, text_color_white, font_weight, font_size_large, self)
        self.button_delete.setGeometry(490, 840, 460, 100)
        self.button_delete.clicked.connect(self.show_delete_item_dialog)

        self.button_edit = StyledButton("Sửa", gradient_color, text_color_white, font_weight, font_size_large, self)
        self.button_edit.setGeometry(960, 840, 460, 100)
        self.button_edit.clicked.connect(self.show_edit_item_dialog)


    def connect_db(self):
        try:
            self.connection = pyodbc.connect('DRIVER={SQL Server};SERVER=DESKTOP-BHR2OIT\GUNX;DATABASE=menu;UID=sa;PWD=abc@123')
            self.cursor = self.connection.cursor()
        except Exception as e:
            print("Error connecting to database:", e)

    def populate_inventory_table(self):
        try:
            self.cursor.execute("SELECT ID, Nguyen_Lieu, So_Luong, Don_Vi, Gia_Nhap FROM dbo.inventory")
            rows = self.cursor.fetchall()

            self.table.setColumnCount(5)
            self.table.setHorizontalHeaderLabels(['ID', 'Nguyên Liệu', 'Số Lượng', 'Đơn Vị', 'Giá Nhập'])

            self.table.setRowCount(len(rows))

            for i, row in enumerate(rows):
                for j, col in enumerate(row):
                    item = QTableWidgetItem()
                    if j in [0, 2, 3]:
                        item.setTextAlignment(Qt.AlignCenter)
                    if j == 4:
                        col = "{:,.0f}".format(float(col))
                        item.setText(col)
                        item.setTextAlignment(Qt.AlignCenter)
                    else:
                        item.setText(str(col))
                    self.table.setItem(i, j, item)

            self.table.verticalHeader().setVisible(False)

            self.table.setColumnWidth(0, 200)
            self.table.setColumnWidth(1, 557)
            self.table.setColumnWidth(2, 150)
            self.table.setColumnWidth(3, 150)
            self.table.setColumnWidth(4, 300)

        except Exception as e:
            print("Error executing query:", e)

    def show_add_item_dialog(self):
        dialog = AddItemDialog(self.cursor)
        if dialog.exec_() == QDialog.Accepted:
            self.populate_inventory_table()

    def show_delete_item_dialog(self):
        dialog = DeleteItemDialog(self.cursor)
        if dialog.exec_() == QDialog.Accepted:
            self.populate_inventory_table()
    def show_edit_item_dialog(self):
        dialog = EditItemDialog(self.cursor)
        if dialog.exec_() == QDialog.Accepted:
            self.populate_inventory_table()

class DeleteItemDialog(QDialog):
    def __init__(self, cursor):
        super().__init__()
        self.setWindowTitle("Xoá mục")

        self.cursor = cursor

        background_color = "#0b2a52"
        text_color_white = "#FFF"
        font_weight = "bold"
        font_size_large = "12pt"
        gradient_color = "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #07f5f1, stop:0.5 #15074a, stop:1 #f70576);"

        self.setStyleSheet(f"background-color: {background_color}; color: {text_color_white}; font-weight: {font_weight}; font-size: {font_size_large};")

        screen_geometry = QApplication.primaryScreen().geometry()
        dialog_width = 500
        dialog_height = 200
        x = (screen_geometry.width() - dialog_width) / 2
        y = (screen_geometry.height() - dialog_height) / 2
        self.setGeometry(int(x), int(y), int(dialog_width), int(dialog_height))

        layout = QVBoxLayout()

        self.label_id = QLabel("Nhập ID mục cần xoá:", self)
        self.label_id.setStyleSheet("color: #FFF; font-weight: bold; font-size: 12pt;")
        layout.addWidget(self.label_id)
        self.lineEdit_id = QLineEdit(self)
        self.lineEdit_id.setStyleSheet("background-color: #FFF; color: #000; border-radius: 15px;")
        self.lineEdit_id.setPlaceholderText("Nhập ID mục cần xoá...")
        layout.addWidget(self.lineEdit_id)

        self.button_delete = StyledButton("Xoá", gradient_color, text_color_white, font_weight, font_size_large, self)
        self.button_delete.clicked.connect(self.delete_item)
        layout.addWidget(self.button_delete)

        self.setLayout(layout)

    def delete_item(self):
        id = self.lineEdit_id.text()
        if id:
            try:
                self.cursor.execute("DELETE FROM dbo.inventory WHERE ID=?", (id,))
                self.cursor.connection.commit()
                self.accept()
            except Exception as e:
                print("Error deleting item:", e)

class EditItemDialog(QDialog):
    def __init__(self, cursor):
        super().__init__()
        self.setWindowTitle("Sửa mục")

        self.cursor = cursor

        background_color = "#0b2a52"
        text_color_white = "#FFF"
        font_weight = "bold"
        font_size_large = "12pt"
        gradient_color = "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #07f5f1, stop:0.5 #15074a, stop:1 #f70576);"

        self.setStyleSheet(f"background-color: {background_color}; color: {text_color_white}; font-weight: {font_weight}; font-size: {font_size_large};")

        screen_geometry = QApplication.primaryScreen().geometry()
        dialog_width = 500
        dialog_height = 200
        x = (screen_geometry.width() - dialog_width) / 2
        y = (screen_geometry.height() - dialog_height) / 2
        self.setGeometry(int(x), int(y), int(dialog_width), int(dialog_height))

        layout = QVBoxLayout()

        self.label_id = QLabel("Nhập ID mục cần sửa:", self)
        self.label_id.setStyleSheet("color: #FFF; font-weight: bold; font-size: 12pt;")
        layout.addWidget(self.label_id)
        
        self.horizontalLayout = QHBoxLayout()

        self.lineEdit_id = QLineEdit(self)
        self.lineEdit_id.setStyleSheet("background-color: #FFF; color: #000; border-radius: 15px;")
        self.lineEdit_id.setPlaceholderText("Nhập ID mục cần sửa...")
        self.horizontalLayout.addWidget(self.lineEdit_id)

        self.button_find = StyledButton("Tìm", gradient_color, text_color_white, font_weight, font_size_large, self)
        self.button_find.clicked.connect(self.find_item)
        self.horizontalLayout.addWidget(self.button_find)

        layout.addLayout(self.horizontalLayout)

        self.label1 = QLabel("Nguyên Liệu mới:", self)
        self.label1.setStyleSheet("color: #FFF; font-weight: bold; font-size: 12pt;")
        layout.addWidget(self.label1)
        self.lineEdit1 = QLineEdit(self)
        self.lineEdit1.setStyleSheet("background-color: #FFF; color: #000; border-radius: 15px;")
        self.lineEdit1.setPlaceholderText("Nhập nguyên liệu mới...")
        layout.addWidget(self.lineEdit1)

        self.label2 = QLabel("Số Lượng mới:", self)
        self.label2.setStyleSheet("color: #FFF; font-weight: bold; font-size: 12pt;")
        layout.addWidget(self.label2)
        self.lineEdit2 = QLineEdit(self)
        self.lineEdit2.setStyleSheet("background-color: #FFF; color: #000; border-radius: 15px;")
        self.lineEdit2.setPlaceholderText("Nhập số lượng mới...")
        layout.addWidget(self.lineEdit2)

        self.label3 = QLabel("Đơn Vị mới:", self)
        self.label3.setStyleSheet("color: #FFF; font-weight: bold; font-size: 12pt;")
        layout.addWidget(self.label3)
        self.comboBox = QComboBox(self)
        self.comboBox.addItems(["Kilogram", "Bịch", "Hộp", "Lít", "Lốc", "Bình"])
        self.comboBox.setStyleSheet("background-color: #FFF; color: #000; border-radius: 15px;")
        layout.addWidget(self.comboBox)

        self.label4 = QLabel("Giá Nhập mới:", self)
        self.label4.setStyleSheet("color: #FFF; font-weight: bold; font-size: 12pt;")
        layout.addWidget(self.label4)
        self.lineEdit4 = QLineEdit(self)
        self.lineEdit4.setStyleSheet("background-color: #FFF; color: #000; border-radius: 15px;")
        self.lineEdit4.setPlaceholderText("Nhập giá nhập mới...")
        layout.addWidget(self.lineEdit4)

        self.button_save = StyledButton("Lưu", gradient_color, text_color_white, font_weight, font_size_large, self)
        self.button_save.clicked.connect(self.edit_item)
        layout.addWidget(self.button_save)

        self.setLayout(layout)

    def find_item(self):
        id = self.lineEdit_id.text()
        if id:
            try:
                self.cursor.execute("SELECT Nguyen_Lieu, So_Luong, Don_Vi, Gia_Nhap FROM dbo.inventory WHERE ID=?", (id,))
                row = self.cursor.fetchone()
                if row:
                    nguyen_lieu, so_luong, don_vi, gia_nhap = row
                    self.lineEdit1.setText(nguyen_lieu)
                    self.lineEdit2.setText(str(so_luong))
                    index = self.comboBox.findText(don_vi)
                    if index >= 0:
                        self.comboBox.setCurrentIndex(index)
                    self.lineEdit4.setText(str(gia_nhap))
                else:
                    QMessageBox.warning(self, "Thông báo", "Không tìm thấy sản phẩm có ID này.")
            except Exception as e:
                print("Error finding item:", e)

    def edit_item(self):
        id = self.lineEdit_id.text()
        nguyen_lieu = self.lineEdit1.text()
        so_luong = self.lineEdit2.text()
        don_vi = self.comboBox.currentText()
        gia_nhap = self.lineEdit4.text()

        if id and nguyen_lieu and so_luong and don_vi and gia_nhap:
            try:
                self.cursor.execute("UPDATE dbo.inventory SET Nguyen_Lieu=?, So_Luong=?, Don_Vi=?, Gia_Nhap=? WHERE ID=?", 
                                    (nguyen_lieu, so_luong, don_vi, gia_nhap, id))
                self.cursor.connection.commit()
                self.accept()
            except Exception as e:
                print("Error editing item:", e)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    inventory_frame = InventoryFrame()
    inventory_frame.show()
    sys.exit(app.exec_())
