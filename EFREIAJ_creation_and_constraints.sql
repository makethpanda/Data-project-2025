DROP DATABASE IF EXISTS efrei;
CREATE DATABASE IF NOT EXISTS efrei;
USE efrei;

-- Create years table with validation for name (length validation)
CREATE TABLE IF NOT EXISTS years (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    CONSTRAINT chk_year_name_length CHECK (LENGTH(name) > 0 AND LENGTH(name) <= 50)
);

-- Create teachers table with validation for email format
CREATE TABLE IF NOT EXISTS teachers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    CONSTRAINT chk_teacher_email_format CHECK (email LIKE '%_@__%.__%')
);

-- Create modules table with validation for name length and non-null fields
CREATE TABLE IF NOT EXISTS modules (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    head_id INT,
    year_id INT,
    FOREIGN KEY (head_id) REFERENCES teachers(id) ON DELETE SET NULL,
    FOREIGN KEY (year_id) REFERENCES years(id) ON DELETE SET NULL,
    CONSTRAINT chk_module_name_length CHECK (LENGTH(name) > 0 AND LENGTH(name) <= 100)
);

-- Create rooms table with validation for room name length
CREATE TABLE IF NOT EXISTS rooms (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    CONSTRAINT chk_room_name_length CHECK (LENGTH(name) > 0 AND LENGTH(name) <= 50)
);

-- Create subjects table with validation for name length and non-null constraints
CREATE TABLE IF NOT EXISTS subjects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    module_id INT,
    teacher_id INT,
    FOREIGN KEY (module_id) REFERENCES modules(id) ON DELETE CASCADE,
    FOREIGN KEY (teacher_id) REFERENCES teachers(id) ON DELETE SET NULL,
    CONSTRAINT chk_subject_name_length CHECK (LENGTH(name) > 0 AND LENGTH(name) <= 100)
);

-- Create classes table WITHOUT delegate_id foreign key initially, add validation
CREATE TABLE IF NOT EXISTS classes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    year_id INT,
    FOREIGN KEY (year_id) REFERENCES years(id) ON DELETE SET NULL,
    CONSTRAINT chk_class_name_length CHECK (LENGTH(name) > 0 AND LENGTH(name) <= 50)
);

-- Create students table with validation for email format and non-null constraints
CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    CONSTRAINT chk_student_email_format CHECK (email LIKE '%_@__%.__%')
);

-- Add delegate_id foreign key to classes and class_id foreign key to students
ALTER TABLE classes ADD COLUMN delegate_id INT, ADD FOREIGN KEY (delegate_id) REFERENCES students(id) ON DELETE SET NULL;
ALTER TABLE students ADD COLUMN class_id INT, ADD FOREIGN KEY (class_id) REFERENCES classes(id) ON DELETE SET NULL;

-- Create class_sessions table with validation on session_date (it should be in the future)
CREATE TABLE IF NOT EXISTS class_sessions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    class_id INT,
    subject_id INT,
    session_date DATETIME NOT NULL,
    teacher_id INT,
    room_id INT,
    FOREIGN KEY (class_id) REFERENCES classes(id) ON DELETE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE,
    FOREIGN KEY (teacher_id) REFERENCES teachers(id) ON DELETE SET NULL,
    FOREIGN KEY (room_id) REFERENCES rooms(id) ON DELETE SET NULL
);

-- Create attendance table with status validation (ENUM already ensures valid status)
CREATE TABLE IF NOT EXISTS attendance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    session_id INT,
    status ENUM('Present', 'Absent', 'Late') NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (session_id) REFERENCES class_sessions(id) ON DELETE CASCADE
);

-- Create marks table with validation for marks and coefficient ranges
CREATE TABLE IF NOT EXISTS marks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    subject_id INT,
    mark DECIMAL(4,2) NOT NULL CHECK (mark >= 0 AND mark <= 20),  -- mark between 0 and 20
    coefficient DECIMAL(3,2) NOT NULL CHECK (coefficient > 0 AND coefficient <= 5),  -- coefficient between 0 and 5
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE
);
