-- Initialize database
--
DROP DATABASE IF EXISTS `e-commerce`;
CREATE DATABASE `e-commerce`;
USE `e-commerce`;

--
-- Create table for entity User
--

CREATE TABLE `user`
 (
	  `id`          BIGINT auto_increment PRIMARY KEY,
	  `password`    VARCHAR(128) NOT NULL,
	  `email`       VARCHAR(254) NOT NULL UNIQUE,
	  `mobile`      VARCHAR(10) NOT NULL UNIQUE,
	  `first_name`  VARCHAR(150) NOT NULL,
	  `last_name`   VARCHAR(150) NOT NULL,
	  `age`         INTEGER UNSIGNED NOT NULL check (`age` >= 0),
	  `sex`         ENUM("M","F","O") NULL,
      -- sex: M: Male, F: Female, O: Other
	  `date_joined` datetime(6) NOT NULL,
	  `card_number` VARCHAR(25) NULL,
	  bank_name     VARCHAR(50) NULL
 );

--
-- create table for ADDRESS ( address and pincode)
--
    
CREATE TABLE `address`
(
	  `id`            INTEGER auto_increment PRIMARY KEY,
	  `address_line1` VARCHAR(100) NOT NULL,
	  `address_line2` VARCHAR(100) NULL,
	  `city`          VARCHAR(50) NOT NULL,
	  `country`       VARCHAR(50) NOT NULL
);


CREATE TABLE `address_pincode`
(
	  `id`      INTEGER UNIQUE,
	  `pincode` VARCHAR(6) NOT NULL,
	  PRIMARY KEY (id),
	  FOREIGN KEY (id) REFERENCES address(id)
);

--
-- Create table for entity Customer
--

CREATE TABLE `customer`
(
	  `user_id`         BIGINT PRIMARY KEY,
	  `total_purchases` INTEGER UNSIGNED NULL DEFAULT 0,
	  `address_id`      INTEGER NULL,
	  CONSTRAINT `customer_user_id_fk_user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
	  CONSTRAINT `customer_address_id_fk_address_id` FOREIGN KEY (`address_id`) REFERENCES `address`(`id`)
);

--
-- Create table for entity Seller
--

CREATE TABLE `seller`
(
	  `user_id`     BIGINT PRIMARY KEY,
	  `total_sales` INTEGER UNSIGNED NULL DEFAULT 0,
	  `address_id`  INTEGER NULL,
	  store_name    VARCHAR(50) NULL,
	  CONSTRAINT `seller_user_id_fk_user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
	  CONSTRAINT `seller_address_id_fk_address_id` FOREIGN KEY (`address_id`) REFERENCES `address`(`id`)
);

--
-- Create table for entity Category
--

CREATE TABLE `category`
(
	  `name`  VARCHAR(50) UNIQUE,
	  `image` VARCHAR(150) DEFAULT "default_category_image.jpg",
	  `id`    INTEGER PRIMARY KEY
);

--
-- Create table for entity Item
--

CREATE TABLE `item`
(
	  `id`    BIGINT auto_increment PRIMARY KEY,
	  `name`  VARCHAR(50) NOT NULL,
	  `price` INTEGER UNSIGNED NOT NULL check (`price` >= 0),
	  `description` LONGTEXT NULL,
	  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
	  `total_sale` INTEGER DEFAULT 0,
	  `stock`      INT DEFAULT 0,
	  `mrp`        INTEGER UNSIGNED NOT NULL CHECK (`mrp` >= 0),
	  -- Add field seller to item
	  `seller_id` BIGINT NOT NULL ,
	  CONSTRAINT `item_seller_id_fk_seller_user_id` FOREIGN KEY (`seller_id`) REFERENCES `seller`(`user_id`),
	  -- Alter unique_together for item (1 constraint)
	  CONSTRAINT `item_name_seller_id_unique` UNIQUE (`name`, `seller_id`),
	  -- Add field category to item
	  `category_id` INTEGER NOT NULL ,
	  CONSTRAINT `item_category_id_fk_category_id` FOREIGN KEY (`category_id`) REFERENCES `category`(`id`)
);

