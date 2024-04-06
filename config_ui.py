from PyQt5.QtWidgets import QMainWindow, QApplication, QFrame, QPushButton, QLabel
from PyQt5.QtCore import Qt, QDateTime, QTimer
from PyQt5.QtGui import QIcon
from menu_frame import MenuFrame
from add_frame import AddFrame
from support_frame import SupportFrame
from delete_frame import DeleteFrame
from edit_frame import EditFrame  
from inventory_frame import InventoryFrame
from PyQt5.QtGui import QClipboard

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        gradient_color = "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #07f5f1, stop:0.5 #15074a, stop:1 #f70576);"
        text_color_white = "#FFF"  
        font_weight = "bold"
        font_size_large = "12pt"
        self.setWindowTitle("Duty-Coffee")
        self.setWindowIcon(QIcon("C:/Users/0x000000000000/Desktop/Python/images/logo.png"))
        self.setGeometry(0, 0, 1920, 1080)
        self.setStyleSheet("background-color: #0b2a52;")

        self.frame1 = MenuFrame(self)
        self.frame1.setGeometry(20, 20, 1000, 600)
        self.frame1.setStyleSheet("background-color: #e4f7f7;")

        self.frame2 = QFrame(self)
        self.frame2.setGeometry(1040, 20, 490, 600)
        self.frame2.setStyleSheet("background-color: #e4f7f7;")

        self.create_order_button = QPushButton("Tạo Đơn", self)
        self.create_order_button.setGeometry(1390, 580, 130, 30)
        self.create_order_button.setStyleSheet(f"QPushButton {{ background: {gradient_color}; color: {text_color_white}; border-radius: 15px; font-weight: {font_weight}; font-size: {font_size_large}; }} QPushButton:hover {{ border: 2px solid #fc057d; }} QPushButton:pressed {{ border: 4px solid #fc057d; }}")
        self.create_order_button.clicked.connect(self.frame1.show_order_message)

        gradient_button_sizes = [
            (1550, 180, 350, 140),
            (1550, 340, 350, 140),
            (1550, 500, 350, 140),
            (1550, 660, 350, 140),
            (1550, 820, 350, 140),
        ]

        other_button_sizes = [
            (20, 640, 490, 150),
            (530, 640, 490, 150),
            (1040, 640, 490, 150),
            (20, 810, 490, 150),
            (530, 810, 490, 150),
            (1040, 810, 490, 150)
        ]

        

        self.buttons = []

        for size, text in zip(gradient_button_sizes, ["Quét Mã QR", "Tính Tiền", "Đặt Bàn", "In Hoá Đơn", "Hỗ Trợ"]):
            button = QPushButton(self)
            button.setGeometry(*size)
            button.setStyleSheet(f"QPushButton {{ background: {gradient_color}; color: {text_color_white}; border-radius: 70px; font-weight: {font_weight}; font-size: {font_size_large}; }} QPushButton:hover {{ border: 4px solid #FFF; }} QPushButton:pressed {{ border: 8px solid #FFF; }}")
            button.setText(text)
            button.setText(text)
            if text == "Hỗ Trợ":
                button.clicked.connect(self.show_support_frame)
            self.buttons.append(button)

        for size, text in zip(other_button_sizes, ["Kho Hàng", "Thu Nhập", "Xem Camera", "Thêm", "Xoá", "Sửa"]):
            button = QPushButton(self)
            button.setGeometry(*size)
            button.setStyleSheet(f"QPushButton {{ background-color: {gradient_color}; color: {text_color_white}; border: none; font-weight: {font_weight}; font-size: {font_size_large}; }} QPushButton:hover {{ border: 4px solid #FFF; }} QPushButton:pressed {{ border: 8px solid #FFF; }}")
            button.setText(text)
            if text == "Thêm":
                button.clicked.connect(self.show_add_frame)
            elif text == "Xoá":
                button.clicked.connect(self.show_delete_frame)
            elif text == "Sửa":  
                button.clicked.connect(self.show_edit_frame)
            elif text == "Kho Hàng":
                button.clicked.connect(self.show_inventory_frame)
            self.buttons.append(button)

        self.time_label = QLabel(self)
        self.time_label.setGeometry(1550, 40, 350, 100)
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setStyleSheet(f"QLabel {{ color: #02f3f7; font-weight: {font_weight}; font-size: 24pt; }}")

        self.duty_label = QLabel(self)
        self.duty_label.setGeometry(1550, 20, 350, 40)
        self.duty_label.setAlignment(Qt.AlignCenter)
        self.duty_label.setStyleSheet(f"QLabel {{ color: #f70254; font-weight: {font_weight}; font-size: 14pt; }}")
        self.duty_label.setText("Duty-Coffee")

        self.update_time()

    
        
    def update_time(self):
        current_time = QDateTime.currentDateTime().toString("hh:mm:ss")
        self.time_label.setText(current_time)
        QTimer.singleShot(1000, self.update_time)

    def show_add_frame(self):
        self.add_frame = AddFrame()
        self.add_frame.data_added.connect(self.frame1.update_table)
        self.add_frame.show()

    def show_delete_frame(self):
        self.delete_frame = DeleteFrame()
        self.delete_frame.data_deleted.connect(self.frame1.update_table)
        self.delete_frame.show()

    def show_edit_frame(self):  
        self.edit_frame = EditFrame()
        self.edit_frame.data_updated.connect(self.frame1.update_table)
        self.edit_frame.show()

    def show_support_frame(self):  
        self.support_frame = SupportFrame()
        self.support_frame.show()

    def show_inventory_frame(self):  
        self.inventory_frame = InventoryFrame()
        self.inventory_frame.show()

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
