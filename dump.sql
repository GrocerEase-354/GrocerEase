DROP TABLE IF EXISTS customer_payment_method;
DROP TABLE IF EXISTS store_order;
DROP TABLE IF EXISTS adds;
DROP TABLE IF EXISTS product_in_shopping_cart;
DROP TABLE IF EXISTS shopping_cart;
DROP TABLE IF EXISTS product;
DROP TABLE IF EXISTS category;
DROP TABLE IF EXISTS customer;
DROP TABLE IF EXISTS seller;
DROP TABLE IF EXISTS user;



CREATE TABLE user (
    userid VARCHAR(20), 
    user_password CHAR(100) NOT NULL,
    house_number INT,
    street_name VARCHAR(100),
    postal_code VARCHAR(20),
    province VARCHAR(100),
    city VARCHAR(100),
    email VARCHAR(100),
    PRIMARY KEY (userid)
);

CREATE TABLE customer (
    id VARCHAR(20),
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    PRIMARY KEY (id),
    FOREIGN KEY (id) REFERENCES user(userid)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE seller (
    id VARCHAR(20),
    company_name VARCHAR(100),
    PRIMARY KEY (id),
    FOREIGN KEY (id) REFERENCES user(userid)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE category (
    category_name VARCHAR(100),
    PRIMARY KEY (category_name)
);

CREATE TABLE product (
    productid INT AUTO_INCREMENT,
    stock INT,
    product_description VARCHAR(1000),
    best_before_date DATE NOT NULL,
    product_name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2),
    sellerid VARCHAR(20),
    category_name CHAR(100),
    PRIMARY KEY (productid),
    FOREIGN KEY (sellerid) REFERENCES seller(id)
    ON DELETE SET NULL
    ON UPDATE CASCADE,
    FOREIGN KEY (category_name) REFERENCES category(category_name)
    ON DELETE SET NULL
    ON UPDATE CASCADE
);

CREATE TABLE store_order (
    customerid VARCHAR(20),
    orderid INT,
    cost DECIMAL(10, 2),
    order_time DATE,
    payment_method_used VARCHAR(100),
    PRIMARY KEY (customerid, orderid),
    FOREIGN KEY (customerid) REFERENCES customer(id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE shopping_cart (
    customerid VARCHAR(20),
    cartid INT,
    PRIMARY KEY (customerid, cartid),
    FOREIGN KEY (customerid) REFERENCES customer(id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE product_in_shopping_cart (
    productid INT,
    customerid VARCHAR(20),
    cartid INT,
    quantity INT,
    PRIMARY KEY (productid, customerid, cartid),
    FOREIGN KEY (productid) REFERENCES product(productid)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
    FOREIGN KEY (customerid, cartid) REFERENCES shopping_cart(customerid, cartid)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE adds (
    customerid VARCHAR(20),
    productid INT,
    PRIMARY KEY (customerid, productid),
    FOREIGN KEY (customerid) REFERENCES customer(id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
    FOREIGN KEY (productid) REFERENCES product(productid)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE customer_payment_method (
    customerid VARCHAR(20),
    payment_method VARCHAR(100),
    PRIMARY KEY (customerid, payment_method),
    FOREIGN KEY (customerid) REFERENCES customer(id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

DELIMITER $$
# Continue generation id's for orders and carts automatically after an initial value is inserted
CREATE TRIGGER OrderIdGeneration BEFORE INSERT ON store_order
FOR EACH ROW
    IF NEW.orderid IS NULL
    THEN    SET NEW.orderid = (
            SELECT MAX(orderid)
            FROM store_order) + 1;
     END IF;


CREATE TRIGGER CartIdGeneration BEFORE INSERT ON shopping_cart
FOR EACH ROW
    IF NEW.cartid IS NULL
    THEN  SET NEW.cartid = (
          SELECT MAX(cartid)
          FROM shopping_cart) + 1;
    END IF;


CREATE TRIGGER `user_insert_constraints` BEFORE INSERT ON `user`
FOR EACH ROW  
IF LENGTH(NEW.userid) < 1 OR LENGTH(NEW.userid) > 20
THEN
    SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'User ID must be between 1 and 20 characters!';
ELSEIF NEW.house_number < 0
THEN
    SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'House number cannot be less than zero!';
ELSEIF LENGTH(NEW.user_password) < 1 OR LENGTH(NEW.user_password) > 100
THEN
    SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Password must be between 1 and 100 characters!';
ELSEIF NEW.email NOT LIKE '%_@__%.__%'
THEN
    SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Invalid email format!';
END IF;$$

CREATE TRIGGER `user_update_constraints` BEFORE UPDATE ON `user`
FOR EACH ROW IF LENGTH(NEW.userid) < 1 OR LENGTH(NEW.userid) > 20
THEN
    SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'User ID must be between 1 and 20 characters!';
ELSEIF NEW.house_number < 0
THEN
    SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'House number cannot be less than zero!';
ELSEIF LENGTH(NEW.user_password) < 1 OR LENGTH(NEW.userid) > 20
THEN
    SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Password must be between 1 and 100 characters!';
ELSEIF NEW.email NOT LIKE '%_@__%.__%'
THEN
    SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Invalid email format!';
END IF;$$

CREATE TRIGGER `product_insert_constraints` BEFORE INSERT ON `product`
FOR EACH ROW IF NEW.productid < 0
THEN
    SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Product ID cannot be less than zero!';
ELSEIF NEW.stock < 0
THEN
    SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Stock cannot be less than zero!';
ELSEIF NEW.best_before_date <= CURRENT_DATE
THEN
    SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Product is expired!';
ELSEIF NEW.price < 0.0
THEN
    SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Price cannot be less than zero!';
END IF;$$

CREATE TRIGGER `product_update_constraints` BEFORE UPDATE ON `product`
FOR EACH ROW IF NEW.productid < 0
THEN
    SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Product ID cannot be less than zero!';
ELSEIF NEW.stock < 0
THEN
    SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Stock cannot be less than zero!';
ELSEIF NEW.best_before_date <= CURRENT_DATE
THEN
    SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Product is expired!';
ELSEIF NEW.price < 0.0
THEN
    SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Price cannot be less than zero!';
END IF;$$

CREATE TRIGGER `store_order_insert_constraints` BEFORE INSERT ON `store_order`
FOR EACH ROW IF NEW.orderid < 0
THEN
    SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Order ID cannot be less than zero!';
ELSEIF NEW.cost < 0.0
THEN
    SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Cost cannot be less than zero!';
ELSEIF NEW.order_time > CURRENT_DATE
THEN
    SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Date of order is later than today!';
END IF;$$

CREATE TRIGGER `store_order_update_constraints` BEFORE UPDATE ON `store_order`
FOR EACH ROW IF NEW.orderid < 0 
THEN
    SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Order ID cannot be less than zero!';
ELSEIF NEW.cost < 0.0
THEN
    SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Cost cannot be less than zero!';
ELSEIF NEW.order_time > CURRENT_DATE
THEN
    SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Date of order is later than today!';
END IF;$$

CREATE TRIGGER `shopping_cart_update_constraint` BEFORE UPDATE ON `shopping_cart`
FOR EACH ROW IF NEW.cartid < 0 
THEN
    SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Cart ID cannot be less than zero!';
END IF;$$

CREATE TRIGGER `shopping_cart_insert_constraint` BEFORE INSERT ON `shopping_cart`
FOR EACH ROW IF NEW.cartid < 0 
THEN
    SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Cart ID cannot be less than zero!';
END IF;$$

CREATE TRIGGER `product_in_shopping_cart_insert_constraints` BEFORE INSERT ON `product_in_shopping_cart`
FOR EACH ROW IF NEW.quantity < 0 
THEN
    SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Quantity cannot be less than zero!';
END IF;$$

CREATE TRIGGER `product_in_shopping_cart_update_constraints` BEFORE UPDATE ON `product_in_shopping_cart`
FOR EACH ROW IF NEW.quantity < 0 
THEN
    SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Quantity cannot be less than zero!';
END IF;$$
DELIMITER ;

/*Populating the tables with tuples*/

/*User Table Entries*/
INSERT INTO user VALUES
('Y123','1234', 1,'152 Street','V3X123','British Columbia', 'Surrey', 'Yogesh@shaw.ca'),
('A123','5678', 2,'156 Street','V3X456','British Columbia', 'Surrey', 'Andy@shaw.ca'),
('H123','9101', 3,'158 Street','V3X789','British Columbia', 'Surrey', 'Hareet@shaw.ca'),
('J123','1112', 4,'160 Street','V3X101','British Columbia', 'Surrey', 'Bob@shaw.ca'),
('B123','1314', 5,'162 Street','V3X111','British Columbia', 'Surrey', 'Brenden@shaw.ca'),
('Micheal101','0987', 6,'160 Street','V3X112','British Columbia', 'Surrey', 'Micheal@shaw.ca'),
('Jim123','6543', 7,'162 Street','V3X113','British Columbia', 'Surrey', 'Jim@shaw.ca'),
('Dwight456','5432', 8,'164 Street','V3X114','British Columbia', 'Surrey', 'Dwight@shaw.ca'),
('Pam789','4321', 9,'166 Street','V3X115','British Columbia', 'Surrey', 'Pam@shaw.ca'),
('Mose112','7809', 10,'168 Street','V3X116','British Columbia', 'Surrey', 'Mose@shaw.ca');

/*User Table Entries*/
INSERT INTO customer VALUES
('Y123','Yogesh','Sonik'),
('A123','Andy','Lu'),
('H123','Hareet','Dhillon'),
('J123','Bob','HealthyGuy'),
('B123','Brenden','Shaw');

/*Seller Table Entries*/
INSERT INTO seller VALUES
('Jim123','Company 1'),
('Dwight456','Dunder Mifflin'),
('Pam789','Company 2'),
('Micheal101','Company 3'),
('Mose112','Company 4');

/*Category Table Entries*/
INSERT INTO category VALUES
('Fruits'),
('Vegetables'),
('Dairy'),
('Meat'),
('Bread');

/*Product table entries*/
INSERT INTO product VALUES
(101,5,'A fresh bunch of Bananas.','2021-04-24','Banana',2.99,'Jim123','Fruits'),
(102,5,'A dozen fresh Apples.','2021-04-24','Apple',3.99,'Jim123','Fruits'),
(103,5,'A bunch of fresh Grapes.','2021-04-24','Grape',4.99,'Jim123','Fruits'),
(104,5,'A box of fresh Oranges.','2021-04-24','Orange',5.99,'Jim123','Fruits'),
(105,5,'A box of fresh Peaches.','2021-04-24','Peach',6.99,'Jim123','Fruits'),

(106,5,'A dozen fresh Beetroots.','2021-4-25','Beet',7.99,'Dwight456','Vegetables'),
(107,5,'A dozen fresh Carrots.','2021-4-25','Carrot',8.99,'Dwight456','Vegetables'),
(108,5,'A fresh bunch of Lettuce.','2021-4-25','Lettuce',9.99,'Dwight456','Vegetables'),
(109,5,'A fresh Cauliflower.','2021-4-25','Cauliflower',10.99,'Dwight456','Vegetables'),
(110,5,'Half-Dozen fresh Eggplant.','2021-4-25','Eggplant',11.99,'Dwight456','Vegetables'),

(111,5,'A fresh jug of Milk.','2021-4-26','Milk',12.99,'Pam789','Dairy'),
(112,5,'A fresh tub of Yogurt.','2021-4-26','Yogurt',13.99,'Pam789','Dairy'),
(113,5,'A fresh wheel of Cheese.','2021-4-26','Cheese',13.99,'Pam789','Dairy'),
(114,5,'A fresh tub of Ice Cream.','2021-4-26','Ice Cream',15.99,'Pam789','Dairy'),
(115,5,'A fresh jug of Skim Milk.','2021-4-26','Skim Milk',16.99,'Pam789','Dairy'),

(116,5,'A whole Chicken.','2021-4-27','Chicken',17.99,'Micheal101','Meat'),
(117,5,'A whole Turkey.','2021-4-27','Turkey',18.99,'Micheal101','Meat'),
(118,5,'A whole Salmon.','2021-4-27','Salmon',19.99,'Micheal101','Meat'),
(119,5,'A whole Steak.','2021-4-27','Steak',20.99,'Micheal101','Meat'),
(120,5,'A whole Goat.','2021-4-27','Goat',21.99,'Micheal101','Meat'),

(121,5,'A fresh loaf of Bread.','2021-4-28','Bread',2.99,'Mose112','Bread'),
(122,5,'A dozen fresh Cheese Buns.','2021-4-28','Cheese Buns',3.99,'Mose112','Bread'),
(123,5,'A dozen fresh Croissants.','2021-4-28','Croissant',4.99,'Mose112','Bread'),
(124,5,'A fresh loaf of Whole Wheat Bread.','2021-4-28','Whole Wheat Bread',5.99,'Mose112','Bread'),
(125,5,'A fresh loaf of Gluten Free Bread.','2021-4-28','Gluten Free Bread',6.99,'Mose112','Bread');

/*Store_order entries*/
INSERT INTO store_order VALUES
('Y123',100,2.99,'2021-2-20','Credit Card'),
('Y123',101,4.99,'2021-2-25','Credit Card'),
('Y123',102,3.99,'2021-2-26','Credit Card'),
('Y123',103,2.99,'2021-2-27','Credit Card'),

('A123',104,2.99,'2021-2-20','Credit Card'),
('A123',105,3.99,'2021-2-21','Credit Card'),
('A123',106,5.99,'2021-2-28','Credit Card'),

('H123',107,4.99,'2021-2-22','Debit Card'),
('H123',108,2.99,'2021-2-25','Debit Card'),

('J123',109,2.99,'2021-2-23','Debit Card'),
('J123',110,2.99,'2021-2-24','Debit Card'),

('B123',111,5.99,'2021-2-24','Debit Card'),
('B123',112,1.99,'2021-2-25','Debit Card');


/*Shopping_cart entries*/
INSERT INTO shopping_cart VALUES
    ('Y123',200),
    ('A123',201),
    ('H123',202),
    ('J123',203),
    ('B123',204);

/*product_in_shopping_cart*/
INSERT INTO product_in_shopping_cart VALUES
    (101,'Y123',200,2),
    (102,'A123',201,2),
    (103,'H123',202,2),
    (104,'J123',203,2),
    (105,'B123',204,2);

/*Adds entries*/
INSERT INTO adds VALUES
('Y123', 101),
('A123',102),
('H123',103),
('J123',104),
('B123',105);

/*customer_payment_method entries*/
INSERT INTO customer_payment_method VAlUES
('Y123','Credit Card'),
('A123','Credit Card'),
('H123', 'Debit Card'),
('J123','Debit Card'),
('B123', 'Debit Card');