--
-- Create table for coupon code
--
CREATE TABLE `coupon_code`
 (
	  `code` VARCHAR(20) PRIMARY KEY,
	  `discount` FLOAT UNSIGNED NOT NULL check (`discount` >= 0 AND `discount` <= 1),
	  `valid_from`  datetime NOT NULL,
	  `valid_to`    datetime NOT NULL,
	  `usage_limit` INTEGER UNSIGNED NULL,
	  `used_count`  INTEGER UNSIGNED NOT NULL DEFAULT 0
 );

--
-- Create table for entity Order
--

CREATE TABLE `order`
 (
	  `id`          BIGINT auto_increment PRIMARY KEY,
	  `order_time`  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	  `amount`      INTEGER NOT NULL,
	  `payment_uid` VARCHAR(50) UNIQUE NOT NULL,
	  -- Add address to entity order (for delivery address)
	  address_id INT NOT NULL,
	  CONSTRAINT order_address_id_fk_address_id FOREIGN KEY (address_id) REFERENCES address(id),
	  -- Add customer to entity order
	  `customer_id` BIGINT NOT NULL ,
	  CONSTRAINT `order_customer_id_fk_customer_user_id` FOREIGN KEY (`customer_id`) REFERENCES `customer`(`user_id`),
	  `coupon_code_name` VARCHAR(20) NULL,
	  CONSTRAINT `order_coupon_code_name_fk_coupon_code` FOREIGN KEY (`coupon_code_name`) REFERENCES `coupon_code`(`code`)
 );
             
--
-- Create table for entity ItemImage
--

CREATE TABLE `itemimage`
(
	  `id`    INTEGER auto_increment PRIMARY KEY,
	  `image` VARCHAR(150) NOT NULL,
	  -- Add field item to itemimage
	  `item_id` BIGINT NOT NULL ,
	  CONSTRAINT `itemimage_item_id_fk_item_id` FOREIGN KEY (`item_id`) REFERENCES `item`(`id`)
);

--
-- Create table for entity OrderItem
--

CREATE TABLE `orderitem`
(
	  `status` ENUM( 'REFUNDED', 'ORDER_PLACED', 'SHIPPED', 'DELIVERED', 'CANCELLED') NOT NULL,
	  `quantity` INTEGER UNSIGNED NOT NULL check (`quantity` >= 0),
	  `price`    INTEGER NOT NULL CHECK (`price` >= 0),
	  -- item
	  `item_id` BIGINT NOT NULL,
	  CONSTRAINT `orderitem_item_id_fk_item_id` FOREIGN KEY (`item_id`) REFERENCES `item` (`id`),
	  -- order
	  `order_id` BIGINT NOT NULL,
	  CONSTRAINT `orderitem_order_id_fk_order_id` FOREIGN KEY (`order_id`) REFERENCES `order` (`id`),
	  -- address (represents store)
	  `from_address_id` INTEGER NOT NULL,
	  CONSTRAINT `orderitem_from_address_id_fk_address_id` FOREIGN KEY (`from_address_id`) REFERENCES `address`(`id`)
);

--
-- Create table for entity Review
--
CREATE TABLE `review`
(
	  `rating` INTEGER UNSIGNED NOT NULL check (`rating` >= 0),
	  `message` LONGTEXT NOT NULL,
	  title      VARCHAR(50) NOT NULL,
	  image      VARCHAR(150) DEFAULT "default_review_image.jpg",
	  `order_id` BIGINT NOT NULL,
	  CONSTRAINT `review_order_id_fk_order_id` FOREIGN KEY (`order_id`) REFERENCES `order` (`id`),
	  `item_id` BIGINT NOT NULL,
	  CONSTRAINT `review_item_id_fk_item_id` FOREIGN KEY (`item_id`) REFERENCES `item` (`id`),
	  -- unique together constraint
	  CONSTRAINT `item_id_order_id_unique` UNIQUE (`item_id`, `order_id`)
);
			
delimiter //
CREATE TRIGGER `check_orderitem_of_review_trigger` 
  BEFORE INSERT
  ON `review` 
  FOR EACH row 
  begin 
  DECLARE order_item_count INT;
  SELECT Count(*) INTO   order_item_count
  FROM   `orderitem`
  WHERE  `order_id` = new.order_id AND `item_id` = new.item_id;
  IF order_item_count = 0 THEN
    signal SQLSTATE '45000'
    SET message_text = 'Invalid reviewer.';
END IF;
END //
delimiter ;

