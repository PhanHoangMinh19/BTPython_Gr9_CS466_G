import bcrypt
from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from dataBe import create_database

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Để dùng flash messages

def get_db_connection():
    conn = sqlite3.connect('user3.db', timeout=10)
    conn.row_factory = sqlite3.Row
    return conn

def add_user(username, password, email, access_level):
    # Mã hóa mật khẩu trước khi lưu vào cơ sở dữ liệu
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO person (username, password, email, access_level)
        VALUES (?, ?, ?, ?)
    ''', (username, hashed_password, email, access_level))
    conn.commit()
    conn.close()

# Trang home
@app.route('/')
def home():
    return render_template('home.html')

# Trang admin
@app.route('/admin')
def admin():
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM person').fetchall()
    conn.close()
    return render_template('admin.html', users=users)

# Trang đăng kí
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    create_database()
    if request.method == 'POST':
        username = request.form['username1']
        password = request.form['password1']
        email = request.form['email']
        access_level = 'user'
        if username and email and password and access_level:
            add_user(username, password, email, access_level)
            return redirect(url_for('login'))
        else:
            flash('Invalid', 'danger')
    return render_template('signup.html')

# Trang đăng nhập
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username2']
        password = request.form['password2']

        # Kiểm tra nếu username và password là admin_1 và 12345
        if username == 'admin_1' and password == '12345':
            flash('Login successful!', 'success')
            return redirect(url_for('admin'))

        # Kiểm tra thông tin đăng nhập bằng database cho các tài khoản khác
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM person WHERE username = ? ', (username,)).fetchone()
        conn.close()

        if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
            flash('Login successful!', 'success')
            if user['access_level'] == 'admin':
                return redirect(url_for('admin'))
            if user['access_level'] == 'user':
                return redirect(url_for('dashboard2'))
            if user['access_level'] == 'content manager':
                return redirect(url_for('dashboard3'))
        else:
            flash('Invalid username or password', 'danger')

    return render_template('login.html')

# Trang dashboard sau khi đăng nhập thành công
@app.route('/dashboard2')
def dashboard2():
    return "<h1>Welcome to user!</h1>"

@app.route('/dashboard3')
def dashboard3():
    return "<h1>Welcome to content manager!</h1>"

# Edit user role
@app.route('/edit_user/<int:id>', methods=['GET', 'POST'])
def edit_user(id):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM person WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        new_role = request.form['role']
        conn.execute('UPDATE person SET access_level = ? WHERE id = ?', (new_role, id))
        conn.commit()
        conn.close()
        return redirect(url_for('admin'))

    conn.close()
    return render_template('edit_user.html', user=user)

# Delete user
@app.route('/delete_user/<int:id>', methods=['POST'])
def delete_user(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM person WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin'))

# Add user
@app.route('/add_user', methods=['GET', 'POST'])
def add_user_route():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        access_level = request.form['role']
        if username and email and password and access_level:
            add_user(username, password, email, access_level)
            return redirect(url_for('admin'))
        else:
            flash('Invalid', 'danger')
    return render_template('add_user.html')

if __name__ == '__main__':
    app.run(debug=True)
