-- Удаление таблиц, если они уже существуют
DROP TABLE IF EXISTS registration_log;
DROP TABLE IF EXISTS registrations;
DROP TABLE IF EXISTS course_assignments;
DROP TABLE IF EXISTS professors;
DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS courses;

-- Создаем таблицу студентов
CREATE TABLE students (
    student_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    date_of_birth DATE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);

-- Создаем таблицу курсов
CREATE TABLE courses (
    course_id SERIAL PRIMARY KEY,
    course_name VARCHAR(100) NOT NULL,
    course_description TEXT,
    course_credits INT NOT NULL
);

-- Создаем таблицу преподавателей
CREATE TABLE professors (
    professor_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    department VARCHAR(100) NOT NULL
);

-- Создаем таблицу назначений курсов
CREATE TABLE course_assignments (
    assignment_id SERIAL PRIMARY KEY,
    course_id INT NOT NULL,
    professor_id INT NOT NULL,
    assignment_date DATE NOT NULL,
    FOREIGN KEY (course_id) REFERENCES courses(course_id),
    FOREIGN KEY (professor_id) REFERENCES professors(professor_id)
);

-- Создаем таблицу регистраций
CREATE TABLE registrations (
    registration_id SERIAL PRIMARY KEY,
    student_id INT NOT NULL,
    course_id INT NOT NULL,
    registration_date DATE NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);

-- Заполнение таблицы студентов
INSERT INTO students (first_name, last_name, date_of_birth, email) VALUES
('John', 'Doe', '1995-05-20', 'john.doe@example.com'),
('Jane', 'Smith', '1996-08-15', 'jane.smith@example.com'),
('Alice', 'Johnson', '1997-03-22', 'alice.johnson@example.com'),
('Bob', 'Brown', '1994-11-12', 'bob.brown@example.com'),
('Carol', 'Davis', '1998-07-30', 'carol.davis@example.com'),
('David', 'Clark', '1997-05-14', 'david.clark@example.com'),
('Emma', 'Walker', '1996-10-22', 'emma.walker@example.com'),
('Frank', 'Wright', '1995-06-18', 'frank.wright@example.com'),
('Grace', 'Hall', '1997-08-05', 'grace.hall@example.com'),
('Hank', 'Lee', '1996-01-12', 'hank.lee@example.com'),
('Ivy', 'Harris', '1998-09-23', 'ivy.harris@example.com'),
('Jack', 'Young', '1994-12-31', 'jack.young@example.com'),
('Kathy', 'King', '1995-11-11', 'kathy.king@example.com'),
('Liam', 'Hill', '1997-04-03', 'liam.hill@example.com'),
('Mia', 'Green', '1996-05-25', 'mia.green@example.com'),
('Noah', 'Adams', '1998-10-15', 'noah.adams@example.com'),
('Olivia', 'Nelson', '1997-02-10', 'olivia.nelson@example.com'),
('Paul', 'Baker', '1995-03-20', 'paul.baker@example.com'),
('Quinn', 'Carter', '1996-06-17', 'quinn.carter@example.com'),
('Ryan', 'Mitchell', '1998-12-07', 'ryan.mitchell@example.com');

-- Заполнение таблицы курсов
INSERT INTO courses (course_name, course_credits, course_description) VALUES
('Mathematics', 3, 'An introduction to mathematical concepts'),
('History', 4, 'Overview of world history'),
('Physics', 4, 'Fundamentals of Physics'),
('Chemistry', 3, 'Basics of Chemistry'),
('Biology', 3, 'Introduction to Biology'),
('Computer Science', 3, 'Basics of computer science'),
('English Literature', 4, 'Study of English literature'),
('Art History', 3, 'Introduction to art history'),
('Economics', 4, 'Principles of economics'),
('Philosophy', 3, 'Introduction to philosophy'),
('Political Science', 4, 'Basics of political science'),
('Psychology', 3, 'Fundamentals of psychology'),
('Sociology', 3, 'Introduction to sociology'),
('Statistics', 3, 'Basics of statistics'),
('Anthropology', 4, 'Introduction to anthropology'),
('Music Theory', 3, 'Fundamentals of music theory'),
('Geography', 3, 'Basics of geography'),
('Environmental Science', 4, 'Introduction to environmental science'),
('Linguistics', 3, 'Study of language structures'),
('Theatre Arts', 3, 'Basics of theatre arts');

