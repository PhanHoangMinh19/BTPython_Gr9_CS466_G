
from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from dataBe import create_database
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Để dùng flash messages
import bcrypt

# Hàm kết nối cơ sở dữ liệu
def get_db_connection():
    conn = sqlite3.connect('user3.db')
    conn.row_factory = sqlite3.Row  # Để trả về kết quả dưới dạng từ điển
    return conn

def add_user(username, password, email, access_level):
    # Mã hóa mật khẩu trước khi lưu vào cơ sở dữ liệu
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Kết nối đến cơ sở dữ liệu
    conn = get_db_connection()

    # Thêm người dùng vào bảng `person`
    conn.execute('''
        INSERT INTO person (username, password, email, access_level)
        VALUES (?, ?, ?, ?)
    ''', (username, hashed_password, email, access_level))

    # Commit và đóng kết nối
    conn.commit()
    conn.close()

#Trang home
@app.route('/')
def home():
    return render_template('home.html')


# Trang đăng kí
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    create_database()
    if request.method == 'POST':
        username = request.form['username1']
        password = request.form['password1']
        email = request.form['email']
        access_level = request.form['access_level']

        if username and email and password and access_level:
            add_user(username,password, email, access_level)
            return redirect(url_for('login'))
        else:
            flash('Invalid','danger')
    return render_template('signup.html')




# Trang đăng nhập
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username2']
        password = request.form['password2']

        # Kiểm tra thông tin đăng nhập
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM person WHERE username = ? ', (username,)).fetchone()
        conn.close()

        if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
                flash('Login successful!', 'success')
                if user['access_level'] == 'admin':
                    return redirect(url_for('dashboard1'))
                if user['access_level'] == 'user':
                    return redirect(url_for('dashboard2'))
                if user['access_level'] == 'content manager':
                    return redirect(url_for('dashboard3'))
        else:
            flash('Invalid username or password', 'danger')

    return render_template('login.html')

# Trang dashboard sau khi đăng nhập thành công
@app.route('/dashboard1')
def dashboard1():
    return "<h1>Welcome to admin!</h1>"
@app.route('/dashboard2')
def dashboard2():
    return "<h1>Welcome to user!</h1>"
@app.route('/dashboard3')
def dashboard3():
    return "<h1>Welcome to content manager!</h1>"

if __name__ == '__main__':
    app.run(debug=True)
