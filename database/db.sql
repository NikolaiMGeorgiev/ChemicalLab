CREATE DATABASE chemical
CREATE TABLE users (id INT AUTO_INCREMENT PRIMARY KEY, name varchar(255), age int, weight float, height float, bodyfat float);
CREATE TABLE diary (id INT AUTO_INCREMENT PRIMARY KEY, user_id int, chemical varchar(255), quantity float, date datetime);
CREATE TABLE lab_history (id INT AUTO_INCREMENT PRIMARY KEY, user_id int, substance varchar(255), muscle_mass int, body_fat int, energy int, stength int, cancer int, impotence int, diabetes int, heart_disease int);