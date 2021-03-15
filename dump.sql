CREATE TABLE user (
    userid VARCHAR(20), 
    user_password CHAR(100) NOT NULL,
    house_number INT,
    street_name VARCHAR(100),
    postal_code VARCHAR(20),
    province VARCHAR(100),
    city VARCHAR(100),
    email VARCHAR(100),
    PRIMARY KEY (userid),
    CONSTRAINT uid_valid CHECK (userid>=0),
    CONSTRAINT hnum_valid CHECK (house_number>=0),
    CONSTRAINT password_valid CHECK (LENGTH(user_password)>=1),
    CONSTRAINT email_valid CHECK (Email REGEXP '^[0-9A-Za-z._-]+@[0-9A-Za-z.-]+\.[a-zA-Z0-9-.]+$')
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
    best_before_date DATE NOT NULL,
    product_name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2),
    sellerid INT,
    category_name CHAR(100),
    PRIMARY KEY (productid),
    FOREIGN KEY (sellerid) REFERENCES seller(id),
    FOREIGN KEY (category_name) REFERENCES category(category_name),
    CONSTRAINT pid_valid CHECK (productid >= 0),
    CONSTRAINT stock_valid CHECK (stock >= 0),
    CONSTRAINT bbdate_valid CHECK (best_before_date > CURRENT_DATE),
    CONSTRAINT price_valid CHECK (price >= 0.0)
);

CREATE TABLE store_order (
    customerid VARCHAR(20),
    orderid INT,
    cost DECIMAL(10, 2),
    order_time DATE,
    payment_method_used VARCHAR(100),
    PRIMARY KEY (customerid, orderid),
    FOREIGN KEY (customerid) REFERENCES customer(id),
    CONSTRAINT oid_valid CHECK (orderid>=0),
    CONSTRAINT cost_valid CHECK (cost>=0.0),
    CONSTRAINT time_valid CHECK (order_time<=CURRENT_DATE)
);

CREATE TABLE shopping_cart (
    customerid VARCHAR(20),
    cartid INT,
    PRIMARY KEY (customerid, cartid),
    FOREIGN KEY (customerid) REFERENCES customer(id),
    CONSTRAINT cid_valid CHECK (cartid>=0)
);

CREATE TABLE product_in_shopping_cart (
    productid INT,
    customerid VARCHAR(20),
    cartid INT,
    quantity INT,
    PRIMARY KEY (productid, customerid, cartid),
    FOREIGN KEY (productid) REFERENCES product(productid),
    FOREIGN KEY (customerid, cartid) REFERENCES shopping_cart(customerid, cartid),
    CONSTRAINT qnty_valid CHECK (quantity>=0)
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
