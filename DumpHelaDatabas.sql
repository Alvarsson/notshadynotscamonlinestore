-- MySQL dump 10.13  Distrib 8.0.18, for macos10.14 (x86_64)
--
-- Host: localhost    Database: NoScam
-- ------------------------------------------------------
-- Server version	8.0.18

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
-- Table structure for table `articles`
--

DROP TABLE IF EXISTS `articles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `articles` (
  `article_number` int(11) NOT NULL AUTO_INCREMENT,
  `stock_quantity` int(11) NOT NULL,
  `picture_url` varchar(150) COLLATE utf8_bin DEFAULT NULL,
  `category` int(11) NOT NULL,
  `price` int(11) NOT NULL,
  `article_name` varchar(30) COLLATE utf8_bin NOT NULL,
  `article_description` varchar(200) COLLATE utf8_bin DEFAULT NULL,
  PRIMARY KEY (`article_number`),
  UNIQUE KEY `ArtNamn_UNIQUE` (`article_name`),
  UNIQUE KEY `ArtNummer_UNIQUE` (`article_number`),
  KEY `fk_category_idx` (`category`),
  CONSTRAINT `fk_category` FOREIGN KEY (`category`) REFERENCES `categories` (`unique_id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `articles`
--

LOCK TABLES `articles` WRITE;
/*!40000 ALTER TABLE `articles` DISABLE KEYS */;
INSERT INTO `articles` VALUES (1,10,NULL,1,20,'Gran','Ett barrigt träd'),(2,15,NULL,1,50,'Tall','Högt barrigt träd'),(3,7,NULL,2,13,'Asp','Ett lövigt träd');
/*!40000 ALTER TABLE `articles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `categories`
--

DROP TABLE IF EXISTS `categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categories` (
  `unique_id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Unikt id',
  `category_name` varchar(30) COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (`unique_id`),
  UNIQUE KEY `category_name_UNIQUE` (`category_name`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categories`
--

LOCK TABLES `categories` WRITE;
/*!40000 ALTER TABLE `categories` DISABLE KEYS */;
INSERT INTO `categories` VALUES (1,'Barrträd'),(5,'Gamer-träd'),(2,'Lövträd'),(3,'Små träd'),(4,'Stora träd'),(7,'Träd från kända serier'),(6,'Wannabee-träd');
/*!40000 ALTER TABLE `categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comments`
--

DROP TABLE IF EXISTS `comments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `comments` (
  `comment_id` int(11) NOT NULL AUTO_INCREMENT,
  `article_number` int(11) NOT NULL COMMENT 'Foreign key connected with table articles: article_number',
  `rating` int(11) NOT NULL,
  `comment` varchar(300) COLLATE utf8_bin NOT NULL,
  `timestamp` datetime NOT NULL,
  `customer_id` int(11) NOT NULL COMMENT 'Foreign key connected with table users: customer_id',
  PRIMARY KEY (`comment_id`),
  UNIQUE KEY `unique_id_UNIQUE` (`comment_id`),
  KEY `article_number_idx` (`article_number`),
  KEY `customer_id_idx` (`customer_id`),
  KEY `customer_id_comment` (`customer_id`),
  KEY `customer_id_idc` (`customer_id`),
  CONSTRAINT `article_number` FOREIGN KEY (`article_number`) REFERENCES `articles` (`article_number`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `customer_idc` FOREIGN KEY (`customer_id`) REFERENCES `users` (`customer_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comments`
--

LOCK TABLES `comments` WRITE;
/*!40000 ALTER TABLE `comments` DISABLE KEYS */;
/*!40000 ALTER TABLE `comments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_items`
--

DROP TABLE IF EXISTS `order_items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order_items` (
  `order_item_id` int(11) NOT NULL AUTO_INCREMENT,
  `article_number` int(11) NOT NULL,
  `order_number_item` int(11) NOT NULL,
  `article_quantity` int(11) NOT NULL,
  PRIMARY KEY (`order_item_id`),
  UNIQUE KEY `order_item_id_UNIQUE` (`order_item_id`),
  KEY `order_number_idx` (`order_number_item`),
  CONSTRAINT `order_number` FOREIGN KEY (`order_number_item`) REFERENCES `users` (`customer_id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_items`
--

LOCK TABLES `order_items` WRITE;
/*!40000 ALTER TABLE `order_items` DISABLE KEYS */;
/*!40000 ALTER TABLE `order_items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders` (
  `order_number` int(11) NOT NULL AUTO_INCREMENT,
  `user` int(11) NOT NULL COMMENT 'Foreign key connected to table users: customer_id',
  `timestamp` datetime NOT NULL,
  PRIMARY KEY (`order_number`),
  UNIQUE KEY `order_number_UNIQUE` (`order_number`),
  KEY `user_idx` (`user`),
  CONSTRAINT `user` FOREIGN KEY (`user`) REFERENCES `users` (`customer_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders`
--

LOCK TABLES `orders` WRITE;
/*!40000 ALTER TABLE `orders` DISABLE KEYS */;
/*!40000 ALTER TABLE `orders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `shopping_cart`
--

DROP TABLE IF EXISTS `shopping_cart`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `shopping_cart` (
  `cart_id` int(11) NOT NULL AUTO_INCREMENT,
  `customer_id` int(11) NOT NULL COMMENT 'Foreign key connected to table users: customer_id',
  PRIMARY KEY (`cart_id`),
  UNIQUE KEY `cart_id_UNIQUE` (`cart_id`),
  KEY `customer_id_idx` (`customer_id`),
  CONSTRAINT `customer_id` FOREIGN KEY (`customer_id`) REFERENCES `users` (`customer_id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shopping_cart`
--

LOCK TABLES `shopping_cart` WRITE;
/*!40000 ALTER TABLE `shopping_cart` DISABLE KEYS */;
/*!40000 ALTER TABLE `shopping_cart` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `shopping_cart_items`
--

DROP TABLE IF EXISTS `shopping_cart_items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `shopping_cart_items` (
  `cart_items_id` int(11) NOT NULL AUTO_INCREMENT,
  `article` int(11) NOT NULL,
  `shopping_cart_id` int(11) NOT NULL,
  `article_quantity` int(11) DEFAULT NULL,
  PRIMARY KEY (`cart_items_id`),
  UNIQUE KEY `cart_items_id_UNIQUE` (`cart_items_id`),
  KEY `article_idx` (`article`),
  KEY `shopping_cart_id_idx` (`shopping_cart_id`),
  CONSTRAINT `article` FOREIGN KEY (`article`) REFERENCES `articles` (`article_number`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `shopping_cart_id` FOREIGN KEY (`shopping_cart_id`) REFERENCES `shopping_cart` (`cart_id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shopping_cart_items`
--

LOCK TABLES `shopping_cart_items` WRITE;
/*!40000 ALTER TABLE `shopping_cart_items` DISABLE KEYS */;
/*!40000 ALTER TABLE `shopping_cart_items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `customer_id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(45) COLLATE utf8_bin NOT NULL,
  `last_name` varchar(70) COLLATE utf8_bin NOT NULL,
  `user_name` varchar(45) COLLATE utf8_bin NOT NULL,
  `password` varchar(60) COLLATE utf8_bin NOT NULL,
  `mail` varchar(100) COLLATE utf8_bin DEFAULT NULL,
  `adress` varchar(100) COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (`customer_id`),
  UNIQUE KEY `customer_id_UNIQUE` (`customer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-11-15 17:14:12
