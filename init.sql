CREATE DATABASE IF NOT EXISTS karaoke_db;
USE karaoke_db;

-- Tạo bảng Users
CREATE TABLE IF NOT EXISTS Users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE
);

-- Thêm một tài khoản admin mẫu (mật khẩu 'admin123')
INSERT INTO Users (username, password, is_admin) VALUES 
('admin', 'pbkdf2:sha256:600000$XDfBrSTTdCu2Q9el$c9c491c9e3c1a2b3d72a0d3e5ca6b61c6cbb0d6a8abf4ad76eac9e5e7cec8c68', TRUE);

-- Thêm một tài khoản user mẫu (mật khẩu 'user123')
INSERT INTO Users (username, password, is_admin) VALUES 
('user', 'pbkdf2:sha256:600000$CnxhgFOIKST7lNRa$5d0ed06d7e65a2c883a94e73b11b4a561dd73b28a645aeeb1c761bbe21aa94a8', FALSE);

-- Sửa đổi bảng Songs
DROP TABLE IF EXISTS Songs;
CREATE TABLE IF NOT EXISTS Songs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    artist VARCHAR(255) DEFAULT 'Unknown Artist',
    image_path VARCHAR(255) DEFAULT 'static/images/default_image.jpg',
    user_id INT,
    is_admin_upload BOOLEAN DEFAULT FALSE,
    is_deleted BOOLEAN DEFAULT FALSE,
    is_favorite BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE SET NULL
);

-- Thêm một số dữ liệu mẫu
INSERT INTO Songs (title, artist, image_path, user_id, is_admin_upload) VALUES 
('Nắng Ấm Xa Dần', 'Sơn Tùng M-TP', 'static/images/default_image.jpg', 1, TRUE),
('Hãy Trao Cho Anh', 'Sơn Tùng M-TP', 'static/images/default_image.jpg', 1, TRUE),
('Em Của Ngày Hôm Qua', 'Sơn Tùng M-TP', 'static/images/default_image.jpg', 2, FALSE); 