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
    productid INT,
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

CREATE TRIGGER `user_insert_constraints` BEFORE INSERT ON `user`
FOR EACH ROW  
IF LENGTH(NEW.userid) < 1 OR NEW.house_number < 0 OR LENGTH(NEW.user_password) < 1 OR NEW.email NOT LIKE '%_@__%.__%' 
THEN
    SIGNAL SQLSTATE '45000';
END IF;$$

CREATE TRIGGER `user_update_constraints` BEFORE UPDATE ON `user`
FOR EACH ROW IF LENGTH(NEW.userid) < 1 OR NEW.house_number < 0 OR LENGTH(NEW.user_password) < 1 OR NEW.email NOT LIKE '%_@__%.__%' 
THEN
    SIGNAL SQLSTATE '45000';
END IF;$$

CREATE TRIGGER `product_insert_constraints` BEFORE INSERT ON `product`
FOR EACH ROW IF NEW.productid < 0 OR NEW.stock < 0 OR NEW.best_before_date <= CURRENT_DATE OR NEW.price < 0.0 
THEN
    SIGNAL SQLSTATE '45000';
END IF;$$

CREATE TRIGGER `product_update_constraints` BEFORE UPDATE ON `product`
FOR EACH ROW IF NEW.productid < 0 OR NEW.stock < 0 OR NEW.best_before_date <= CURRENT_DATE OR NEW.price < 0.0 
THEN
    SIGNAL SQLSTATE '45000';
END IF;$$

CREATE TRIGGER `store_order_insert_constraints` BEFORE INSERT ON `store_order`
FOR EACH ROW IF NEW.orderid < 0 OR NEW.cost < 0.0 OR NEW.order_time > CURRENT_DATE 
THEN
    SIGNAL SQLSTATE '45000';
END IF;$$

CREATE TRIGGER `store_order_update_constraints` BEFORE UPDATE ON `store_order`
FOR EACH ROW IF NEW.orderid < 0 OR NEW.cost < 0.0 OR NEW.order_time > CURRENT_DATE 
THEN
    SIGNAL SQLSTATE '45000';
END IF;$$

CREATE TRIGGER `shopping_cart_update_constraint` BEFORE UPDATE ON `shopping_cart`
FOR EACH ROW IF NEW.cartid < 0 
THEN
    SIGNAL SQLSTATE '45000';
END IF;$$

CREATE TRIGGER `shopping_cart_insert_constraint` BEFORE INSERT ON `shopping_cart`
FOR EACH ROW IF NEW.cartid < 0 
THEN
    SIGNAL SQLSTATE '45000';
END IF;$$

CREATE TRIGGER `product_in_shopping_cart_insert_constraints` BEFORE INSERT ON `product_in_shopping_cart`
FOR EACH ROW IF NEW.quantity < 0 
THEN
    SIGNAL SQLSTATE '45000';
END IF;$$

CREATE TRIGGER `product_in_shopping_cart_update_constraints` BEFORE UPDATE ON `product_in_shopping_cart`
FOR EACH ROW IF NEW.quantity < 0 
THEN
    SIGNAL SQLSTATE '45000';
END IF;$$