-- if you want to CHECK THE INVALID REVIEW TRIGGER, here is an invalid case. test it after the reviews insert statements :
-- INSERT INTO `review` (`rating`, `message`, `order_id`, `item_id`,`title`) VALUES
-- (1, 'I was extremely disappointed with the item I received as it was not as advertised.', 1, 12, 'Misleading advertisement');


--
-- Create table for relation "Keep in Cart"
--

CREATE TABLE `cart`
(
	  `customer_id` BIGINT NOT NULL,
	  CONSTRAINT `cart_customer_id_fk_customer_user_id` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`user_id`),
	  `item_id`BIGINT NOT NULL,
	  CONSTRAINT `cart_item_id_fk_item_id` FOREIGN KEY (`item_id`) REFERENCES `item` (`id`),
	  `quantity` INTEGER NOT NULL check (`quantity` >= 0),
	  -- unique
	  CONSTRAINT `cart_items_cart_id_item_id_unique` UNIQUE (`customer_id`, `item_id`)
);

--
-- Create table for entity "Payment"
--

CREATE TABLE payment
(
	  payment_type ENUM('credit', 'debit', 'upi', 'bank transfer'),
	  payment_uid VARCHAR(50) PRIMARY KEY,
	  payment_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	  FOREIGN KEY (payment_uid) REFERENCES `order`(payment_uid)
);

--- - - - - - — - - - - - - —------ - - —------ - - —--------- - - - –        - —-------- —-----       —- —--      



-- Dummy data for relation user

INSERT INTO `user` (`id`,  `email`,   `password`, `mobile`, `first_name`, `last_name`, `age`, `sex`, `date_joined`) VALUES
(12, 'user0@test.com',   '!35a8lIhPbMTZTCDICFstVUISwacueHn8TEtimSY9', '9800989800', '', '', 0, NULL, '2023-04-11 14:34:36.895416'),
(16,  'user1@test.com',   '!35a8lIhPbMTZTCDICFstVUISwacueHn8TEtimSY9', '9898989801', '', '', 0, NULL, '2023-04-11 14:34:36.895416'),
(17,   'user2@test.com',  '!35a8lIhPbMTZTCDICFstVUISwacueHn8TEtimSY9', '9898989802', '', '', 0, NULL, '2023-04-11 14:34:36.895416'),
(18,   'user3@test.com',  '!35a8lIhPbMTZTCDICFstVUISwacueHn8TEtimSY9', '9898989803', '', '', 0, NULL, '2023-04-11 14:34:36.895416'),
(19,   'user4@test.com',   '!35a8lIhPbMTZTCDICFstVUISwacueHn8TEtimSY9', '9898989804', '', '', 0, NULL, '2023-04-11 14:34:36.895416'),
(20,   'user5@test.com',  '!35a8lIhPbMTZTCDICFstVUISwacueHn8TEtimSY9', '9898989805', '', '', 0, NULL, '2023-04-11 14:34:36.895416')
;

-- Dummy data for entity Address

INSERT INTO `address` (`address_line1`, `address_line2`, `city`, `country`)
VALUES
("Address Line 1A", "Address Line 2A", "CityA", "CountryA"),
("Address Line 1B", "Address Line 2B", "CityB", "CountryB"),
("Address Line 1C", "Address Line 2C", "CityC", "CountryC"),
("Address Line 1D", "Address Line 2D", "CityD", "CountryD"),
("Address Line 1E", "Address Line 2E", "CityE", "CountryE"),
("Address Line 1F", "Address Line 2F", "CityF", "CountryF"),
("Address Line 1G", "Address Line 2G", "CityG", "CountryG"),
("Address Line 1H", "Address Line 2H", "CityH", "CountryH"),
("Address Line 1I", "Address Line 2I", "CityI", "CountryI"),
("Address Line 1J", "Address Line 2J", "CityJ", "CountryJ");

INSERT INTO `address_pincode` (`id`, `pincode`)
VALUES
(1, "123456"),
(2, "234567"),
(3, "345678"),
(4, "456789"),
(5, "567890"),
(6, "678901"),
(7, "789012"),
(8, "890123"),
(9, "901234"),
(10, "012345");


-- Dummy data for relation customer

INSERT INTO `customer` (`user_id`, `address_id`)
VALUES
(16, 1),
(17, 2),
(18,  3),
(19, 4),
(20, 5);

