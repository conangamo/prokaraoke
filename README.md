# Ứng dụng Tra cứu Thông tin Bài hát Karaoke

Ứng dụng web đơn giản cho phép tra cứu và thêm bài hát karaoke, được đóng gói bằng Docker để dễ dàng triển khai.

## Cài đặt và Chạy với Docker

### Yêu cầu
- [Docker](https://www.docker.com/products/docker-desktop/)
- [Docker Compose](https://docs.docker.com/compose/install/) (thường đã được cài đặt kèm với Docker Desktop)

### Các bước cài đặt

1. **Clone hoặc tải repository này về máy**

2. **Chạy ứng dụng với Docker Compose**

   Mở terminal/command prompt và chạy lệnh sau tại thư mục gốc của dự án:

   ```
   docker-compose up -d
   ```

   Lệnh này sẽ:
   - Tạo và chạy container cho ứng dụng Flask
   - Tạo và chạy container cho MySQL
   - Thiết lập volumes để lưu trữ dữ liệu

3. **Truy cập ứng dụng**

   Mở trình duyệt và truy cập địa chỉ:
   ```
   http://localhost:5000
   ```

4. **Dừng ứng dụng**

   Để dừng ứng dụng, chạy lệnh:
   ```
   docker-compose down
   ```

   Để dừng và xóa volumes (dữ liệu sẽ bị mất):
   ```
   docker-compose down -v
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