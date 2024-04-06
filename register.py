import tkinter as tk
from tkinter import messagebox
import pyodbc
import hashlib
import random
import string
from datetime import datetime, timedelta
import pyperclip

def check_existing_userid(userid):
    server = 'DESKTOP-BHR2OIT\\GUNX'
    database = 'menu'
    username_db = 'sa'
    password_db = 'abc@123'
    driver = '{ODBC Driver 17 for SQL Server}'
    conn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';DATABASE='+database+';UID='+username_db+';PWD='+password_db)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM dbo.accounts WHERE userid = ?", (userid,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row is not None

def check_existing_username(username):
    server = 'DESKTOP-BHR2OIT\\GUNX'
    database = 'menu'
    username_db = 'sa'
    password_db = 'abc@123'
    driver = '{ODBC Driver 17 for SQL Server}'
    conn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';DATABASE='+database+';UID='+username_db+';PWD='+password_db)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM dbo.accounts WHERE username = ?", (username,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row is not None

def generate_license(userid, username, password):
    random_char_sets = []
    while len(random_char_sets) < 5:
        random_chars = ''.join(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for _ in range(5))
        if random_chars not in random_char_sets:
            random_char_sets.append(random_chars)

    return '-'.join(random_char_sets)

def generate_password():
    while True:
        password = ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(8))
        if (any(c.islower() for c in password) and 
            any(c.isupper() for c in password) and 
            any(c.isdigit() for c in password) and 
            any(c in string.punctuation for c in password)):
            return password

def encrypt_data(data):
    return hashlib.sha256((data + '10charshift').encode()).hexdigest()

def save_account(name, password, privilege, term, entry_license, root):
    server = 'DESKTOP-BHR2OIT\\GUNX'
    database = 'menu'
    username_db = 'sa'
    password_db = 'abc@123'
    driver = '{ODBC Driver 17 for SQL Server}'
    conn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';DATABASE='+database+';UID='+username_db+';PWD='+password_db)
    cursor = conn.cursor()

    while True:
        userid = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        if not check_existing_userid(userid):
            break

    if check_existing_username(name):
        messagebox.showerror("Lỗi", "Tên đăng nhập đã tồn tại.")
        return

    license = generate_license(userid, name, password)

    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    encrypted_password = encrypt_data(password)
    encrypted_license = hashlib.sha256(license.encode()).hexdigest()
    encrypted_privilege = hashlib.sha256(privilege.encode()).hexdigest()

    begin_time = datetime.now()
    end_time = None

    if term == 'Vĩnh viễn':
        end_time = datetime(9999, 12, 31, 23, 59, 59)
    else:
        if term == '7 ngày':
            end_time = datetime.now() + timedelta(days=7)
        elif term == '30 ngày':
            end_time = datetime.now() + timedelta(days=30)
        elif term == '90 ngày':
            end_time = datetime.now() + timedelta(days=90)
        elif term == '180 ngày':
            end_time = datetime.now() + timedelta(days=180)
        elif term == '365 ngày':
            end_time = datetime.now() + timedelta(days=365)

    # Sử dụng parameterized query để tránh lỗi Injection và đảm bảo định dạng đúng cho các kiểu dữ liệu
    cursor.execute("INSERT INTO dbo.accounts (userid, username, password, license_hash, privilege, begin_time, end_time) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                   (userid, name, hashed_password, encrypted_license, encrypted_privilege, begin_time, end_time))
    conn.commit()
    cursor.close()
    conn.close()

    entry_license.insert(0, license)  # Cập nhật giá trị của entry_license
    show_register_success_dialog(license, root)



def show_register_success_dialog(license, root):
    success_dialog = tk.Toplevel(root)
    success_dialog.title("Đăng ký thành công")
    success_dialog.geometry("350x100")

    label_message = tk.Label(success_dialog, text=f"Đăng ký thành công.\nLicense của tài khoản: {license}")
    label_message.pack(pady=10)

    button_copy = tk.Button(success_dialog, text="Copy License", command=lambda: copy_license(license))
    button_copy.pack(pady=5)

def copy_license(license):
    pyperclip.copy(license)
    messagebox.showinfo("Thông báo", "License đã được copy vào clipboard.")

def register():
    root = tk.Tk()
    root.title("Đăng ký tài khoản")
    root.geometry("240x190")

    label_username = tk.Label(root, text="Tên đăng ký:")
    label_username.grid(row=0, column=0, padx=5, pady=5)

    label_password = tk.Label(root, text="Nhập mật khẩu:")
    label_password.grid(row=1, column=0, padx=5, pady=5)

    label_privilege = tk.Label(root, text="Quyền:")
    label_privilege.grid(row=2, column=0, padx=5, pady=5)

    label_term = tk.Label(root, text="Thời hạn:")
    label_term.grid(row=3, column=0, padx=5, pady=5)

    entry_username = tk.Entry(root)
    entry_username.grid(row=0, column=1, padx=5, pady=5)

    entry_password = tk.Entry(root, show="*")
    entry_password.grid(row=1, column=1, padx=5, pady=5)

    privilege_options = ['Staff', 'Manager']
    var_privilege = tk.StringVar(root)
    var_privilege.set(privilege_options[0]) 
    dropdown_privilege = tk.OptionMenu(root, var_privilege, *privilege_options)
    dropdown_privilege.grid(row=2, column=1, padx=5, pady=5)

    term_options = ['7 ngày', '30 ngày', '90 ngày', '180 ngày', '365 ngày', 'Vĩnh viễn']
    var_term = tk.StringVar(root)
    var_term.set(term_options[0]) 
    dropdown_term = tk.OptionMenu(root, var_term, *term_options)
    dropdown_term.grid(row=3, column=1, padx=5, pady=5)

    entry_license = tk.Entry(root, state='readonly')
    

    button_register = tk.Button(root, text="Đăng ký", command=lambda: on_register(entry_username, entry_password, var_privilege, var_term, entry_license, root))
    button_register.grid(row=4, columnspan=2, padx=5, pady=5)

    # Tạo vô hình chữ nhật bên trên nút Đăng ký
    hidden_rectangle = tk.Label(root, width=5, height=1, bg=root.cget("bg"))
    hidden_rectangle.grid(row=4, column=0, padx=5, pady=5)

    root.mainloop()

def on_register(entry_username, entry_password, var_privilege, var_term, entry_license, root):
    name = entry_username.get()
    password = entry_password.get()
    privilege = var_privilege.get()
    term = var_term.get()

    if name.strip() == "" or password.strip() == "":
        messagebox.showerror("Lỗi", "Vui lòng điền đầy đủ thông tin.")
    elif len(password) < 8:
        messagebox.showerror("Lỗi", "Mật khẩu phải có ít nhất 8 ký tự.")
    else:
        save_account(name, password, privilege, term, entry_license, root)

register()
