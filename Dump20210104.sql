-- MySQL dump 10.13  Distrib 8.0.22, for Win64 (x86_64)
--
-- Host: localhost    Database: saledb
-- ------------------------------------------------------
-- Server version	8.0.22

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
-- Table structure for table `airport`
--

DROP TABLE IF EXISTS `airport`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `airport` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=44 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `airport`
--

LOCK TABLES `airport` WRITE;
/*!40000 ALTER TABLE `airport` DISABLE KEYS */;
INSERT INTO `airport` VALUES (1,'Bac Kinh'),(2,'Binh Dinh'),(3,'Ca Mau'),(4,'Can Tho'),(5,'Da Nang'),(6,'Dak Lak'),(7,'Dien Bien Phu'),(8,'Gia Lai'),(9,'Ha Noi'),(10,'Hai Phong'),(11,'Hue'),(12,'Jeju'),(13,'Khanh Hoa'),(14,'Kien Giang'),(18,'Lam Dong'),(19,'Los Angeles'),(21,'Ma Cao'),(24,'Muan'),(16,'Nghe An'),(32,'Phu Quoc'),(22,'Phu Yen'),(17,'Quang Binh'),(20,'Quang Nam'),(31,'Quang Ninh'),(23,'San Francisco'),(28,'Seoul'),(15,'Thanh Hoa'),(30,'Thuong Hai'),(25,'Tokyo'),(27,'TP HCM'),(33,'Tra Vinh'),(26,'Vu Han'),(29,'Vung Tau');
/*!40000 ALTER TABLE `airport` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bill`
--

DROP TABLE IF EXISTS `bill`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bill` (
  `id` int NOT NULL AUTO_INCREMENT,
  `datetime_bill` date DEFAULT NULL,
  `money` float NOT NULL DEFAULT '400000',
  `client_id` int NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `client_id` (`client_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `bill_ibfk_1` FOREIGN KEY (`client_id`) REFERENCES `client` (`id`),
  CONSTRAINT `bill_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bill`
--

LOCK TABLES `bill` WRITE;
/*!40000 ALTER TABLE `bill` DISABLE KEYS */;
INSERT INTO `bill` VALUES (1,'2020-12-26',2500000,1,2),(2,'2020-12-26',100000,2,2);
/*!40000 ALTER TABLE `bill` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `booking`
--

DROP TABLE IF EXISTS `booking`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `booking` (
  `id` int NOT NULL AUTO_INCREMENT,
  `datetime_booking` date DEFAULT NULL,
  `amount_seat` int DEFAULT '1',
  `client_id` int NOT NULL,
  `flight_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `client_id` (`client_id`),
  KEY `flight_id` (`flight_id`),
  CONSTRAINT `booking_ibfk_1` FOREIGN KEY (`client_id`) REFERENCES `client` (`id`),
  CONSTRAINT `booking_ibfk_2` FOREIGN KEY (`flight_id`) REFERENCES `flight` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `booking`
--

LOCK TABLES `booking` WRITE;
/*!40000 ALTER TABLE `booking` DISABLE KEYS */;
INSERT INTO `booking` VALUES (1,'2020-12-26',1,1,3),(2,'2020-12-26',1,2,4),(3,'2020-12-26',1,4,7);
/*!40000 ALTER TABLE `booking` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `client`
--

DROP TABLE IF EXISTS `client`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `client` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `phone` varchar(50) NOT NULL,
  `idcard` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `idcard` (`idcard`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `client`
--

LOCK TABLES `client` WRITE;
/*!40000 ALTER TABLE `client` DISABLE KEYS */;
INSERT INTO `client` VALUES (1,'Nguyen Thi Minh Thu','0346279377','2222222'),(2,'Thach Ngoc Hai','0346279370','888888888'),(3,'Nguyen Van Tan','0346279399','33333333'),(4,'Le Duc Tan','0346279123','55555555'),(5,'Nguyen Tra My','0346279081','000000'),(6,'Nguyen Ha Nam','0346279084','0000001'),(7,'Nguyễn Văn Nam','0975226327','1111112222'),(8,'','',''),(9,'Nguyễn Văn Nam','0975226327','1234567'),(10,'Nguyễn Văn Nam','0975226327','12345678'),(11,'Nguyễn Văn Nam','0975226327','11111113');
/*!40000 ALTER TABLE `client` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `flight`
--

DROP TABLE IF EXISTS `flight`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `flight` (
  `id` int NOT NULL AUTO_INCREMENT,
  `date_flight_from` date DEFAULT NULL,
  `date_flight_to` date DEFAULT NULL,
  `flight_route_id` int NOT NULL,
  `plane_id` int NOT NULL,
  `time_begin` time DEFAULT NULL,
  `time_end` time DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `flight_route_id` (`flight_route_id`),
  KEY `plane_id` (`plane_id`),
  CONSTRAINT `flight_ibfk_1` FOREIGN KEY (`flight_route_id`) REFERENCES `flightroute` (`id`),
  CONSTRAINT `flight_ibfk_2` FOREIGN KEY (`plane_id`) REFERENCES `plane` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `flight`
--

LOCK TABLES `flight` WRITE;
/*!40000 ALTER TABLE `flight` DISABLE KEYS */;
INSERT INTO `flight` VALUES (3,'2020-12-26','2020-12-31',1,2,'09:00:00','00:00:00'),(4,'2020-12-26','2020-12-29',2,1,'10:00:00','00:00:00'),(5,'2020-12-26','2020-12-28',2,4,'11:00:00','00:00:00'),(6,'2020-12-26','2021-01-08',3,2,'17:00:00','20:00:00'),(7,'2020-12-26','2020-12-26',1,1,'17:00:00','21:00:00'),(12,'2020-12-31','2020-12-31',1,3,'13:00:00','17:00:00'),(13,'2020-12-31','2021-01-01',2,1,'12:00:00','04:00:00'),(14,'2020-12-31','2020-12-31',3,4,'10:00:00','20:00:00'),(15,'2021-01-01','2021-01-01',3,1,'12:00:00','04:00:00'),(16,'2021-01-01','2021-01-01',1,1,'04:00:00','23:00:00'),(17,'2021-01-02','2021-01-02',3,1,'10:00:00','21:00:00'),(18,'2021-01-02','2021-01-02',2,1,'13:00:00','17:00:00'),(19,'2021-01-03','2021-01-03',1,1,'10:00:00','00:00:00'),(20,'2021-01-04','2021-01-05',2,1,'13:00:00','17:00:00'),(21,'2021-01-04','2021-01-05',4,1,'10:00:00','21:00:00');
/*!40000 ALTER TABLE `flight` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `flight_flightdetail`
--

DROP TABLE IF EXISTS `flight_flightdetail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `flight_flightdetail` (
  `flight_id` int NOT NULL,
  `flightdetail_id` int NOT NULL,
  PRIMARY KEY (`flight_id`,`flightdetail_id`),
  KEY `flightdetail_id` (`flightdetail_id`),
  CONSTRAINT `flight_flightdetail_ibfk_1` FOREIGN KEY (`flight_id`) REFERENCES `flight` (`id`),
  CONSTRAINT `flight_flightdetail_ibfk_2` FOREIGN KEY (`flightdetail_id`) REFERENCES `flightdetail` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `flight_flightdetail`
--

LOCK TABLES `flight_flightdetail` WRITE;
/*!40000 ALTER TABLE `flight_flightdetail` DISABLE KEYS */;
INSERT INTO `flight_flightdetail` VALUES (3,2),(4,2),(5,3),(6,3),(15,3),(7,4),(12,4),(13,4),(16,4),(14,9),(14,10),(14,11),(20,11),(17,12),(17,13),(18,13),(19,14),(19,15),(21,16);
/*!40000 ALTER TABLE `flight_flightdetail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `flightdetail`
--

DROP TABLE IF EXISTS `flightdetail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `flightdetail` (
  `id` int NOT NULL AUTO_INCREMENT,
  `inter_airport` varchar(30) DEFAULT 'HongKong',
  `waiting_time` int DEFAULT '0',
  `note` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `flightdetail`
--

LOCK TABLES `flightdetail` WRITE;
/*!40000 ALTER TABLE `flightdetail` DISABLE KEYS */;
INSERT INTO `flightdetail` VALUES (2,'Bac Kinh',120,NULL),(3,'Ha Noi',180,NULL),(4,'HongKong',120,NULL),(9,'HongKong',120,NULL),(10,'Ha Noi',120,NULL),(11,'Quang Nam',60,NULL),(12,'HongKong',120,NULL),(13,'Ha Noi',120,NULL),(14,'HongKong',60,NULL),(15,'Ha Noi',60,NULL),(16,'HongKong',120,NULL);
/*!40000 ALTER TABLE `flightdetail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `flightroute`
--

DROP TABLE IF EXISTS `flightroute`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `flightroute` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_airport1` int DEFAULT '1',
  `id_airport2` int DEFAULT '2',
  `name` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `flightroute`
--

LOCK TABLES `flightroute` WRITE;
/*!40000 ALTER TABLE `flightroute` DISABLE KEYS */;
INSERT INTO `flightroute` VALUES (1,12,20,'Jeju-QuangNam'),(2,13,20,'KhanhHoa-QuangNam'),(3,17,29,'QuangBinh-VungTau'),(4,1,2,'BacKinh-BinhDinh');
/*!40000 ALTER TABLE `flightroute` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `plane`
--

DROP TABLE IF EXISTS `plane`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `plane` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `amount_of_seat1` int DEFAULT '70',
  `amount_of_seat2` int DEFAULT '70',
  `quantity` int DEFAULT '140',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `plane`
--

LOCK TABLES `plane` WRITE;
/*!40000 ALTER TABLE `plane` DISABLE KEYS */;
INSERT INTO `plane` VALUES (1,'Boeing 787',120,70,190),(2,'Airbus A350',150,100,250),(3,'Airbus A330',70,70,140),(4,'Airbus A321',224,159,383),(5,'ATR 72-500',120,80,200);
/*!40000 ALTER TABLE `plane` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `priceflight`
--

DROP TABLE IF EXISTS `priceflight`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `priceflight` (
  `id` int NOT NULL AUTO_INCREMENT,
  `vnd` int DEFAULT '0',
  `name` varchar(45) DEFAULT NULL,
  `flight_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `priceflight_ibfk1_idx` (`flight_id`),
  CONSTRAINT `priceflight_ibfk1` FOREIGN KEY (`flight_id`) REFERENCES `flight` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `priceflight`
--

LOCK TABLES `priceflight` WRITE;
/*!40000 ALTER TABLE `priceflight` DISABLE KEYS */;
INSERT INTO `priceflight` VALUES (1,20000000,'QuangBinh-VungTau2',17),(2,10000000,'QuangBinh-VungTau1',17),(3,4000000,'Jeju-QuangNam2',19),(4,2000000,'Jeju-QuangNam1',19),(5,1000000,'KhanhHoa-QuangNam1',20),(6,400000,'KhanhHoa-QuangNam2',20),(7,200000,'BacKinh-BinhDinh1',21),(8,2500000,'BacKinh-BinhDinh2',21);
/*!40000 ALTER TABLE `priceflight` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ticket`
--

DROP TABLE IF EXISTS `ticket`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ticket` (
  `id` int NOT NULL AUTO_INCREMENT,
  `status` tinyint(1) DEFAULT '1',
  `price_flight_id` int NOT NULL,
  `type_ticket_id` int NOT NULL,
  `flight_id` int NOT NULL,
  `client_id` int NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `price_flight_id` (`price_flight_id`),
  KEY `type_ticket_id` (`type_ticket_id`),
  KEY `flight_id` (`flight_id`),
  KEY `client_id` (`client_id`),
  KEY `ticket_ibfk_5` (`user_id`),
  CONSTRAINT `ticket_ibfk_1` FOREIGN KEY (`price_flight_id`) REFERENCES `priceflight` (`id`),
  CONSTRAINT `ticket_ibfk_2` FOREIGN KEY (`type_ticket_id`) REFERENCES `typeticket` (`id`),
  CONSTRAINT `ticket_ibfk_3` FOREIGN KEY (`flight_id`) REFERENCES `flight` (`id`),
  CONSTRAINT `ticket_ibfk_4` FOREIGN KEY (`client_id`) REFERENCES `client` (`id`),
  CONSTRAINT `ticket_ibfk_5` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `ticket_chk_1` CHECK ((`status` in (0,1)))
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ticket`
--

LOCK TABLES `ticket` WRITE;
/*!40000 ALTER TABLE `ticket` DISABLE KEYS */;
INSERT INTO `ticket` VALUES (1,1,1,1,3,1,2),(2,1,5,2,4,2,2),(3,1,2,1,3,4,2);
/*!40000 ALTER TABLE `ticket` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `typeticket`
--

DROP TABLE IF EXISTS `typeticket`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `typeticket` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `typeticket`
--

LOCK TABLES `typeticket` WRITE;
/*!40000 ALTER TABLE `typeticket` DISABLE KEYS */;
INSERT INTO `typeticket` VALUES (1,'Loai 1'),(2,'Loai 2');
/*!40000 ALTER TABLE `typeticket` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `typeticket_booking`
--

DROP TABLE IF EXISTS `typeticket_booking`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `typeticket_booking` (
  `typeticket_id` int NOT NULL,
  `booking_id` int NOT NULL,
  PRIMARY KEY (`typeticket_id`,`booking_id`),
  KEY `booking_id` (`booking_id`),
  CONSTRAINT `typeticket_booking_ibfk_1` FOREIGN KEY (`typeticket_id`) REFERENCES `typeticket` (`id`),
  CONSTRAINT `typeticket_booking_ibfk_2` FOREIGN KEY (`booking_id`) REFERENCES `booking` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `typeticket_booking`
--

LOCK TABLES `typeticket_booking` WRITE;
/*!40000 ALTER TABLE `typeticket_booking` DISABLE KEYS */;
INSERT INTO `typeticket_booking` VALUES (1,1),(1,2),(2,3);
/*!40000 ALTER TABLE `typeticket_booking` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `phone` varchar(50) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `active` tinyint(1) NOT NULL DEFAULT '1',
  `type` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `username` (`username`),
  CONSTRAINT `user_chk_1` CHECK ((`active` in (0,1))),
  CONSTRAINT `user_chk_2` CHECK ((`type` in (0,1)))
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'Nguyen Thi Minh Thu','minhthuthum@gmail.com','0346279377','mint','a41c70912a36ebac23655666ef167c57',1,1),(2,'Nguyen Minh Thu','minhthu@gmail.com','0346279378','mint1002','a41c70912a36ebac23655666ef167c57',1,0);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'saledb'
--

--
-- Dumping routines for database 'saledb'
--
/*!50003 DROP FUNCTION IF EXISTS `fun_check_name_airport` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` FUNCTION `fun_check_name_airport`(id int) RETURNS varchar(30) CHARSET utf8mb4
    DETERMINISTIC
BEGIN 
	declare air_name varchar(30);
    set air_name = (select a.name from airport as a where a.id = id) ;
	return air_name ;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `proc_search_flight` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `proc_search_flight`(
	IN id_air_from int, IN id_air_to int, IN datefrom date
)
BEGIN
	SELECT p.quantity, sum(b.amount_seat) FROM flightroute as fr, flight as f,plane as p, booking as b
	WHERE  fr.id_airport1 = id_air_from and fr.id_airport2 = id_air_to and fr.id = f.flight_route_id and f.date_flight_from = datefrom and f.plane_id = p.id and f.id = b.flight_id
	GROUP BY p.quantity, p.id ;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-01-04 17:16:18