-- Dummy data for relation seller

INSERT INTO `seller` (`user_id`, `address_id`, store_name)
VALUES
(12,  6, 'store1'),
(16,  7, 'storethis'),
(17,  8 ,'that store'),
(18,  9, 'best store'),
(19,  10, 'another great store'),
(20,  1, 'worlds\' best store');


-- Dummy data for relation category

INSERT INTO `category` (`id`, `name`, `image`) VALUES
(1, 'ELECTRONICS', 'category_images/electronics.jpg'),
(2, 'CLOTHING', 'category_images/clothing.jpg'),
(3, 'BABY', 'category_images/baby.jpg'),
(4, 'SPORTS', 'category_images/sports.jpg'),
(5, 'HOME', 'category_images/home.jpg'),
(6, 'TOYS', 'category_images/toys.jpg'),
(7, 'BEAUTY', 'category_images/beauty.jpg'),
(8, 'GROCERY', 'category_images/grocery.jpg'),
(9, 'AUTOMOTIVE', 'category_images/automotive.jpg'),
(10, 'BOOKS', 'category_images/books.jpg'),
(11, 'HEALTH', 'category_images/health.jpg'),
(12, 'SHOES', 'category_images/shoes.jpg'),
(13, 'JEWELRY', 'category_images/jewelry.jpg'),
(14, 'TOOLS', 'category_images/tools.jpg'),
(15, 'GARDEN', 'category_images/garden.jpg');

-- Dummy data for relation item

