CREATE TABLE IF NOT EXISTS subscribers (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone VARCHAR(40),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Safe to add index separately
CREATE INDEX idx_subscribers_email ON subscribers(email);
