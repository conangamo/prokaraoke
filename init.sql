CREATE DATABASE IF NOT EXISTS karaoke_db;
USE karaoke_db;

CREATE TABLE IF NOT EXISTS Songs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    artist VARCHAR(255) DEFAULT 'Unknown Artist',
    image_path VARCHAR(255) DEFAULT 'static/images/default_image.jpg'
);

-- Thêm một số dữ liệu mẫu
INSERT INTO Songs (title, artist, image_path) VALUES 
('Nắng Ấm Xa Dần', 'Sơn Tùng M-TP', 'static/images/default_image.jpg'),
('Hãy Trao Cho Anh', 'Sơn Tùng M-TP', 'static/images/default_image.jpg'),
('Em Của Ngày Hôm Qua', 'Sơn Tùng M-TP', 'static/images/default_image.jpg'); 