INSERT INTO `item` (`id`, `name`, `price`, `description`, `category_id`,`seller_id`, `total_sale`,`mrp`) VALUES
(1, 'iPhone 11', 1000, 'iPhone 11 is a smartphone designed, developed, and marketed by Apple Inc. It is the twelfth generation of the iPhone. It was announced on September 10, 2019, alongside the higher-end iPhone 11 Pro and iPhone 11 Pro Max, at the Steve Jobs Theater in the Apple Park campus. The iPhone 11 features a 6.1-inch Liquid Retina IPS LCD display with support for Dolby Vision and HDR10, an Apple-designed A13 Bionic chipset, a dual-camera system on the back consisting of a 12-megapixel wide-angle camera and a 12-megapixel ultra-wide-angle camera, a 12-megapixel front-facing camera, and a 3,110 mAh battery. It is available in six colors: purple, green, yellow, black, white, and PRODUCT(RED).', 1,16, 22,10000),
(2, 'iPhone 11 Pro', 1200, 'iPhone 11 Pro is a smartphone designed, developed, and marketed by Apple Inc. It is the thirteenth generation of the iPhone. It was announced on September 10, 2019, alongside the higher-end iPhone 11 Pro Max and iPhone 11, at the Steve Jobs Theater in the Apple Park campus. The iPhone 11 Pro features a 5.8-inch Super Retina XDR OLED display with support for Dolby Vision and HDR10, an Apple-designed A13 Bionic chipset, a triple-camera system on the back consisting of a 12-megapixel wide-angle camera, a 12-megapixel ultra-wide-angle camera, and a 12-megapixel telephoto camera, a 12-megapixel front-facing camera, and a 3,190 mAh battery. It is available in four colors: midnight green, space gray, silver, and gold.', 1,16, 44,10000),
(3, 'iPhone 11 Pro Max', 1300, 'iPhone 11 Pro Max is a smartphone designed, developed, and marketed by Apple Inc. It is the thirteenth generation of the iPhone. It was announced on September 10, 2019, alongside the higher-end iPhone 11 Pro and iPhone 11, at the Steve Jobs Theater in the Apple Park campus. The iPhone 11 Pro Max features a 6.5-inch Super Retina XDR OLED display with support for Dolby Vision and HDR10, an Apple-designed A13 Bionic chipset, a triple-camera system on the back consisting of a 12-megapixel wide-angle camera, a 12-megapixel ultra-wide-angle camera, and a 12-megapixel telephoto camera, a 12-megapixel front-facing camera, and a 3,500 mAh battery. It is available in four colors: midnight green, space gray, silver, and gold.', 1,16, 55,10000),
(4, 'MacBook Pro', 1800, 'MacBook Pro is a line of Macintosh portable computers introduced in January 2006 by Apple Inc. It is the high-end model of the MacBook family and is currently available in 13- and 16-inch screen sizes. A 15-inch version was available between April 2006 and June 2012. The first generation MacBook Pro was externally similar to the PowerBook G4 it replaced, but inside the case was completely redesigned, incorporating an Intel processor, a glass trackpad, and LED-backlit display. The MacBook Pro is the successor to the PowerBook G4 and is Apple\'s current high-end consumer notebook.', 1,16, 6,10000),
(5, 'MacBook Air', 1500, 'MacBook Air is a line of Macintosh portable computers developed and manufactured by Apple Inc. It consists of a full-size keyboard, a machined aluminum case, and a thin light structure. The Air is available in 13-inch and 11-inch screen sizes. The 13-inch model was available in silver or space gray, while the 11-inch model was available in white or silver. The 13-inch MacBook Air was discontinued on October 26, 2018, and the 11-inch model was discontinued on July 15, 2017. The MacBook Air is the successor to the MacBook and is currently Apple\'s most affordable notebook computer.', 1,16, 7,10000),
(6, 'iPad', 400, 'iPad is a line of tablet computers designed, developed and marketed by Apple Inc., which run the iOS mobile operating system. The first iPad was released on April 3, 2010; the most recent iPad models are the 10.2-inch iPad (8th generation) released on September 18, 2020, and the 11-inch iPad Pro (2nd generation) released on November 7, 2017. The user interface is built around the device\'s multi-touch screen, including a virtual keyboard. The iPad includes built-in Wi-Fi and cellular connectivity on select models. As of January 2019, there have been over 500 million iPads sold.', 1,16, 88,10000),
(7, 'AirPods', 200, 'AirPods are wireless Bluetooth earbuds created by Apple Inc. They were introduced on September 7, 2016, as a wireless alternative to the EarPods that come bundled with iPhones. The AirPods are designed to be used with Apple\'s W1 chip, which is also used in the Apple Watch and Beats headphones. The AirPods are compatible with all Apple devices that support Bluetooth 4.2 and later, including the iPhone, iPad, Apple Watch, and Mac. The AirPods are also compatible with Android devices that support Bluetooth 5.0 and later.', 1,16, 19,10000),
(8, 'T-Shirt', 800, 'A T-shirt is a style of unisex fabric shirt named after the T shape of its body and sleeves. Traditionally it has short sleeves and a round neckline, known as a crew neck, which lacks a collar. T-shirts are generally made of a light, inexpensive fabric and are easy to clean. T-shirts are also a medium for expression and advertising, with any imaginable combination of words, art and photographs on display.', 2,16, 10,10000),
(9, 'Shoes', 1000, 'A shoe is an item of footwear intended to protect and comfort the human foot while the wearer is doing various activities. Shoes are also used as an item of decoration and fashion. The design of shoes has varied enormously through time and from culture to culture, with appearance originally being tied to function. Additionally, fashion has often dictated many design elements, such as whether shoes have very high heels or flat ones. Contemporary footwear in the 2010s varies widely in style, complexity and cost. Basic sandals may consist of only a thin sole and simple strap and be sold for a low cost. High fashion shoes made by famous designers may be made of expensive materials, use complex construction and sell for hundreds or even thousands of dollars a pair.', 2,16, 11,10000),
(10, 'Watch', 2000, 'A watch is a small timepiece intended to be carried or worn by a person. It is designed to keep working despite the motions caused by the person\'s activities. A wristwatch is designed to be worn around the wrist, attached by a watch strap or other type of bracelet. A pocket watch is designed for a person to carry in a pocket. Watches progressed in the 17th century from spring-powered clocks, which appeared as early as the 14th century. During most of its history the watch was a mechanical device, driven by clockwork, powered by winding a mainspring, and keeping time with an oscillating balance wheel. These are called mechanical watches. In the 1960s the electronic quartz watch was invented, which was powered by a battery and kept time with a vibrating quartz crystal.', 2,16, 12,10000),
(11, 'Sunglasses', 500, 'Sunglasses or sun glasses are a form of protective eyewear designed primarily to prevent bright sunlight and high-energy visible light from damaging or discomforting the eyes. They can sometimes also function as a visual aid, as variously termed spectacles or glasses exist, featuring lenses that are colored, polarized or darkened. In the early 20th century, they were also known as sun cheaters. In the 20th century, they were known as shades. In the 21st century, a generic form of the term \'sunglasses\' is used.', 2,16, 77,2000),
(12, 'Headphones', 1500, 'Headphones or earphones are a pair of small loudspeaker drivers worn on or around the head over a user\'s ears. They are electroacoustic transducers, which convert an electrical signal to a corresponding sound. Headphones are also known as ear speakers, earphones, or, colloquially, cans. Headphones are used by a wide range of people for a wide variety of reasons. They are used by audiophiles for critical listening and personal audio enjoyment, by gamers for immersive gaming, by musicians for practice and live performances, by moviegoers for private listening, and by air travellers for audio and video entertainment.', 2,16, 33,4000),
(13, 'Backpack', 2000, 'A backpack is, in its simplest form, a cloth sack carried on one\'s back and secured with two straps that go over the shoulders, but there can be variations. The backpack may have one or two shoulder straps, each of which can be padded or unpadded, and can be adjustable in length. The backpack may also have a handle at the top, a waist belt, and compression straps that tighten the pack to reduce its volume. Backpacks are often made of nylon, canvas, leather, or vinyl.', 2,17, 14,3000),
(14, 'Baby Powder', 500, 'Baby powder is a talcum powder used for babies. It is used to keep the skin dry and prevent rashes. It is also used to keep the diaper area dry. It is used to keep the skin soft and smooth. It is used to keep the skin dry and prevent rashes. It is also used to keep the diaper area dry. It is used to keep the skin soft and smooth.', 3,17, 5,10000),
(15, 'Baby Soap', 1000, 'Baby soap is a soap used for babies. It is used to keep the skin soft and smooth. It is used to keep the skin dry and prevent rashes. It is also used to keep the diaper area dry. It is used to keep the skin soft and smooth. It is used to keep the skin dry and prevent rashes. It is also used to keep the diaper area dry.', 3,17, 9,10000),
(16, 'Baby Oil', 1500, 'Baby oil is a mineral oil used for babies. It is used to keep the skin soft and smooth. It is used to keep the skin dry and prevent rashes. It is also used to keep the diaper area dry. It is used to keep the skin soft and smooth. It is used to keep the skin dry and prevent rashes. It is also used to keep the diaper area dry.', 3,17, 4,10000),
(17, 'Baby Shampoo', 2000, 'Baby shampoo is a shampoo used for babies. It is used to keep the skin soft and smooth. It is used to keep the skin dry and prevent rashes.', 3,17, 5,10000),
(18, 'Baby Lotion', 2500, 'Baby lotion is a lotion used for babies. It is used to keep the skin soft and smooth. It is used to keep the skin dry and prevent rashes. It is also used to keep the diaper area dry. It is used to keep the skin soft and smooth. It is used to keep the skin dry and prevent rashes. It is also used to keep the diaper area moist.', 3,17, 7,10000),
(19, 'Baby Wipes', 3000, 'Baby wipes are a type of wet wipe used for babies. It is used to keep the skin soft and smooth. It is used to keep the skin dry and prevent rashes. It is also used to keep the diaper area dry. It is used to keep the skin soft and smooth. It is used to keep the skin dry and prevent rashes. It is also used to keep the diaper area moist.', 3,17, 6,6000),
(20, 'Rare Necklace', 5000, 'A rare necklace is a necklace used for fashion by celebrities.', 13,17, 8,5000),
(21, 'Rare Ring', 5000, 'A rare ring is a ring used for babies. It is used for fashion by celebrities.', 13,18, 8,5000),
(22, 'Rare Bracelet', 5000, 'A rare bracelet is a bracelet use for fashion by celebrities.', 13,18, 11,5000),
(23, 'Rare Earrings', 5000, 'A rare earrings is used for fashion by celebrities.', 13,18, 11,5000),
(24, 'Rare Watch', 5000, 'A rare watch is a watch used for fashion by celebrities.', 13,18, 11,5000),
(25, 'Rare Sunglasses', 5000, 'A rare sunglasses is a sunglasses used for fashion by celebrities.', 13,18, 11,5000),
(26, 'Rare Belt', 5000, 'A rare belt is a belt used for babies. It is used to keep the skin soft and smooth. It is used to keep the skin dry and prevent rashes. It is also used to keep the diaper area dry. It is used to keep the skin soft and smooth. It is used to keep the skin dry and prevent rashes. It is also used to keep the diaper area dry.', 13,19, 11,6000),
(27, 'Rose seeds', 500, 'Rose seeds are for growing new lily plants. The pleasant aroma in surroundings.', 15,19, 17,700),
(28, 'Jasmine seeds', 350, 'Jasmine seeds are used for growing new lily plants. The pleasant aroma in surroundings.', 15,19, 11,700),
(29, 'Lily seeds', 250, 'Lily seeds are seeds used for growing new lily plants. The pleasant aroma in surroundings.', 15,20, 20,700);

