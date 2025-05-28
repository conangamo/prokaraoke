CREATE DATABASE  IF NOT EXISTS `karaoke_db` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `karaoke_db`;
-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: karaoke_db
-- ------------------------------------------------------
-- Server version	8.0.42

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Favorites`
--

DROP TABLE IF EXISTS `Favorites`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Favorites` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `song_id` int NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_user_song` (`user_id`,`song_id`),
  KEY `song_id` (`song_id`),
  CONSTRAINT `Favorites_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `Users` (`id`),
  CONSTRAINT `Favorites_ibfk_2` FOREIGN KEY (`song_id`) REFERENCES `Songs` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Favorites`
--

LOCK TABLES `Favorites` WRITE;
/*!40000 ALTER TABLE `Favorites` DISABLE KEYS */;
INSERT INTO `Favorites` VALUES (1,3,12,'2025-05-26 09:14:51');
/*!40000 ALTER TABLE `Favorites` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Songs`
--

DROP TABLE IF EXISTS `Songs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Songs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `artist` varchar(255) DEFAULT 'Unknown Artist',
  `image_path` varchar(255) DEFAULT 'static/images/default_image.jpg',
  `user_id` int DEFAULT NULL,
  `is_admin_upload` tinyint(1) DEFAULT '0',
  `is_deleted` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `Songs_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `Users` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Songs`
--

LOCK TABLES `Songs` WRITE;
/*!40000 ALTER TABLE `Songs` DISABLE KEYS */;
INSERT INTO `Songs` VALUES (4,'Cơn mưa ngang qua','Sơn Tùng M-TP','/static/images/1072279b-ac91-4b46-a673-32d7675900bf_Son_Tung_M-TP_-_Con_mua_ngang_qua.png',3,0,0),(5,'Mưa Rơi Vào Phòng','Khởi My','/static/images/c0dea5e2-a466-4a01-8b66-db9d6a2671fb_maxresdefault.jpg',3,0,0),(6,'Chịu Cách Mình Nói Thua','Rhyder','/static/images/0f7269a7-8771-4b92-9bc8-1ad4b5256578_ab67616d0000b2733687e8b4ade89380cb3d27c6.jpg',3,0,0),(7,'Sau Cơn Mưa','COOLKID','/static/images/3ffa5efa-a17b-469a-9109-75f1c964cc45_3268b5a7ef8bc57a0efc516c35bb24c3.jpg',3,0,0),(8,'Trình','HieuThuHai','/static/images/86dc29ee-12be-48c6-ba75-da4abe35d24e_ab67616d0000b273d52fd56d03776396bb440624.jpg',3,0,0),(9,'Ái Nộ','Masew','/static/images/99a96553-3cc7-4a8c-9027-66de9c2e5189_e3210b257f605f0e4765d02773d7e1cb.jpg',3,0,0),(10,'Sau Tất Cả','Erik','/static/images/ffa64c43-e09e-4626-bd3e-7b03582c5e41_55a2e33a5d4d6a70f5144181c28eacb0_1452855672.jpg',3,0,0),(11,'Đắm Chìm','Trâu','/static/images/b29bd51c-ac47-49df-99f3-bd7e840d6dc5_images.jpg',3,1,0),(12,'Hoa Cỏ Lau','Phong Max','/static/images/74276ff0-23d7-4251-b7a2-a8ceb86d7219_9f579b0fe9276f8eba9464199f9a1b49.jpg',3,1,0),(13,'HeartBeat','Rix Rule','/static/images/0d887088-532d-4d23-9340-90c660edf2af_artworks-GzfIMl4afU4Ym6AV-9FazvQ-t500x500.jpg',3,1,0),(14,'Heathens','Twenty One','/static/images/23e2e2b9-7c5c-4160-b04a-35207bcd2e09_artworks-000476538615-ejx36d-t500x500.jpg',3,1,0),(15,'Nơi Tình Yêu Kết Thúc','Bùi Anh Tuấn','/static/images/32b71cf3-561f-4b0a-a8c8-9fa490eb48b4_f2361dacdbd7c2963d0b111484cf08db.jpg',3,1,0),(16,'Hướng Dương','Tito x Gin','/static/images/9bed753e-934c-4c94-a954-a30a4d69c55e_artworks-hI5abpcnqIzORp78-zfgCOA-t500x500.jpg',3,1,0),(17,'Khu Vườn Tình','Tăng Duy Tân','/static/images/ff97ec47-096e-4a97-8342-4924809dd0b5_1784518a4542d3b777fbf5cfdde81282.jpg',3,1,0);
/*!40000 ALTER TABLE `Songs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Users`
--

DROP TABLE IF EXISTS `Users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `is_admin` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Users`
--

LOCK TABLES `Users` WRITE;
/*!40000 ALTER TABLE `Users` DISABLE KEYS */;
INSERT INTO `Users` VALUES (1,'admin','pbkdf2:sha256:600000$XDfBrSTTdCu2Q9el$c9c491c9e3c1a2b3d72a0d3e5ca6b61c6cbb0d6a8abf4ad76eac9e5e7cec8c68',1),(2,'user','pbkdf2:sha256:600000$CnxhgFOIKST7lNRa$5d0ed06d7e65a2c883a94e73b11b4a561dd73b28a645aeeb1c761bbe21aa94a8',0),(3,'user1','pbkdf2:sha256:600000$L9K97rXSS3HZdviN$e22898f200471c6d69d23728c852c395c9b3f99e6d1da2d9c975fe42d22fdafc',1),(4,'user2','pbkdf2:sha256:600000$zYmNJjr0Gxyl9oUj$c184acc5fd84c41ef3859369e8938d3a28ed664fb0c79dfad741c7165293e052',1),(5,'user3','pbkdf2:sha256:600000$iQx9Dh0GvYfZdlhM$0d88e41bfc2913310f839d5ab51f53fc8262f416e7cdfde8d15b28ba2dcac148',0);
/*!40000 ALTER TABLE `Users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-28 22:55:23