-- Заполнение таблицы преподавателей
INSERT INTO professors (first_name, last_name, department) VALUES
('Dr. Emily', 'Clark', 'Mathematics'),
('Dr. Michael', 'Brown', 'History'),
('Dr. Sarah', 'Wilson', 'Physics'),
('Dr. James', 'Taylor', 'Chemistry'),
('Dr. Linda', 'Miller', 'Biology'),
('Dr. William', 'Moore', 'Computer Science'),
('Dr. Elizabeth', 'Jackson', 'English Literature'),
('Dr. Daniel', 'White', 'Art History'),
('Dr. Patricia', 'Harris', 'Economics'),
('Dr. Robert', 'Martin', 'Philosophy'),
('Dr. Barbara', 'Thompson', 'Political Science'),
('Dr. Richard', 'Garcia', 'Psychology'),
('Dr. Mary', 'Martinez', 'Sociology'),
('Dr. Charles', 'Robinson', 'Statistics'),
('Dr. Joseph', 'Walker', 'Anthropology'),
('Dr. Susan', 'Young', 'Music Theory'),
('Dr. Thomas', 'Allen', 'Geography'),
('Dr. Karen', 'King', 'Environmental Science'),
('Dr. Christopher', 'Wright', 'Linguistics'),
('Dr. Jennifer', 'Scott', 'Theatre Arts');

-- Заполнение таблицы назначений курсов
INSERT INTO course_assignments (course_id, professor_id, assignment_date) VALUES
(1, 1, '2023-01-05'),
(2, 2, '2023-01-10'),
(3, 3, '2023-01-15'),
(4, 4, '2023-01-20'),
(5, 5, '2023-01-25'),
(6, 6, '2023-02-01'),
(7, 7, '2023-02-05'),
(8, 8, '2023-02-10'),
(9, 9, '2023-02-15'),
(10, 10, '2023-02-20'),
(11, 11, '2023-02-25'),
(12, 12, '2023-03-01'),
(13, 13, '2023-03-05'),
(14, 14, '2023-03-10'),
(15, 15, '2023-03-15'),
(16, 16, '2023-03-20'),
(17, 17, '2023-03-25'),
(18, 18, '2023-03-30'),
(19, 19, '2023-04-01'),
(20, 20, '2023-04-05');

-- Заполнение таблицы регистраций
INSERT INTO registrations (student_id, course_id, registration_date) VALUES
(1, 1, '2023-01-10'),
(2, 2, '2023-02-12'),
(3, 3, '2023-03-10'),
(4, 4, '2023-04-15'),
(5, 5, '2023-05-20'),
(6, 6, '2023-06-25'),
(7, 7, '2023-07-30'),
(8, 8, '2023-08-05'),
(9, 9, '2023-09-10'),
(10, 10, '2023-10-15'),
(11, 11, '2023-11-20'),
(12, 12, '2023-12-25'),
(13, 13, '2023-01-30'),
(14, 14, '2023-02-04'),
(15, 15, '2023-03-10'),
(16, 16, '2023-04-15'),
(17, 17, '2023-05-20'),
(18, 18, '2023-06-25'),
(19, 19, '2023-07-30'),
(20, 20, '2023-08-05'),
(1, 2, '2023-09-10'),
(2, 3, '2023-10-15'),
(3, 4, '2023-11-20'),
(4, 5, '2023-12-25'),
(5, 6, '2023-01-30'),
(6, 7, '2023-02-04'),
(7, 8, '2023-03-10'),
(8, 9, '2023-04-15'),
(9, 10, '2023-05-20'),
(10, 11, '2023-06-25'),
(11, 12, '2023-07-30'),
(12, 13, '2023-08-05'),
(13, 14, '2023-09-10'),
(14, 15, '2023-10-15'),
(15, 16, '2023-11-20'),
(16, 17, '2023-12-25'),
(17, 18, '2023-01-30'),
(18, 19, '2023-02-04'),
(19, 20, '2023-03-10'),
(20, 1, '2023-04-15');

-- Создание таблицы для логов регистраций
CREATE TABLE registration_log (
    log_id SERIAL PRIMARY KEY,
    student_id INT NOT NULL,
    course_id INT NOT NULL,
    registration_date DATE NOT NULL,
    log_date TIMESTAMP NOT NULL
);

-- Создание триггера для логирования регистраций
CREATE OR REPLACE FUNCTION log_registration() RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO registration_log (student_id, course_id, registration_date, log_date)
    VALUES (NEW.student_id, NEW.course_id, NEW.registration_date, CURRENT_TIMESTAMP);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Привязка триггера к таблице регистраций
CREATE TRIGGER after_registration
AFTER INSERT ON registrations
FOR EACH ROW
EXECUTE FUNCTION log_registration();