-- dummy data for itemimage

Insert into itemimage (image, item_id) values 

("item_images/iphone11.jpg",1),
("item_images/iphone.jpg",1),
("item_images/iphone11pro.jpg",2),
("item_images/iphone11.jpg",2),
("item_images/iphone11promax.jpg",3),
("item_images/iphone11.jpg",3),
("item_images/macbookpro.jpg",4),
("item_images/macbookair.jpg",5),
("item_images/ipad.jpg",6),
("item_images/airpod.jpg",7),
("item_images/tshirt.jpg",8),
("item_images/shoes.jpg",9),
("item_images/watch.jpeg",10),
("item_images/sunglasses.jpg",11),
("item_images/headphones.jpg",12),
("item_images/backpack.jpg",13),
("item_images/babypowder.jpg",14),
("item_images/babysoap.jpg",15),
("item_images/babyoil.jpg",16),
("item_images/babyshampoo.jpg",17),
("item_images/babylotion.jpg",18),
("item_images/babywipes.jpg",19),
("item_images/necklace.jpg",20),
("item_images/ring.jpg",21),
("item_images/bracelet.jpg",22),
("item_images/earrings.jpg",23),
("item_images/watch.jpeg",24),
("item_images/sunglasses.jpg",25),
("item_images/belt.jpg",26),
("item_images/roseseeds.jpg",27),
("item_images/jasmineseeds.jpg",28),
("item_images/lilyseeds.jpg",29);


