# Ứng Dụng Karaoke

Ứng dụng tra cứu và quản lý bài hát karaoke với các tính năng:
- Quản lý bài hát (thêm, sửa, xóa)
- Hệ thống đăng nhập và phân quyền admin/user
- Thùng rác để khôi phục bài hát đã xóa
- Đánh dấu bài hát yêu thích

## Cách chạy ứng dụng

Có hai cách để chạy ứng dụng:

### 1. Sử dụng Docker (Khuyên dùng)

Phương pháp này sẽ tạo môi trường đầy đủ với MySQL Server:

```bash
# Clone repo (nếu chưa có)
git clone <repository-url>
cd pro_karaoke_project

# Khởi động ứng dụng với Docker
docker-compose up -d
```

Truy cập ứng dụng tại: **http://localhost:5001**

### 2. Chạy trực tiếp bằng Python

Phương pháp này yêu cầu:
- MySQL Server đang chạy trên port 3308
- Python 3.x đã được cài đặt

```bash
# Clone repo (nếu chưa có)
git clone <repository-url>
cd pro_karaoke_project

# Cài đặt thư viện
pip install -r requirements.txt

# Chạy ứng dụng
python run.py
```

Truy cập ứng dụng tại: **http://localhost:5000**

## Tài khoản mặc định

- **Admin**: 
  - Username: admin
  - Password: admin

## Cấu trúc ứng dụng

```
pro_karaoke_project/
├── app/                    # Package chính của ứng dụng
│   ├── models/             # Mô hình dữ liệu
│   ├── routes/             # Các định tuyến HTTP
│   ├── static/             # File tĩnh (CSS, JS, hình ảnh)
│   ├── templates/          # Template HTML
│   ├── utils/              # Tiện ích
│   └── __init__.py         # Khởi tạo ứng dụng
├── config.py               # Cấu hình ứng dụng
├── docker-compose.yml      # Cấu hình Docker
├── init.sql                # Script khởi tạo DB
├── requirements.txt        # Thư viện yêu cầu
└── run.py                  # Script khởi động
```

## Kết nối với MySQL qua MySQL Workbench

1. **Cài đặt MySQL Workbench**

   Tải và cài đặt [MySQL Workbench](https://dev.mysql.com/downloads/workbench/)

2. **Thiết lập kết nối mới**

   - Mở MySQL Workbench
   - Chọn "+" bên cạnh "MySQL Connections"
   - Nhập thông tin kết nối:
     - Connection Name: Karaoke App
     - Hostname: localhost
     - Port: 3307
     - Username: user
     - Password: password (khi được hỏi)
   - Nhấn "Test Connection" để kiểm tra
   - Nhấn "OK" để lưu

3. **Kết nối và quản lý cơ sở dữ liệu**

   - Nhấp vào kết nối đã tạo
   - Chọn schema "karaoke_db" từ danh sách schema
   - Quản lý bảng "Songs" và dữ liệu

## Cài đặt thủ công (không dùng Docker)

### Yêu cầu
- Python 3.8+
- MySQL Server

### Các bước cài đặt

1. **Cài đặt thư viện Python**
   ```
   pip install -r requirements.txt
   ```

2. **Cài đặt và cấu hình MySQL**
   - Cài đặt MySQL Server
   - Tạo cơ sở dữ liệu và bảng như trong file `init.sql`
   - Cập nhật thông tin kết nối trong file `app.py`

3. **Chạy ứng dụng**
   ```
   python app.py
   ```

4. **Truy cập ứng dụng**
   ```
   http://localhost:5000
   ```

## Cấu trúc dự án
- `app.py`: Ứng dụng Flask
- `Dockerfile`: Cấu hình Docker cho ứng dụng Flask
- `docker-compose.yml`: Cấu hình Docker Compose để chạy Flask và MySQL
- `init.sql`: Script khởi tạo cơ sở dữ liệu
- `requirements.txt`: Danh sách thư viện Python
- `templates/`: Thư mục chứa templates HTML
- `static/images/`: Thư mục lưu trữ ảnh bìa bài hát 