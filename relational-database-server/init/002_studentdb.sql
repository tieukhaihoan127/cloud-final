-- Create new database
CREATE DATABASE IF NOT EXISTS studentdb;
USE studentdb;

-- Create students table
CREATE TABLE IF NOT EXISTS students (
  id INT PRIMARY KEY AUTO_INCREMENT,
  student_id VARCHAR(10),
  fullname VARCHAR(100),
  dob DATE,
  major VARCHAR(50)
);

-- Insert sample data
INSERT INTO students (student_id, fullname, dob, major) VALUES
('SV001', 'Nguyen Van A', '2002-05-10', 'Computer Science'),
('SV002', 'Tran Thi B', '2003-11-20', 'Information Systems'),
('SV003', 'Le Van C', '2001-09-15', 'Software Engineering');

-- UPDATE
UPDATE students
SET major = 'Computer Engineering'
WHERE student_id = 'SV001';

-- DELETE
DELETE FROM students
WHERE student_id = 'SV003';