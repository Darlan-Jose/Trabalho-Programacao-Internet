USE stc;

DROP TABLE IF EXISTS admins;
DROP TABLE IF EXISTS dealers;

CREATE TABLE admins (
    admin_name VARCHAR(10) PRIMARY KEY,
    passwd VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE dealers (
    dealer_id VARCHAR(5) PRIMARY KEY,
    dealer_name VARCHAR(20) NOT NULL,
    dlpasswd VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Senha: 'test'
INSERT INTO admins (admin_name, passwd) VALUES 
('root', '$2b$12$5dAZwB6dbdjLH2V0riROEuBu4TjMgClfHJeAwPF7XNEpWmRPqS6.G');

-- Senha: 'dealer123'
INSERT INTO dealers (dealer_id, dealer_name, dlpasswd) VALUES 
('D001', 'João Silva', '$2b$12$5dAZwB6dbdjLH2V0riROEuu6Prk1lvhNveh6ffuf98e7yxLMl3u5S');