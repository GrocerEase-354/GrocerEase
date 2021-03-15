CREATE TABLE user (
    userid INT, 
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
    id INT,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    PRIMARY KEY (id),
    FOREIGN KEY (id) REFERENCES user(userid)
);

CREATE TABLE seller (
    id INT,
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
    sellerid INT,
    category_name CHAR(100),
    PRIMARY KEY (productid),
    FOREIGN KEY (sellerid) REFERENCES seller(id),
    FOREIGN KEY (category_name) REFERENCES category(category_name)
);

CREATE TABLE store_order (
    customerid INT,
    orderid INT,
    cost DECIMAL(10, 2),
    order_time DATE,
    payment_method_used VARCHAR(100),
    PRIMARY KEY (customerid, orderid),
    FOREIGN KEY (customerid) REFERENCES customer(id)
);

CREATE TABLE shopping_cart (
    customerid INT,
    cartid INT,
    PRIMARY KEY (customerid, cartid),
    FOREIGN KEY (customerid) REFERENCES customer(id)
);

CREATE TABLE product_in_shopping_cart (
    productid INT,
    customerid INT,
    cartid INT,
    quantity INT,
    PRIMARY KEY (productid, customerid, cartid),
    FOREIGN KEY (productid) REFERENCES product(productid),
    FOREIGN KEY (customerid, cartid) REFERENCES shopping_cart(customerid, cartid)
);

CREATE TABLE adds (
    customerid INT,
    productid INT,
    PRIMARY KEY (customerid, productid),
    FOREIGN KEY (customerid) REFERENCES customer(id),
    FOREIGN KEY (productid) REFERENCES product(productid)
);

CREATE TABLE customer_payment_method (
    customerid INT,
    payment_method VARCHAR(100),
    PRIMARY KEY (customerid, payment_method),
    FOREIGN KEY (customerid) REFERENCES customer(id)
);