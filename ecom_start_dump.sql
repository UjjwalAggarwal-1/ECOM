-- MySQL dump 10.13  Distrib 8.0.28, for Win64 (x86_64)
--
-- Host: localhost    Database: ecom
-- ------------------------------------------------------
-- Server version	8.0.28

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `address`
--

DROP TABLE IF EXISTS `address`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `address` (
  `id` int NOT NULL AUTO_INCREMENT,
  `address_line1` varchar(100) NOT NULL,
  `address_line2` varchar(100) DEFAULT NULL,
  `city` varchar(50) NOT NULL,
  `country` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `address`
--

LOCK TABLES `address` WRITE;
/*!40000 ALTER TABLE `address` DISABLE KEYS */;
INSERT INTO `address` VALUES (1,'Address Line 1A','Address Line 2A','CityA','CountryA'),(2,'Address Line 1B','Address Line 2B','CityB','CountryB'),(3,'Address Line 1C','Address Line 2C','CityC','CountryC'),(4,'Address Line 1D','Address Line 2D','CityD','CountryD'),(5,'Address Line 1E','Address Line 2E','CityE','CountryE'),(6,'Address Line 1F','Address Line 2F','CityF','CountryF'),(7,'Address Line 1G','Address Line 2G','CityG','CountryG'),(8,'Address Line 1H','Address Line 2H','CityH','CountryH'),(9,'Address Line 1I','Address Line 2I','CityI','CountryI'),(10,'Address Line 1J','Address Line 2J','CityJ','CountryJ');
/*!40000 ALTER TABLE `address` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `address_pincode`
--

DROP TABLE IF EXISTS `address_pincode`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `address_pincode` (
  `id` int NOT NULL,
  `pincode` varchar(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  CONSTRAINT `address_pincode_ibfk_1` FOREIGN KEY (`id`) REFERENCES `address` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `address_pincode`
--

LOCK TABLES `address_pincode` WRITE;
/*!40000 ALTER TABLE `address_pincode` DISABLE KEYS */;
INSERT INTO `address_pincode` VALUES (1,'123456'),(2,'234567'),(3,'345678'),(4,'456789'),(5,'567890'),(6,'678901'),(7,'789012'),(8,'890123'),(9,'901234'),(10,'012345');
/*!40000 ALTER TABLE `address_pincode` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cart`
--

DROP TABLE IF EXISTS `cart`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cart` (
  `customer_id` bigint NOT NULL,
  `item_id` bigint NOT NULL,
  `quantity` int NOT NULL,
  UNIQUE KEY `cart_items_cart_id_item_id_unique` (`customer_id`,`item_id`),
  KEY `cart_item_id_fk_item_id` (`item_id`),
  CONSTRAINT `cart_customer_id_fk_customer_user_id` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`user_id`),
  CONSTRAINT `cart_item_id_fk_item_id` FOREIGN KEY (`item_id`) REFERENCES `item` (`id`),
  CONSTRAINT `cart_chk_1` CHECK ((`quantity` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cart`
--

LOCK TABLES `cart` WRITE;
/*!40000 ALTER TABLE `cart` DISABLE KEYS */;
INSERT INTO `cart` VALUES (17,6,3),(18,6,3),(18,7,5),(18,25,2),(19,3,1),(19,4,4),(19,5,9),(19,21,2),(20,6,1),(20,12,5),(20,15,8),(20,16,5);
/*!40000 ALTER TABLE `cart` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `category`
--

DROP TABLE IF EXISTS `category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `category` (
  `name` varchar(50) DEFAULT NULL,
  `image` varchar(150) DEFAULT NULL,
  `id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `category`
--

LOCK TABLES `category` WRITE;
/*!40000 ALTER TABLE `category` DISABLE KEYS */;
INSERT INTO `category` VALUES ('ELECTRONICS','category_images/electronics.jpg',1),('CLOTHING','category_images/clothing.jpg',2),('BABY','category_images/baby.jpg',3),('SPORTS','category_images/sports.jpg',4),('HOME','category_images/home.jpg',5),('TOYS','category_images/toys.jpg',6),('BEAUTY','category_images/beauty.jpg',7),('GROCERY','category_images/grocery.jpg',8),('AUTOMOTIVE','category_images/automotive.jpg',9),('BOOKS','category_images/books.jpg',10),('HEALTH','category_images/health.jpg',11),('SHOES','category_images/shoes.jpg',12),('JEWELRY','category_images/jewelry.jpg',13),('TOOLS','category_images/tools.jpg',14),('GARDEN','category_images/garden.jpg',15);
/*!40000 ALTER TABLE `category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `coupon_code`
--

DROP TABLE IF EXISTS `coupon_code`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `coupon_code` (
  `code` varchar(20) NOT NULL,
  `discount` float unsigned NOT NULL,
  `valid_from` datetime NOT NULL,
  `valid_to` datetime NOT NULL,
  `usage_limit` int unsigned DEFAULT NULL,
  `used_count` int unsigned NOT NULL DEFAULT '0',
  UNIQUE KEY `code` (`code`),
  CONSTRAINT `coupon_code_chk_1` CHECK (((`discount` >= 0) and (`discount` <= 1)))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `coupon_code`
--

LOCK TABLES `coupon_code` WRITE;
/*!40000 ALTER TABLE `coupon_code` DISABLE KEYS */;
/*!40000 ALTER TABLE `coupon_code` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customer`
--

DROP TABLE IF EXISTS `customer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customer` (
  `user_id` bigint NOT NULL,
  `total_purchases` int unsigned DEFAULT '0',
  `address_id` int DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  KEY `customer_address_id_fk_address_id` (`address_id`),
  CONSTRAINT `customer_address_id_fk_address_id` FOREIGN KEY (`address_id`) REFERENCES `address` (`id`),
  CONSTRAINT `customer_user_id_fk_user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer`
--

LOCK TABLES `customer` WRITE;
/*!40000 ALTER TABLE `customer` DISABLE KEYS */;
INSERT INTO `customer` VALUES (16,0,1),(17,0,2),(18,0,3),(19,0,4),(20,0,5);
/*!40000 ALTER TABLE `customer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `item`
--

DROP TABLE IF EXISTS `item`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `item` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `price` int unsigned NOT NULL,
  `description` longtext,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `total_sale` int DEFAULT '0',
  `stock` int DEFAULT '0',
  `seller_id` bigint NOT NULL,
  `category_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `item_name_seller_id_unique` (`name`,`seller_id`),
  KEY `item_seller_id_fk_seller_user_id` (`seller_id`),
  KEY `item_category_id_fk_category_id` (`category_id`),
  CONSTRAINT `item_category_id_fk_category_id` FOREIGN KEY (`category_id`) REFERENCES `category` (`id`),
  CONSTRAINT `item_seller_id_fk_seller_user_id` FOREIGN KEY (`seller_id`) REFERENCES `seller` (`user_id`),
  CONSTRAINT `item_chk_1` CHECK ((`price` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `item`
--

LOCK TABLES `item` WRITE;
/*!40000 ALTER TABLE `item` DISABLE KEYS */;
INSERT INTO `item` VALUES (1,'iPhone 11',1000,'iPhone 11 is a smartphone designed, developed, and marketed by Apple Inc. It is the twelfth generation of the iPhone. It was announced on September 10, 2019, alongside the higher-end iPhone 11 Pro and iPhone 11 Pro Max, at the Steve Jobs Theater in the Apple Park campus. The iPhone 11 features a 6.1-inch Liquid Retina IPS LCD display with support for Dolby Vision and HDR10, an Apple-designed A13 Bionic chipset, a dual-camera system on the back consisting of a 12-megapixel wide-angle camera and a 12-megapixel ultra-wide-angle camera, a 12-megapixel front-facing camera, and a 3,110 mAh battery. It is available in six colors: purple, green, yellow, black, white, and PRODUCT(RED).','2023-04-17 15:56:42',22,0,16,1),(2,'iPhone 11 Pro',1200,'iPhone 11 Pro is a smartphone designed, developed, and marketed by Apple Inc. It is the thirteenth generation of the iPhone. It was announced on September 10, 2019, alongside the higher-end iPhone 11 Pro Max and iPhone 11, at the Steve Jobs Theater in the Apple Park campus. The iPhone 11 Pro features a 5.8-inch Super Retina XDR OLED display with support for Dolby Vision and HDR10, an Apple-designed A13 Bionic chipset, a triple-camera system on the back consisting of a 12-megapixel wide-angle camera, a 12-megapixel ultra-wide-angle camera, and a 12-megapixel telephoto camera, a 12-megapixel front-facing camera, and a 3,190 mAh battery. It is available in four colors: midnight green, space gray, silver, and gold.','2023-04-17 15:56:42',44,0,16,1),(3,'iPhone 11 Pro Max',1300,'iPhone 11 Pro Max is a smartphone designed, developed, and marketed by Apple Inc. It is the thirteenth generation of the iPhone. It was announced on September 10, 2019, alongside the higher-end iPhone 11 Pro and iPhone 11, at the Steve Jobs Theater in the Apple Park campus. The iPhone 11 Pro Max features a 6.5-inch Super Retina XDR OLED display with support for Dolby Vision and HDR10, an Apple-designed A13 Bionic chipset, a triple-camera system on the back consisting of a 12-megapixel wide-angle camera, a 12-megapixel ultra-wide-angle camera, and a 12-megapixel telephoto camera, a 12-megapixel front-facing camera, and a 3,500 mAh battery. It is available in four colors: midnight green, space gray, silver, and gold.','2023-04-17 15:56:42',55,0,16,1),(4,'MacBook Pro',1800,'MacBook Pro is a line of Macintosh portable computers introduced in January 2006 by Apple Inc. It is the high-end model of the MacBook family and is currently available in 13- and 16-inch screen sizes. A 15-inch version was available between April 2006 and June 2012. The first generation MacBook Pro was externally similar to the PowerBook G4 it replaced, but inside the case was completely redesigned, incorporating an Intel processor, a glass trackpad, and LED-backlit display. The MacBook Pro is the successor to the PowerBook G4 and is Apple\'s current high-end consumer notebook.','2023-04-17 15:56:42',6,0,16,1),(5,'MacBook Air',1500,'MacBook Air is a line of Macintosh portable computers developed and manufactured by Apple Inc. It consists of a full-size keyboard, a machined aluminum case, and a thin light structure. The Air is available in 13-inch and 11-inch screen sizes. The 13-inch model was available in silver or space gray, while the 11-inch model was available in white or silver. The 13-inch MacBook Air was discontinued on October 26, 2018, and the 11-inch model was discontinued on July 15, 2017. The MacBook Air is the successor to the MacBook and is currently Apple\'s most affordable notebook computer.','2023-04-17 15:56:42',7,0,16,1),(6,'iPad',400,'iPad is a line of tablet computers designed, developed and marketed by Apple Inc., which run the iOS mobile operating system. The first iPad was released on April 3, 2010; the most recent iPad models are the 10.2-inch iPad (8th generation) released on September 18, 2020, and the 11-inch iPad Pro (2nd generation) released on November 7, 2017. The user interface is built around the device\'s multi-touch screen, including a virtual keyboard. The iPad includes built-in Wi-Fi and cellular connectivity on select models. As of January 2019, there have been over 500 million iPads sold.','2023-04-17 15:56:42',88,0,16,1),(7,'AirPods',200,'AirPods are wireless Bluetooth earbuds created by Apple Inc. They were introduced on September 7, 2016, as a wireless alternative to the EarPods that come bundled with iPhones. The AirPods are designed to be used with Apple\'s W1 chip, which is also used in the Apple Watch and Beats headphones. The AirPods are compatible with all Apple devices that support Bluetooth 4.2 and later, including the iPhone, iPad, Apple Watch, and Mac. The AirPods are also compatible with Android devices that support Bluetooth 5.0 and later.','2023-04-17 15:56:42',19,0,16,1),(8,'T-Shirt',800,'A T-shirt is a style of unisex fabric shirt named after the T shape of its body and sleeves. Traditionally it has short sleeves and a round neckline, known as a crew neck, which lacks a collar. T-shirts are generally made of a light, inexpensive fabric and are easy to clean. T-shirts are also a medium for expression and advertising, with any imaginable combination of words, art and photographs on display.','2023-04-17 15:56:42',10,0,16,2),(9,'Shoes',1000,'A shoe is an item of footwear intended to protect and comfort the human foot while the wearer is doing various activities. Shoes are also used as an item of decoration and fashion. The design of shoes has varied enormously through time and from culture to culture, with appearance originally being tied to function. Additionally, fashion has often dictated many design elements, such as whether shoes have very high heels or flat ones. Contemporary footwear in the 2010s varies widely in style, complexity and cost. Basic sandals may consist of only a thin sole and simple strap and be sold for a low cost. High fashion shoes made by famous designers may be made of expensive materials, use complex construction and sell for hundreds or even thousands of dollars a pair.','2023-04-17 15:56:42',11,0,16,2),(10,'Watch',2000,'A watch is a small timepiece intended to be carried or worn by a person. It is designed to keep working despite the motions caused by the person\'s activities. A wristwatch is designed to be worn around the wrist, attached by a watch strap or other type of bracelet. A pocket watch is designed for a person to carry in a pocket. Watches progressed in the 17th century from spring-powered clocks, which appeared as early as the 14th century. During most of its history the watch was a mechanical device, driven by clockwork, powered by winding a mainspring, and keeping time with an oscillating balance wheel. These are called mechanical watches. In the 1960s the electronic quartz watch was invented, which was powered by a battery and kept time with a vibrating quartz crystal.','2023-04-17 15:56:42',12,0,16,2),(11,'Sunglasses',500,'Sunglasses or sun glasses are a form of protective eyewear designed primarily to prevent bright sunlight and high-energy visible light from damaging or discomforting the eyes. They can sometimes also function as a visual aid, as variously termed spectacles or glasses exist, featuring lenses that are colored, polarized or darkened. In the early 20th century, they were also known as sun cheaters. In the 20th century, they were known as shades. In the 21st century, a generic form of the term \'sunglasses\' is used.','2023-04-17 15:56:42',77,0,16,2),(12,'Headphones',1500,'Headphones or earphones are a pair of small loudspeaker drivers worn on or around the head over a user\'s ears. They are electroacoustic transducers, which convert an electrical signal to a corresponding sound. Headphones are also known as ear speakers, earphones, or, colloquially, cans. Headphones are used by a wide range of people for a wide variety of reasons. They are used by audiophiles for critical listening and personal audio enjoyment, by gamers for immersive gaming, by musicians for practice and live performances, by moviegoers for private listening, and by air travellers for audio and video entertainment.','2023-04-17 15:56:42',33,0,16,2),(13,'Backpack',2000,'A backpack is, in its simplest form, a cloth sack carried on one\'s back and secured with two straps that go over the shoulders, but there can be variations. The backpack may have one or two shoulder straps, each of which can be padded or unpadded, and can be adjustable in length. The backpack may also have a handle at the top, a waist belt, and compression straps that tighten the pack to reduce its volume. Backpacks are often made of nylon, canvas, leather, or vinyl.','2023-04-17 15:56:42',14,0,17,2),(14,'Baby Powder',500,'Baby powder is a talcum powder used for babies. It is used to keep the skin dry and prevent rashes. It is also used to keep the diaper area dry. It is used to keep the skin soft and smooth. It is used to keep the skin dry and prevent rashes. It is also used to keep the diaper area dry. It is used to keep the skin soft and smooth.','2023-04-17 15:56:42',5,0,17,3),(15,'Baby Soap',1000,'Baby soap is a soap used for babies. It is used to keep the skin soft and smooth. It is used to keep the skin dry and prevent rashes. It is also used to keep the diaper area dry. It is used to keep the skin soft and smooth. It is used to keep the skin dry and prevent rashes. It is also used to keep the diaper area dry.','2023-04-17 15:56:42',9,0,17,3),(16,'Baby Oil',1500,'Baby oil is a mineral oil used for babies. It is used to keep the skin soft and smooth. It is used to keep the skin dry and prevent rashes. It is also used to keep the diaper area dry. It is used to keep the skin soft and smooth. It is used to keep the skin dry and prevent rashes. It is also used to keep the diaper area dry.','2023-04-17 15:56:42',4,0,17,3),(17,'Baby Shampoo',2000,'Baby shampoo is a shampoo used for babies. It is used to keep the skin soft and smooth. It is used to keep the skin dry and prevent rashes.','2023-04-17 15:56:42',5,0,17,3),(18,'Baby Lotion',2500,'Baby lotion is a lotion used for babies. It is used to keep the skin soft and smooth. It is used to keep the skin dry and prevent rashes. It is also used to keep the diaper area dry. It is used to keep the skin soft and smooth. It is used to keep the skin dry and prevent rashes. It is also used to keep the diaper area moist.','2023-04-17 15:56:42',7,0,17,3),(19,'Baby Wipes',3000,'Baby wipes are a type of wet wipe used for babies. It is used to keep the skin soft and smooth. It is used to keep the skin dry and prevent rashes. It is also used to keep the diaper area dry. It is used to keep the skin soft and smooth. It is used to keep the skin dry and prevent rashes. It is also used to keep the diaper area moist.','2023-04-17 15:56:42',6,0,17,3),(20,'Rare Necklace',5000,'A rare necklace is a necklace used for fashion by celebrities.','2023-04-17 15:56:42',8,0,17,13),(21,'Rare Ring',5000,'A rare ring is a ring used for babies. It is used for fashion by celebrities.','2023-04-17 15:56:42',8,0,18,13),(22,'Rare Bracelet',5000,'A rare bracelet is a bracelet use for fashion by celebrities.','2023-04-17 15:56:42',11,0,18,13),(23,'Rare Earrings',5000,'A rare earrings is used for fashion by celebrities.','2023-04-17 15:56:42',11,0,18,13),(24,'Rare Watch',5000,'A rare watch is a watch used for fashion by celebrities.','2023-04-17 15:56:42',11,0,18,13),(25,'Rare Sunglasses',5000,'A rare sunglasses is a sunglasses used for fashion by celebrities.','2023-04-17 15:56:42',11,0,18,13),(26,'Rare Belt',5000,'A rare belt is a belt used for babies. It is used to keep the skin soft and smooth. It is used to keep the skin dry and prevent rashes. It is also used to keep the diaper area dry. It is used to keep the skin soft and smooth. It is used to keep the skin dry and prevent rashes. It is also used to keep the diaper area dry.','2023-04-17 15:56:42',11,0,19,13),(27,'Rose seeds',500,'Rose seeds are for growing new lily plants. The pleasant aroma in surroundings.','2023-04-17 15:56:42',17,0,19,15),(28,'Jasmine seeds',350,'Jasmine seeds are used for growing new lily plants. The pleasant aroma in surroundings.','2023-04-17 15:56:42',11,0,19,15),(29,'Lily seeds',250,'Lily seeds are seeds used for growing new lily plants. The pleasant aroma in surroundings.','2023-04-17 15:56:42',20,0,20,15);
/*!40000 ALTER TABLE `item` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `itemimage`
--

DROP TABLE IF EXISTS `itemimage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `itemimage` (
  `id` int NOT NULL AUTO_INCREMENT,
  `image` varchar(100) NOT NULL,
  `item_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `itemimage_item_id_fk_item_id` (`item_id`),
  CONSTRAINT `itemimage_item_id_fk_item_id` FOREIGN KEY (`item_id`) REFERENCES `item` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `itemimage`
--

LOCK TABLES `itemimage` WRITE;
/*!40000 ALTER TABLE `itemimage` DISABLE KEYS */;
/*!40000 ALTER TABLE `itemimage` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order`
--

DROP TABLE IF EXISTS `order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `order_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `amount` int NOT NULL,
  `payment_uid` varchar(50) NOT NULL,
  `customer_id` bigint NOT NULL,
  `coupon_code_name` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `payment_uid` (`payment_uid`),
  KEY `order_customer_id_fk_customer_user_id` (`customer_id`),
  KEY `order_coupon_code_name_fk_coupon_code` (`coupon_code_name`),
  CONSTRAINT `order_coupon_code_name_fk_coupon_code` FOREIGN KEY (`coupon_code_name`) REFERENCES `coupon_code` (`code`),
  CONSTRAINT `order_customer_id_fk_customer_user_id` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order`
--

LOCK TABLES `order` WRITE;
/*!40000 ALTER TABLE `order` DISABLE KEYS */;
INSERT INTO `order` VALUES (1,'2023-04-16 15:56:42',2200,'12efew3',16,NULL),(2,'2023-04-15 15:56:42',3100,'2324324',17,NULL),(3,'2023-04-14 15:56:42',1900,'32323',18,NULL),(4,'2023-04-13 15:56:42',1000,'4234123',19,NULL),(5,'2023-04-12 15:56:42',3000,'5123123',20,NULL),(6,'2023-04-11 15:56:42',2000,'621132',16,NULL),(7,'2023-04-10 15:56:42',700,'7ewfwef',17,NULL),(8,'2023-04-09 15:56:42',6000,'8324324fw',18,NULL),(9,'2023-04-08 15:56:42',2500,'944ewd',19,NULL),(10,'2023-04-07 15:56:42',4100,'10wefew',20,NULL);
/*!40000 ALTER TABLE `order` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orderitem`
--

DROP TABLE IF EXISTS `orderitem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orderitem` (
  `status` enum('REFUNDED','ORDER_PLACED','SHIPPED','DELIVERED') NOT NULL,
  `quantity` int unsigned NOT NULL,
  `item_id` bigint NOT NULL,
  `order_id` bigint NOT NULL,
  `price` int NOT NULL,
  `from_address_id` int NOT NULL,
  `to_address_id` int NOT NULL,
  KEY `orderitem_item_id_fk_item_id` (`item_id`),
  KEY `orderitem_order_id_fk_order_id` (`order_id`),
  KEY `orderitem_from_address_id_fk_address_id` (`from_address_id`),
  KEY `orderitem_to_address_id_fk_address_id` (`to_address_id`),
  CONSTRAINT `orderitem_from_address_id_fk_address_id` FOREIGN KEY (`from_address_id`) REFERENCES `address` (`id`),
  CONSTRAINT `orderitem_item_id_fk_item_id` FOREIGN KEY (`item_id`) REFERENCES `item` (`id`),
  CONSTRAINT `orderitem_order_id_fk_order_id` FOREIGN KEY (`order_id`) REFERENCES `order` (`id`),
  CONSTRAINT `orderitem_to_address_id_fk_address_id` FOREIGN KEY (`to_address_id`) REFERENCES `address` (`id`),
  CONSTRAINT `orderitem_chk_1` CHECK ((`quantity` >= 0)),
  CONSTRAINT `orderitem_chk_2` CHECK ((`price` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orderitem`
--

LOCK TABLES `orderitem` WRITE;
/*!40000 ALTER TABLE `orderitem` DISABLE KEYS */;
INSERT INTO `orderitem` VALUES ('DELIVERED',1,1,1,1000,1,6),('DELIVERED',1,2,1,1200,1,6),('DELIVERED',1,3,2,1300,2,7),('DELIVERED',1,4,2,1800,2,7),('DELIVERED',1,5,3,1500,3,8),('DELIVERED',1,6,3,400,3,8),('REFUNDED',1,7,4,200,4,9),('REFUNDED',1,8,4,800,4,9),('REFUNDED',1,9,5,1000,5,10),('REFUNDED',1,10,5,2000,5,10),('DELIVERED',1,11,6,500,6,10),('DELIVERED',1,12,6,1500,6,10),('ORDER_PLACED',1,13,7,200,7,1),('ORDER_PLACED',2,14,7,500,7,1),('SHIPPED',1,15,8,1000,8,1),('SHIPPED',3,16,8,1500,8,1),('ORDER_PLACED',1,17,9,2000,9,3),('ORDER_PLACED',1,18,9,500,9,3),('SHIPPED',2,19,10,1500,10,4),('SHIPPED',1,20,10,800,10,4);
/*!40000 ALTER TABLE `orderitem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payment`
--

DROP TABLE IF EXISTS `payment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `payment` (
  `payment_type` enum('credit','debit','upi','bank transfer') DEFAULT NULL,
  `payment_uid` varchar(50) NOT NULL,
  `payment_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`payment_uid`),
  CONSTRAINT `payment_ibfk_1` FOREIGN KEY (`payment_uid`) REFERENCES `order` (`payment_uid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payment`
--

LOCK TABLES `payment` WRITE;
/*!40000 ALTER TABLE `payment` DISABLE KEYS */;
INSERT INTO `payment` VALUES ('debit','10wefew','2023-04-17 10:26:42'),('credit','12efew3','2023-04-17 10:26:42'),('debit','2324324','2023-04-17 10:26:42'),('upi','32323','2023-04-17 10:26:42'),('bank transfer','4234123','2023-04-17 10:26:42'),('credit','5123123','2023-04-17 10:26:42'),('debit','621132','2023-04-17 10:26:42'),('upi','7ewfwef','2023-04-17 10:26:42'),('bank transfer','8324324fw','2023-04-17 10:26:42'),('credit','944ewd','2023-04-17 10:26:42');
/*!40000 ALTER TABLE `payment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `review`
--

DROP TABLE IF EXISTS `review`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `review` (
  `rating` int unsigned NOT NULL,
  `message` longtext NOT NULL,
  `order_id` bigint NOT NULL,
  `item_id` bigint NOT NULL,
  `title` varchar(50) NOT NULL,
  `image` varchar(150) DEFAULT NULL,
  UNIQUE KEY `item_id_order_id_unique` (`item_id`,`order_id`),
  KEY `review_order_id_fk_order_id` (`order_id`),
  CONSTRAINT `review_item_id_fk_item_id` FOREIGN KEY (`item_id`) REFERENCES `item` (`id`),
  CONSTRAINT `review_order_id_fk_order_id` FOREIGN KEY (`order_id`) REFERENCES `order` (`id`),
  CONSTRAINT `review_chk_1` CHECK ((`rating` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `review`
--

LOCK TABLES `review` WRITE;
/*!40000 ALTER TABLE `review` DISABLE KEYS */;
INSERT INTO `review` VALUES (5,'I\'m very impressed with the product quality and the shipping was incredibly fast! I would highly recommend this seller to anyone looking for quality products and excellent service.',1,1,'Excellent product quality and fast shipping',NULL),(5,'I had a great experience with the customer service team, who were very helpful and made the returns process easy and hassle-free. The item itself was also of great quality and I couldn\'t be happier with my purchase.',1,2,'Great customer service and easy returns',NULL),(5,'The item was exactly as described and I\'m very satisfied with my purchase. The quality is great and it was delivered in a timely manner.',2,3,'Item as described, very satisfied',NULL),(1,'The shipping was extremely slow and it wasn\'t worth the wait. I would caution buyers to be prepared for a long wait time if they decide to purchase from this seller.',2,4,'Extremely slow shipping, not worth the wait',NULL),(5,'I was impressed with how well-packaged the item was and how quickly it arrived. The seller clearly takes care in ensuring their products are delivered in top condition.',3,5,'Well-packaged and quick delivery',NULL),(1,'I was extremely disappointed with the item I received as it was not as advertised. The seller\'s description was misleading and I would caution other buyers to be wary before making a purchase.',3,6,'Misleading advertisement, not as expected',NULL),(3,'While the product itself was decent, I was disappointed that the shipping took longer than expected. If you\'re not in a hurry to receive your purchase, this seller might still be a good option.',4,7,'Decent product quality, slow shipping',NULL),(3,'The item arrived as described, but unfortunately the packaging was damaged during transit. It\'s not a deal-breaker, but it was still disappointing.',4,8,'Item as described, damaged packaging',NULL),(3,'The product quality was just average and didn\'t meet my expectations. I would recommend looking elsewhere if you\'re looking for a higher quality item.',5,9,'Average product quality, not as expected',NULL);
/*!40000 ALTER TABLE `review` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `seller`
--

DROP TABLE IF EXISTS `seller`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `seller` (
  `user_id` bigint NOT NULL,
  `total_sales` int unsigned DEFAULT '0',
  `address_id` int DEFAULT NULL,
  `store_name` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  KEY `seller_address_id_fk_address_id` (`address_id`),
  CONSTRAINT `seller_address_id_fk_address_id` FOREIGN KEY (`address_id`) REFERENCES `address` (`id`),
  CONSTRAINT `seller_user_id_fk_user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `seller`
--

LOCK TABLES `seller` WRITE;
/*!40000 ALTER TABLE `seller` DISABLE KEYS */;
INSERT INTO `seller` VALUES (12,0,6,'store1'),(16,0,7,'storethis'),(17,0,8,'that store'),(18,0,9,'best store'),(19,0,10,'another great store'),(20,0,1,'worlds\' best store');
/*!40000 ALTER TABLE `seller` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `email` varchar(254) NOT NULL,
  `mobile` varchar(10) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `age` int unsigned NOT NULL,
  `sex` varchar(1) DEFAULT NULL,
  `date_joined` datetime(6) NOT NULL,
  `card_number` varchar(25) DEFAULT NULL,
  `bank_name` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `mobile` (`mobile`),
  CONSTRAINT `user_chk_1` CHECK ((`age` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (12,'!35a8lIhPbMTZTCDICFstVUISwacueHn8TEtimSY9','user0@test.com','9800989800','','',0,NULL,'2023-04-11 14:34:36.895416',NULL,NULL),(16,'!35a8lIhPbMTZTCDICFstVUISwacueHn8TEtimSY9','user1@test.com','9898989801','','',0,NULL,'2023-04-11 14:34:36.895416',NULL,NULL),(17,'!35a8lIhPbMTZTCDICFstVUISwacueHn8TEtimSY9','user2@test.com','9898989802','','',0,NULL,'2023-04-11 14:34:36.895416',NULL,NULL),(18,'!35a8lIhPbMTZTCDICFstVUISwacueHn8TEtimSY9','user3@test.com','9898989803','','',0,NULL,'2023-04-11 14:34:36.895416',NULL,NULL),(19,'!35a8lIhPbMTZTCDICFstVUISwacueHn8TEtimSY9','user4@test.com','9898989804','','',0,NULL,'2023-04-11 14:34:36.895416',NULL,NULL),(20,'!35a8lIhPbMTZTCDICFstVUISwacueHn8TEtimSY9','user5@test.com','9898989805','','',0,NULL,'2023-04-11 14:34:36.895416',NULL,NULL);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-04-17 15:57:47