-- Dummy data for relation order

INSERT INTO `order` (`order_time`, `customer_id`, `amount`, `payment_uid`, address_id)
VALUES
(NOW() - INTERVAL 1 DAY, 16, 2200, "12efew3",1),
(NOW() - INTERVAL 2 DAY, 17, 3100, "2324324",1),
(NOW() - INTERVAL 3 DAY, 18, 1900, "32323",1),
(NOW() - INTERVAL 4 DAY, 19, 1000, "4234123",1),
(NOW() - INTERVAL 5 DAY, 20, 3000, "5123123",1),
(NOW() - INTERVAL 6 DAY, 16, 2000, "621132",1),
(NOW() - INTERVAL 7 DAY, 17, 700, "7ewfwef",1),
(NOW() - INTERVAL 8 DAY, 18, 6000, "8324324fw",1),
(NOW() - INTERVAL 9 DAY, 19, 2500, "944ewd",1),
(NOW() - INTERVAL 10 DAY, 20,4100, "10wefew",1);

-- dummy data for payment

INSERT INTO payment (payment_type, payment_uid)
VALUES 
('credit', '12efew3'),
('debit', '2324324'),
('upi', '32323'),
('bank transfer', '4234123'),
('credit', '5123123'),
('debit', '621132'),
('upi', '7ewfwef'),
('bank transfer', '8324324fw'),
('credit', '944ewd'),
('debit', '10wefew');

-- Dummy data for relation orderitem

