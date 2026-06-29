CREATE DATABASE sftp_db;
USE sftp_db;
 
CREATE TABLE users (
    id_user INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50),
    surname VARCHAR(50),
    username VARCHAR(50) UNIQUE,
    mail VARCHAR(100) UNIQUE,
    password VARCHAR(200),
    password_pgp VARCHAR(200) NULL,
    location VARCHAR(100) NULL,
    account_status INT DEFAULT 1,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_login DATETIME NULL,
    public_key TEXT NULL,
    private_key TEXT NULL
);
 
CREATE TABLE files (
    id_file INT PRIMARY KEY AUTO_INCREMENT,
    file_name VARCHAR(255),
    secure_name VARCHAR(255) UNIQUE,
    file_size BIGINT,
    mime_type VARCHAR(100),
    upload_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
 
CREATE TABLE uploads (
    id_upload INT PRIMARY KEY AUTO_INCREMENT,
    id_user INT,
    id_file INT,
    uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_user) REFERENCES users(id_user),
    FOREIGN KEY (id_file) REFERENCES files(id_file)
);
 
CREATE TABLE shares (
    id_share INT PRIMARY KEY AUTO_INCREMENT,
    id_file INT,
    id_sender INT,
    id_receiver INT,
    shared_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    expires_at DATETIME,
    is_downloaded BOOLEAN DEFAULT FALSE,
    download_count INT DEFAULT 0,
    encryption_type VARCHAR(20) DEFAULT 'AES-256',
    message TEXT,
    FOREIGN KEY (id_file) REFERENCES files(id_file),
    FOREIGN KEY (id_sender) REFERENCES users(id_user),
    FOREIGN KEY (id_receiver) REFERENCES users(id_user)
);
 
CREATE TABLE friendships (
    id_friendship INT PRIMARY KEY AUTO_INCREMENT,
    id_requester INT,
    id_receiver INT,
    status VARCHAR(20) DEFAULT 'pending',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_requester) REFERENCES users(id_user),
    FOREIGN KEY (id_receiver) REFERENCES users(id_user)
);
 
CREATE TABLE logs (
    id_log INT PRIMARY KEY AUTO_INCREMENT,
    id_user INT,
    id_file INT,
    action_type VARCHAR(50),
    ip_address VARCHAR(45),
    log_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_user) REFERENCES users(id_user),
    FOREIGN KEY (id_file) REFERENCES files(id_file)
);

CREATE TABLE ban_records (
    id_ban INT PRIMARY KEY AUTO_INCREMENT,
    id_user INT, 
    id_admin INT, 
    banned_at DATETIME DEFAULT CURRENT_TIMESTAMP, 
    unbanned_at DATETIME NULL, 
    reason VARCHAR(255), 
    FOREIGN KEY (id_user) REFERENCES users(id_user), 
    FOREIGN KEY (id_admin) REFERENCES users(id_user) 
); 


