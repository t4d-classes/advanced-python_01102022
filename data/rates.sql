CREATE DATABASE app;

USE app;

CREATE TABLE rate (
    id INT AUTO_INCREMENT,
    closing_date DATE,
    currency_symbol VARCHAR(3),
    exchange_rate DECIMAL(18,10),
    PRIMARY KEY(id)
);

INSERT INTO rate (closing_date, currency_symbol, exchange_rate) VALUES ('2019-01-03', 'EUR', 0.8812125485);