import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QMainWindow, QFrame
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtCore import Qt
import pyodbc
import hashlib
import time

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Duty-Coffee")
        self.setWindowIcon(QIcon("C:/Users/0x000000000000/Desktop/Python/images/logo.png"))
        self.setGeometry(0, 0, 400, 200)
        
        gradient_color = "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #07f5f1, stop:0.5 #15074a, stop:1 #f70576);"
        gradient_color2 = "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #0a234f, stop:0.5 #06094f, stop:1 #130742);"
        self.setStyleSheet("background-color: " + gradient_color2)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        self.label_title = QLabel("Đăng nhập", self)
        self.label_title.setFont(QFont("Arial", 16))
        self.label_title.setStyleSheet("background-color: " + gradient_color + "color: white; border: none; padding: 10px 20px; border-radius: 5px; font-weight: bold;")
        self.label_title.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label_title)

        self.textbox_username = QLineEdit(self)
        self.textbox_username.setPlaceholderText("Tài khoản")
        self.textbox_username.setStyleSheet("background-color: rgba(255, 255, 255, 100); border: 1px solid #ccc; border-radius: 10px;")
        self.textbox_username.setFixedHeight(35)
        self.set_line_edit_icon(self.textbox_username, "C:/Users/0x000000000000/Desktop/Python/images/username_icon.png")
        layout.addWidget(self.textbox_username)

        self.textbox_password = QLineEdit(self)
        self.textbox_password.setPlaceholderText("Mật khẩu")
        self.textbox_password.setEchoMode(QLineEdit.Password)
        self.textbox_password.setStyleSheet("background-color: rgba(255, 255, 255, 100); border: 1px solid #ccc; border-radius: 10px;")
        self.textbox_password.setFixedHeight(35)
        self.set_line_edit_icon(self.textbox_password, "C:/Users/0x000000000000/Desktop/Python/images/password_icon.png")
        layout.addWidget(self.textbox_password)

        self.textbox_license = QLineEdit(self)
        self.textbox_license.setPlaceholderText("License")
        self.textbox_license.setStyleSheet("background-color: rgba(255, 255, 255, 100); border: 1px solid #ccc; border-radius: 10px;")
        self.textbox_license.setFixedHeight(35)
        self.set_line_edit_icon(self.textbox_license, "C:/Users/0x000000000000/Desktop/Python/images/license_icon.png")
        layout.addWidget(self.textbox_license)

        hbox = QHBoxLayout()
        self.button_login = QPushButton("Đăng nhập", self)
        self.button_login.setStyleSheet("background-color: " + gradient_color + "color: white; border: none; padding: 10px 20px; border-radius: 5px; font-weight: bold;")
        self.button_login.clicked.connect(self.login)
        self.button_login.setCursor(Qt.PointingHandCursor)
        hbox.addWidget(self.button_login)

        self.button_exit = QPushButton("Thoát", self)
        self.button_exit.setStyleSheet("background-color: " + gradient_color + "color: white; border: none; padding: 10px 20px; border-radius: 5px; font-weight: bold;")
        self.button_exit.clicked.connect(self.exit)
        self.button_exit.setCursor(Qt.PointingHandCursor)
        hbox.addWidget(self.button_exit)

        layout.addLayout(hbox)
        self.setLayout(layout)

        self.center()

    def center(self):
        screen = QApplication.primaryScreen()
        rect = screen.availableGeometry()
        width = rect.width()
        height = rect.height()
        window_rect = self.frameGeometry()
        window_width = window_rect.width()
        window_height = window_rect.height()
        self.move((width - window_width) // 2, (height - window_height) // 2)

    def login(self):
        username = self.textbox_username.text()
        password = self.textbox_password.text()
        license = self.textbox_license.text()

        if not username or not password or not license:
            self.show_message_box("Lỗi", "Vui lòng nhập đầy đủ thông tin.")
            return

        result = self.check_credentials(username, password, license)
        if result == "valid":
            self.hide()
            self.open_main_window()
        elif result == "invalid_username_password":
            self.show_message_box("Lỗi", "Tên đăng nhập hoặc mật khẩu không đúng.")
        elif result == "invalid_license":
            self.show_message_box("Lỗi", "License không đúng hoặc đã hết hạn sử dụng.<br>License có dạng: AB12C-SDF34-ASDZD-24DFR-ASD12")

    def show_message_box(self, title, message):
        error_box = QMessageBox(self)
        error_box.setStyleSheet("background-color: #f0f0f0;")
        message_text = "<span style='color: white; font-weight: bold;'>{}</span>".format(message)
        error_box.warning(self, title, message_text)


    def exit(self):
        self.close()

    def check_credentials(self, username, password, license):
        try:
            server = 'DESKTOP-BHR2OIT\\GUNX'
            database = 'menu'
            username_db = 'sa'
            password_db = 'abc@123'
            driver = '{ODBC Driver 17 for SQL Server}'

            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            encrypted_license = hashlib.sha256(license.encode()).hexdigest()

            current_time = int(time.time())

            conn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';DATABASE='+database+';UID='+username_db+';PWD='+password_db)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM dbo.accounts WHERE username = ? AND password = ?", (username, hashed_password))
            row = cursor.fetchone()
            cursor.close()
            conn.close()

            if row is None:
                return "invalid_username_password"

            begin_time = int(time.mktime(row.begin_time.timetuple()))
            end_time = int(time.mktime(row.end_time.timetuple()))

            if row.license_hash != encrypted_license or begin_time > current_time or end_time < current_time:
                return "invalid_license"

            return "valid"
        except Exception as e:
            self.show_message_box("Lỗi", str(e))
            return "error"

    def set_line_edit_icon(self, line_edit, icon_path):
        pixmap = QPixmap(icon_path)
        icon = QIcon(pixmap)
        line_edit.addAction(icon, QLineEdit.LeadingPosition)

    def open_main_window(self):
        self.main_window = MainWindow()
        self.main_window.showFullScreen()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")
        self.setGeometry(0, 0, 1920, 1080)
        self.setStyleSheet("background-color: #f0f0f0;")

        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        frame1 = QFrame(self)
        frame1.setGeometry(20, 20, 10, 10)
        frame1.setStyleSheet("background-color: red;")

        frame2 = QFrame(self)
        frame2.setGeometry(1040, 20, 10, 10)
        frame2.setStyleSheet("background-color: blue;")

        layout.addWidget(frame1)
        layout.addWidget(frame2)

        main_widget.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())