INSERT INTO `orderitem` (`order_id`, `item_id`, `quantity`, `price`, `from_address_id`, `status`)
VALUES
(1, 1, 1, 1000, 1, 'DELIVERED'),
(1, 2, 1, 1200, 1, 'DELIVERED'),
(2, 3, 1, 1300, 2, 'DELIVERED'),
(2, 4, 1, 1800, 2, 'DELIVERED'),
(3, 5, 1, 1500, 3, 'DELIVERED'),
(3, 6, 1, 400, 3, 'DELIVERED'),
(4, 7, 1, 200, 4, 'REFUNDED'),
(4, 8, 1, 800, 4, 'REFUNDED'),
(5, 9, 1, 1000, 5, 'REFUNDED'),
(5, 10, 1, 2000, 5, 'REFUNDED'),
(6, 11, 1, 500, 6, 'DELIVERED'),
(6, 12, 1, 1500, 6, 'DELIVERED'),
(7, 13, 1, 200, 7, 'ORDER_PLACED'),
(7, 14, 2, 500, 7, 'ORDER_PLACED'),
(8, 15, 1, 1000, 8, 'SHIPPED'),
(8, 16, 3, 1500, 8, 'SHIPPED'),
(9, 17, 1, 2000, 9, 'ORDER_PLACED'),
(9, 18, 1, 500, 9, 'ORDER_PLACED'),
(10, 19, 2, 1500, 10, 'SHIPPED'),
(10, 20, 1, 800, 10, 'SHIPPED');

-- Dummy data for relation review

INSERT INTO `review` (`rating`, `message`, `order_id`, `item_id`,`title`) VALUES
(5, 'I\'m very impressed with the product quality and the shipping was incredibly fast! I would highly recommend this seller to anyone looking for quality products and excellent service.', 1, 1, 'Excellent product quality and fast shipping'),
(5, 'I had a great experience with the customer service team, who were very helpful and made the returns process easy and hassle-free. The item itself was also of great quality and I couldn\'t be happier with my purchase.', 1, 2, 'Great customer service and easy returns'),
(5, 'The item was exactly as described and I\'m very satisfied with my purchase. The quality is great and it was delivered in a timely manner.', 2, 3, 'Item as described, very satisfied'),
(5, 'I was impressed with how well-packaged the item was and how quickly it arrived. The seller clearly takes care in ensuring their products are delivered in top condition.', 3, 5, 'Well-packaged and quick delivery'),
(3, 'While the product itself was decent, I was disappointed that the shipping took longer than expected. If you\'re not in a hurry to receive your purchase, this seller might still be a good option.', 4, 7, 'Decent product quality, slow shipping'),
(3, 'The item arrived as described, but unfortunately the packaging was damaged during transit. It\'s not a deal-breaker, but it was still disappointing.', 4, 8, 'Item as described, damaged packaging'),
(3, 'The product quality was just average and didn\'t meet my expectations. I would recommend looking elsewhere if you\'re looking for a higher quality item.', 5, 9, 'Average product quality, not as expected'),
(1, 'The shipping was extremely slow and it wasn\'t worth the wait. I would caution buyers to be prepared for a long wait time if they decide to purchase from this seller.', 2, 4, 'Extremely slow shipping, not worth the wait')
;

-- dummy data for cart

INSERT INTO cart (customer_id, item_id, quantity)
VALUES
(18, 6, 3),
(18, 7, 5),
(18, 25, 2),
(19, 5, 9),
(19, 21, 2),
(19, 4, 4),
(19, 3, 1),
(20, 12, 5),
(20, 15, 8),
(20, 6, 1),
(20, 16, 5),
(17, 6, 3);

-- dummy data for coupon code

INSERT INTO `coupon_code` (`code`, `discount`, `valid_from`, `valid_to`, `usage_limit`)
VALUES 
  ('C0DE1', 0.15, '2023-04-16 00:00:00', '2023-09-20 00:00:00', 5),
  ('C0DE2', 0.10, '2023-04-19 00:00:00', '2023-05-19 00:00:00', 10),
  ('C0DE3', 0.20, '2023-04-20 00:00:00', '2023-05-20 00:00:00', 3),
  ('C0DE4', 0.05, '2023-04-21 00:00:00', '2023-05-21 00:00:00', 100000),
  ('C0DE5', 0.25, '2023-04-22 00:00:00', '2023-05-22 00:00:00', 2),
  ('C0DE6', 0.10, '2023-04-23 00:00:00', '2023-05-23 00:00:00', 8),
  ('C0DE7', 0.30, '2023-04-24 00:00:00', '2023-05-24 00:00:00', 1),
  ('C0DE8', 0.10, '2023-04-25 00:00:00', '2023-05-25 00:00:00', 100000),
  ('C0DE9', 0.15, '2023-04-26 00:00:00', '2023-05-26 00:00:00', 4),
  ('C0DE10', 0.20, '2023-04-27 00:00:00', '2023-05-27 00:00:00', 3);



