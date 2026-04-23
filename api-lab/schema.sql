-- API Security Lab Database Schema
-- PostgreSQL 15 - 6 Challenges

-- USERS TABLE
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100),
    role VARCHAR(20) DEFAULT 'user' CHECK (role IN ('user', 'admin', 'moderator')),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- ITEMS TABLE
CREATE TABLE items (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10,2),
    category VARCHAR(50),
    owner_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- SECRETS TABLE
CREATE TABLE secrets (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    secret_name VARCHAR(100),
    secret_value TEXT
);

-- CUSTOMERS TABLE (for v6 SQLi)
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(20),
    address TEXT,
    credit_card VARCHAR(255)
);

-- TRANSACTIONS TABLE (for v4)
CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    amount DECIMAL(10,2),
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT NOW()
);

-- RATE LIMITED LOG (for v4)
CREATE TABLE rate_limit_log (
    id SERIAL PRIMARY KEY,
    ip_address VARCHAR(45),
    endpoint VARCHAR(100),
    request_count INTEGER DEFAULT 1,
    window_start TIMESTAMP DEFAULT NOW()
);

-- SEED DATA

-- Users (id: 1=admin, 2-4=regular users)
INSERT INTO users (username, password, email, role) VALUES
('admin', 'admin123', 'admin@apilab.local', 'admin'),
('john', 'john123', 'john@apilab.local', 'user'),
('jane', 'jane123', 'jane@apilab.local', 'user'),
('bob', 'bob123', 'bob@apilab.local', 'user'),
('alice', 'alice123', 'alice@apilab.local', 'moderator');

-- Items
INSERT INTO items (name, description, price, category, owner_id) VALUES
('Laptop Pro', '15 inch Dell XPS', 1299.99, 'electronics', 2),
('Wireless Mouse', 'Logitech MX Master', 89.99, 'electronics', 2),
('Office Chair', 'Ergonomic Herman Miller', 899.99, 'furniture', 3),
('Standing Desk', 'Electric standing desk', 599.99, 'furniture', 3),
('Monitor 4K', '27 inch LG 4K', 449.99, 'electronics', 4),
('Mechanical Keyboard', 'Custom mechanical keyboard', 159.99, 'electronics', 2);

-- Secrets (sensitive data)
INSERT INTO secrets (user_id, secret_name, secret_value) VALUES
(1, 'api_key', 'sk_live_adminey1827364'),
(1, 'admin_notes', 'TOP SECRET: Project Omega'),
(1, 'root_password', 'super_secret_root_pass'),
(2, 'ssn', '123-45-6789'),
(2, 'cc_number', '4111111111111111'),
(2, 'api_token', 'user_john_token_abc'),
(3, 'ssn', '987-65-4321'),
(3, 'cc_number', '4222222222222222'),
(3, 'api_token', 'user_jane_token_xyz');

-- Customers (for v6 SQLi)
INSERT INTO customers (name, email, phone, address, credit_card) VALUES
('Alice Johnson', 'alice@email.com', '555-0101', '123 Main St, Springfield, IL', '4111111111111111'),
('Charlie Brown', 'charlie@email.com', '555-0102', '456 Oak Ave, Chicago, IL', '4222222222222222'),
('David Lee', 'david@email.com', '555-0103', '789 Pine Rd, Boston, MA', '4333333333333333'),
('Eva Martinez', 'eva@email.com', '555-0104', '321 Elm St, NYC, NY', '4444444444444444'),
('Frank Miller', 'frank@email.com', '555-0105', '654 Maple Dr, Seattle, WA', '4555555555555555'),
('Grace Kim', 'grace@email.com', '555-0106', '987 Cedar Ln, Austin, TX', '4666666666666666');

-- Transactions
INSERT INTO transactions (user_id, amount, status) VALUES
(2, 1299.99, 'completed'),
(2, 89.99, 'completed'),
(3, 899.99, 'completed'),
(3, 599.99, 'pending'),
(4, 449.99, 'completed');

-- Indexes for performance
CREATE INDEX idx_items_owner ON items(owner_id);
CREATE INDEX idx_secrets_user ON secrets(user_id);
CREATE INDEX idx_transactions_user ON transactions(user_id);
CREATE INDEX idx_customers_email ON customers(email);
CREATE INDEX idx_users_username ON users(username);