CREATE TABLE user (
    userid VARCHAR(20),
    user_password CHAR(100),
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
);

CREATE TABLE seller (
    id VARCHAR(20),
    company_name VARCHAR(100),
    PRIMARY KEY (id),
    FOREIGN KEY (id) REFERENCES user(userid)
);

CREATE TABLE category (
    category_name VARCHAR(100),
    PRIMARY KEY (category_name)
);

CREATE TABLE product (
    productid INT,
    stock INT,
    product_description VARCHAR(1000),
    best_before_date DATE,
    product_name VARCHAR(100),
    price DECIMAL(10, 2),
    sellerid VARCHAR(20),
    category_name CHAR(100),
    PRIMARY KEY (productid),
    FOREIGN KEY (sellerid) REFERENCES seller(id),
    FOREIGN KEY (category_name) REFERENCES category(category_name)
);

CREATE TABLE store_order (
    customerid VARCHAR(20),
    orderid INT,
    cost DECIMAL(10, 2),
    order_time DATE,
    payment_method_used VARCHAR(100),
    PRIMARY KEY (customerid, orderid),
    FOREIGN KEY (customerid) REFERENCES customer(id)
);

CREATE TABLE shopping_cart (
    customerid VARCHAR(20),
    cartid INT,
    PRIMARY KEY (customerid, cartid),
    FOREIGN KEY (customerid) REFERENCES customer(id)
);

CREATE TABLE product_in_shopping_cart (
    productid INT,
    customerid VARCHAR(20),
    cartid INT,
    quantity INT,
    PRIMARY KEY (productid, customerid, cartid),
    FOREIGN KEY (productid) REFERENCES product(productid),
    FOREIGN KEY (customerid, cartid) REFERENCES shopping_cart(customerid, cartid)
);

CREATE TABLE adds (
    customerid VARCHAR(20),
    productid INT,
    PRIMARY KEY (customerid, productid),
    FOREIGN KEY (customerid) REFERENCES customer(id),
    FOREIGN KEY (productid) REFERENCES product(productid)
);

CREATE TABLE customer_payment_method (
    customerid VARCHAR(20),
    payment_method VARCHAR(100),
    PRIMARY KEY (customerid, payment_method),
    FOREIGN KEY (customerid) REFERENCES customer(id)
);


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
('Dwight456','Dunder Miflin'),
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
(123,5,'A fresh bunch of Bananas.','2021-04-24','Banana',2.99,'Jim123','Fruits'),
(456,5,'A dozen fresh Carrots.','2021-4-25','Carrot',4.99,'Dwight456','Vegetables'),
(789,5,'A fresh jug of milk.','2021-4-26','Milk',3.99,'Pam789','Dairy'),
(101,5,'A whole chicken.','2021-4-24','Chicken',5.99,'Micheal101','Meat'),
(112,5,'A fresh loaf of Bread.','2021-4-24','Bread',2.99,'Mose112','Bread');

/*Store_order entries*/
INSERT INTO store_order VALUES
('Y123','123',2.99,'2021-2-20','Credit Card'),
('A123','456',3.99,'2021-2-21','Credit Card'),
('H123','789',4.99,'2021-2-22','Debit Card'),
('J123','101',2.99,'2021-2-23','Debit Card'),
('B123','112',5.99,'2021-2-24','Debit Card');

/*Shopping_cart entries*/
INSERT INTO shopping_cart VALUE
    ('Y123',123),
    ('A123',456),
    ('H123',789),
    ('J123',101),
    ('B123',112);

/*product_in_shopping_cart*/
INSERT INTO product_in_shopping_cart VALUES
    (123,'Y123',123,2),
    (456,'Y123',123,2),
    (789,'A123',456,2),
    (101,'H123',789,2),
    (112,'J123',101,2);

/*Adds entries*/
INSERT INTO adds VALUES
('Y123', 123),
('Y123',456),
('A123',789),
('H123',101),
('J123',112);

/*customer_payment_method entries*/
INSERT INTO customer_payment_method VAlUES
('Y123','Credit Card'),
('A123','Credit Card'),
('H123', 'Debit Card'),
('J123','Debit Card'),
('B123', 'Debit Card');