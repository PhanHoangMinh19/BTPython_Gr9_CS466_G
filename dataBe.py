import sqlite3

# Hàm tạo cơ sở dữ liệu
def create_database():
    # Kết nối đến cơ sở dữ liệu (nếu cơ sở dữ liệu chưa tồn tại, nó sẽ được tạo)
    conn = sqlite3.connect('user3.db')
    cursor = conn.cursor()

    # Tạo bảng `users` nếu chưa tồn tại
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS person (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            access_level TEXT NOT NULL
        )
    ''')
# + id: Cột id là khóa chính (PRIMARY KEY) và được tự động tăng giá trị
    #   (AUTOINCREMENT) mỗi khi thêm bản ghi mới.
# + username: Cột username là kiểu TEXT và không được phép để trống (NOT NULL). Nó
    #         phải là duy nhất (UNIQUE), nghĩa là không thể có hai người dùng với
    #         cùng tên đăng nhập.
# + password: Cột password là kiểu TEXT và không được để trống.
# + email: Cột email là kiểu TEXT và cũng không được để trống, phải là duy nhất (UNIQUE),
    #      nghĩa là không thể có hai người dùng với cùng địa chỉ email.
# + access_level: Cột access_level là kiểu TEXT và không được để trống, dùng để lưu trữ
    #      cấp độ truy cập của người dùng (ví dụ: admin, user, v.v.).


    # Commit và đóng kết nối
    conn.commit()
    conn.close()

    #print("Cơ sở dữ liệu 'user_management.db' và bảng 'users' đã được tạo thành công!")

if __name__ == "__main__":
    create_database()
