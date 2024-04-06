from PyQt5.QtWidgets import QFrame, QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton, QApplication, QWidget, QHBoxLayout, QLabel, QMessageBox
from PyQt5.QtCore import Qt, QDateTime
import pyodbc
import locale
import pyperclip

locale.setlocale(locale.LC_ALL, '')

class MenuFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: #e4f7f7;")
        self.products_exist = False
        server = 'DESKTOP-BHR2OIT\\GUNX'
        database = 'menu'
        username = 'sa'
        password = 'abc@123'
        connection = pyodbc.connect(f'DRIVER=ODBC Driver 17 for SQL Server;SERVER={server};DATABASE={database};UID={username};PWD={password}')
        cursor = connection.cursor()
        cursor.execute('SELECT ID, San_Pham, Gia_Tien, So_Luong FROM dbo.products')
        data = cursor.fetchall()
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setRowCount(len(data))
        self.table.verticalHeader().setVisible(False)
        header_labels = ['ID', 'Sản Phẩm', 'Giá Tiền', 'Số Lượng', 'Order', '']
        self.table.setHorizontalHeaderLabels(header_labels)
        for i, row in enumerate(data):
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                if j == 2:
                    value = locale.format_string("%d", float(value), grouping=True)
                    item.setText(value)
                self.table.setItem(i, j, item)
            gradient_color = "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #07f5f1, stop:0.5 #15074a, stop:1 #f70576);"
            text_color_white = "#FFF"
            font_weight = "bold"
            font_size_large = "7pt"
            widget = QWidget()
            layout = QHBoxLayout()
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setAlignment(Qt.AlignCenter)
            plus_button = QPushButton("+")
            plus_button.setFixedSize(20, 20)
            plus_button.setStyleSheet(f"QPushButton {{ background: {gradient_color}; color: {text_color_white}; border-radius: 10px; font-weight: {font_weight}; font-size: {font_size_large}; }} QPushButton:hover {{ border: 1px solid #fc057d; }} QPushButton:pressed {{ border: 2px solid #fc057d; }}")
            plus_button.clicked.connect(self.on_plus_button_clicked)
            minus_button = QPushButton("-")
            minus_button.setFixedSize(20, 20)
            minus_button.setStyleSheet(f"QPushButton {{ background: {gradient_color}; color: {text_color_white}; border-radius: 10px; font-weight: {font_weight}; font-size: {font_size_large}; }} QPushButton:hover {{ border: 1px solid #fc057d; }} QPushButton:pressed {{ border: 2px solid #fc057d; }}")
            minus_button.clicked.connect(self.on_minus_button_clicked)
            order_layout = QHBoxLayout()
            order_layout.addWidget(minus_button)
            order_layout.addWidget(plus_button)
            widget.setLayout(order_layout)
            self.table.setCellWidget(i, 4, widget)
        self.table.setColumnWidth(0, 106)
        self.table.setColumnWidth(1, 420)
        self.table.setColumnWidth(2, 200)
        self.table.setColumnWidth(3, 120)
        self.table.setColumnWidth(4, 109)
        for column_index in [0, 2, 3]:
            self.table.horizontalHeaderItem(column_index).setTextAlignment(Qt.AlignCenter)
            for row_index in range(len(data)):
                item = self.table.item(row_index, column_index)
                if item:
                    item.setTextAlignment(Qt.AlignCenter)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout = QVBoxLayout(self)
        layout.addWidget(self.table)
        self.setLayout(layout)
        self.add_buttons(len(data))

    def clear_frame2_table(self):
        frame2 = self.parent().frame2
        table = frame2.findChild(QTableWidget)
        if table:
            table.clearContents()
            table.setRowCount(0)

    def clear_frame2_total_label(self):
        frame2 = self.parent().frame2
        total_label = frame2.findChild(QLabel, "total_label")
        if total_label:
            total_label.deleteLater()

    def show_order_message(self):
        has_selected_products = False
        frame2 = self.parent().frame2
        table = frame2.findChild(QTableWidget)
        if table and table.rowCount() > 0:
            has_selected_products = True

        if not self.products_exist and not has_selected_products:
            QMessageBox.information(self, "Thông báo", "Bạn cần phải chọn sản phẩm từ menu mới có thể tạo đơn.")
        else:
            reply = QMessageBox.question(self, "Thông báo", "Bạn có muốn tạo đơn hàng không?",
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                current_datetime = QDateTime.currentDateTime().toString("yyyyMMddhhmmss")
                order_code = int(current_datetime)
                QMessageBox.information(self, "Thông báo", f"Mã đơn hàng của bạn là: {order_code}", QMessageBox.Ok)
                pyperclip.copy(str(order_code))
                server = 'DESKTOP-BHR2OIT\\GUNX'
                database = 'menu'
                username = 'sa'
                password = 'abc@123'
                connection = pyodbc.connect(
                    f'DRIVER=ODBC Driver 17 for SQL Server;SERVER={server};DATABASE={database};UID={username};PWD={password}')
                cursor = connection.cursor()

                for row_index in range(table.rowCount()):
                    san_pham = table.item(row_index, 0).text()
                    gia_tien_str = table.item(row_index, 1).text().replace(',', '')
                    gia_tien = float(locale.atof(gia_tien_str))
                    so_luong = int(table.item(row_index, 2).text())
                    if so_luong > 0:
                        cursor.execute(
                            "INSERT INTO dbo.bill (Bill_ID, San_Pham, Gia_Tien, So_Luong, Tong_Tien) VALUES (?, ?, ?, ?, ?)",
                            (order_code, san_pham, gia_tien_str, so_luong, gia_tien * so_luong))
                connection.commit()

                total_price = sum(
                    float(table.item(row_index, 3).text().replace(',', '')) * int(
                        table.item(row_index, 2).text()) for row_index in range(table.rowCount()) if
                    table.item(row_index, 2) and table.item(row_index, 3) and int(table.item(row_index, 2).text()) > 0)

                for row_index in range(table.rowCount()):
                    if table.item(row_index, 2) and table.item(row_index, 3) and int(table.item(row_index, 2).text()) > 0:
                        san_pham = table.item(row_index, 0).text()
                        gia_tien_str = table.item(row_index, 1).text().replace(',', '')
                        gia_tien = float(locale.atof(gia_tien_str))
                        so_luong = int(table.item(row_index, 2).text())
                        tong_tien = gia_tien * so_luong
                        cursor.execute(
                            "UPDATE dbo.bill SET Tong_Tien = ? WHERE Bill_ID = ? AND San_Pham = ?",
                            (tong_tien, order_code, san_pham))
                connection.commit()

                QMessageBox.information(self, "Thông báo", "Đã sao chép đơn hàng.", QMessageBox.Ok)
                self.clear_frame2_table()
                self.clear_frame2_total_label()
            else:
                QMessageBox.information(self, "Thông báo", "Bạn đã thoát.", QMessageBox.Ok)
                self.clear_frame2_table()
                self.clear_frame2_total_label()

    def add_buttons(self, num_rows):
        gradient_color = "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #07f5f1, stop:0.5 #15074a, stop:1 #f70576);"
        text_color_white = "#FFF"
        font_weight = "bold"
        font_size_large = "7pt"
        for row in range(num_rows):
            widget = QWidget()
            layout = QHBoxLayout()
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setAlignment(Qt.AlignCenter)
            plus_button = QPushButton("+")
            plus_button.setFixedSize(20, 20)
            plus_button.setStyleSheet(f"QPushButton {{ background: {gradient_color}; color: {text_color_white}; border-radius: 10px; font-weight: {font_weight}; font-size: {font_size_large}; }} QPushButton:hover {{ border: 1px solid #fc057d; }} QPushButton:pressed {{ border: 2px solid #fc057d; }}")
            plus_button.clicked.connect(self.on_plus_button_clicked)
            minus_button = QPushButton("-")
            minus_button.setFixedSize(20, 20)
            minus_button.setStyleSheet(f"QPushButton {{ background: {gradient_color}; color: {text_color_white}; border-radius: 10px; font-weight: {font_weight}; font-size: {font_size_large}; }} QPushButton:hover {{ border: 1px solid #fc057d; }} QPushButton:pressed {{ border: 2px solid #fc057d; }}")
            minus_button.clicked.connect(self.on_minus_button_clicked)
            order_layout = QHBoxLayout()
            order_layout.addWidget(minus_button)
            order_layout.addWidget(plus_button)
            widget.setLayout(order_layout)
            self.table.setCellWidget(row, 4, widget)

    def on_plus_button_clicked(self):
        button = self.sender()
        if button:
            index = self.table.indexAt(button.parent().pos())
            row = index.row()
            san_pham = self.table.item(row, 1).text()
            gia_tien_str = self.table.item(row, 2).text().replace(',', '')
            gia_tien = locale.format_string("%d", float(gia_tien_str), grouping=True)
            so_luong = self.table.item(row, 3).text()
            frame2 = self.parent().frame2
            frame2_layout = frame2.layout()
            if not frame2_layout:
                frame2_layout = QVBoxLayout()
                frame2.setLayout(frame2_layout)
            table = frame2.findChild(QTableWidget)
            if not table:
                table = QTableWidget()
                table.setColumnCount(3)
                table.verticalHeader().setVisible(False)
                table.setHorizontalHeaderLabels(['Sản Phẩm', 'Giá Tiền', 'Số Lượng'])
                table.setColumnWidth(0, 241)
                table.setColumnWidth(1, 120)
                table.setColumnWidth(2, 105)
                table.setEditTriggers(QTableWidget.NoEditTriggers)
                frame2_layout.addWidget(table)
            for row_index in range(table.rowCount()):
                if table.item(row_index, 0).text() == san_pham:
                    current_quantity = int(table.item(row_index, 2).text())
                    new_quantity = current_quantity + 1
                    table.setItem(row_index, 2, QTableWidgetItem(str(new_quantity)))
                    item = table.item(row_index, 2)
                    if item:
                        item.setTextAlignment(Qt.AlignCenter)
                    self.update_total_label(table)
                    return
            row_count = table.rowCount()
            table.setRowCount(row_count + 1)
            table.setItem(row_count, 0, QTableWidgetItem(san_pham))
            table.setItem(row_count, 1, QTableWidgetItem(gia_tien))
            table.setItem(row_count, 2, QTableWidgetItem('1'))
            item = table.item(row_count, 2)
            if item:
                item.setTextAlignment(Qt.AlignCenter)
            for i in range(3):
                item = table.item(row_count, i)
                if item:
                    item.setTextAlignment(Qt.AlignCenter)
            self.update_total_label(table)

    def on_minus_button_clicked(self):
        button = self.sender()
        if button:
            index = self.table.indexAt(button.parent().pos())
            row = index.row()
            san_pham = self.table.item(row, 1).text()
            frame2 = self.parent().frame2
            table = frame2.findChild(QTableWidget)
            if table:
                for row_index in range(table.rowCount()):
                    if table.item(row_index, 0).text() == san_pham:
                        current_quantity = int(table.item(row_index, 2).text())
                        if current_quantity > 1:
                            new_quantity = current_quantity - 1
                            table.setItem(row_index, 2, QTableWidgetItem(str(new_quantity)))
                            item = table.item(row_index, 2)
                            if item:
                                item.setTextAlignment(Qt.AlignCenter)
                        else:
                            table.removeRow(row_index)
                        self.update_total_label(table)
                        return

    def update_total_label(self, table):
        total = 0
        for row_index in range(table.rowCount()):
            gia_tien_str = table.item(row_index, 1).text().replace(',', '')
            so_luong = int(table.item(row_index, 2).text())
            gia_tien = float(locale.atof(gia_tien_str))
            total += gia_tien * so_luong
        formatted_total = locale.format_string("%d", total, grouping=True)
        frame2 = self.parent().frame2
        total_label = frame2.findChild(QLabel, "total_label")
        if total_label:
            total_label.setText(f"Tổng tiền: {formatted_total} VNĐ")
        else:
            total_label = QLabel(f"Tổng tiền: {formatted_total} VNĐ")
            total_label.setObjectName("total_label")
            total_label.setStyleSheet("font-size: 14pt; font-weight: bold; color: #ff5100;")
            frame2.layout().addWidget(total_label)

    def update_table(self):
        server = 'DESKTOP-BHR2OIT\\GUNX'
        database = 'menu'
        username = 'sa'
        password = 'abc@123'
        connection = pyodbc.connect(f'DRIVER=ODBC Driver 17 for SQL Server;SERVER={server};DATABASE={database};UID={username};PWD={password}')
        cursor = connection.cursor()
        cursor.execute('SELECT ID, San_Pham, Gia_Tien, So_Luong FROM dbo.products')
        data = cursor.fetchall()
        self.table.setRowCount(len(data))
        for i, row in enumerate(data):
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                if j == 2:
                    value = locale.format_string("%d", float(value), grouping=True)
                    item.setText(value)
                self.table.setItem(i, j, item)
        for column_index in [0, 2, 3]:
            self.table.horizontalHeaderItem(column_index).setTextAlignment(Qt.AlignCenter)
            for row_index in range(len(data)):
                item = self.table.item(row_index, column_index)
                if item:
                    item.setTextAlignment(Qt.AlignCenter)
        self.table.viewport().update()   

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    menu_frame = MenuFrame()
    menu_frame.show()
    sys.exit(app.exec_())
