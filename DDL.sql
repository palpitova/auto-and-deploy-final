CREATE TABLE IF NOT EXISTS data_shops (
    id SERIAL PRIMARY KEY,
    doc_id VARCHAR(50) NOT NULL,
    shop_id INTEGER NOT NULL,
    cash_id INTEGER NOT NULL,
    item_name VARCHAR(255) NOT NULL,
    category VARCHAR(100),
    amount INTEGER NOT NULL,
    price NUMERIC(10, 2) NOT NULL,
    discount NUMERIC(10, 2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
