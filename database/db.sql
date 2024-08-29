CREATE DATABASE chemical
CREATE TABLE users (id int AUTO_INCREMENT PRIMARY KEY, name varchar(255), age int, weight float, height float, bodyfat float);
CREATE TABLE vendors (id int AUTO_INCREMENT PRIMARY KEY, name varchar(255));
CREATE TABLE chats (id int AUTO_INCREMENT PRIMARY KEY, user_id int, vendor_id int DEFAULT NULL);
CREATE TABLE messages (id int AUTO_INCREMENT PRIMARY KEY, chat_id int, content text, sent_time datetime DEFAULT NOW(), sender varchar(256), `read` int DEFAULT 0);
CREATE TABLE diary (id int AUTO_INCREMENT PRIMARY KEY, user_id int, chemical varchar(255), quantity float, date datetime);
CREATE TABLE lab_history (id int AUTO_INCREMENT PRIMARY KEY, user_id int, substance varchar(255), muscle_mass int, body_fat int, energy int, stength int, cancer int, impotence int, diabetes int, heart_disease int);

INSERT INTO vendors (name) VALUES ("Ven Dor I")
INSERT INTO vendors (name) VALUES ("Ven Dor II")