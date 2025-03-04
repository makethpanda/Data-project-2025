-- 1️⃣ Basic Checks

-- Check all students and their assigned classes
SELECT s.id, s.first_name, s.last_name, c.name AS class_name
FROM students s
JOIN classes c ON s.class_id = c.id
ORDER BY c.name, s.last_name;

-- List all head teachers and their assigned subjects
SELECT t.id, t.first_name, t.last_name, sub.name AS subject_name
FROM teachers t
JOIN subjects sub ON t.id = sub.teacher_id
ORDER BY t.last_name;

-- Count the number of students per class
SELECT c.name AS class_name, COUNT(s.id) AS student_count
FROM classes c
LEFT JOIN students s ON c.id = s.class_id
GROUP BY c.name
ORDER BY student_count DESC;

-- 2️⃣ Class & Session Insights

-- Find subjects taught in each class
SELECT c.name AS class_name, sub.name AS subject_name
FROM class_sessions cs
JOIN classes c ON cs.class_id = c.id
JOIN subjects sub ON cs.subject_id = sub.id
GROUP BY c.name, sub.name
ORDER BY c.name;

-- Find the busiest teachers (who have the most sessions assigned)
SELECT t.id, t.first_name, t.last_name, COUNT(cs.id) AS session_count
FROM teachers t
JOIN class_sessions cs ON t.id = cs.teacher_id
GROUP BY t.id
ORDER BY session_count DESC
LIMIT 5;


--  Classe sessions in the past month
SELECT cs.id, c.name AS class_name, sub.name AS subject_name, cs.session_date, r.name AS room
FROM class_sessions cs
JOIN classes c ON cs.class_id = c.id
JOIN subjects sub ON cs.subject_id = sub.id
JOIN rooms r ON cs.room_id = r.id
WHERE cs.session_date BETWEEN DATE_SUB(CURDATE(), INTERVAL 1 MONTH) AND CURDATE()
ORDER BY cs.session_date;

-- 3️⃣ Student Performance & Grades

-- Find the top-performing students in each subject
SELECT s.first_name, s.last_name, sub.name AS subject_name, m.mark
FROM marks m
JOIN students s ON m.student_id = s.id
JOIN subjects sub ON m.subject_id = sub.id
WHERE m.mark = (SELECT MAX(m2.mark) FROM marks m2 WHERE m2.subject_id = m.subject_id)
ORDER BY sub.name, m.mark DESC;

-- Get the average grade per subject
SELECT sub.name AS subject_name, ROUND(AVG(m.mark), 2) AS avg_mark
FROM marks m
JOIN subjects sub ON m.subject_id = sub.id
GROUP BY sub.name
ORDER BY avg_mark DESC;

-- Find students who are failing (average mark below 10)
SELECT s.first_name, s.last_name, ROUND(AVG(m.mark), 2) AS avg_mark
FROM marks m
JOIN students s ON m.student_id = s.id
GROUP BY s.id
HAVING avg_mark < 10
ORDER BY avg_mark ASC;

-- Find students with the highest total weighted score (mark * coefficient)
SELECT s.first_name, s.last_name, SUM(m.mark * m.coefficient) AS total_score
FROM marks m
JOIN students s ON m.student_id = s.id
GROUP BY s.id
ORDER BY total_score DESC
LIMIT 5;

-- 4️⃣ Room & Schedule Management

-- Check room usage (sessions per room)
SELECT r.name AS room_name, COUNT(cs.id) AS session_count
FROM rooms r
JOIN class_sessions cs ON r.id = cs.room_id
GROUP BY r.id
ORDER BY session_count DESC;

-- Find overlapping class sessions (same room, same time)
SELECT cs1.session_date, r.name AS room_name, c1.name AS class_1, c2.name AS class_2
FROM class_sessions cs1
JOIN class_sessions cs2 ON cs1.room_id = cs2.room_id AND cs1.session_date = cs2.session_date AND cs1.id <> cs2.id
JOIN rooms r ON cs1.room_id = r.id
JOIN classes c1 ON cs1.class_id = c1.id
JOIN classes c2 ON cs2.class_id = c2.id
ORDER BY cs1.session_date;

-- Find the most commonly used room
SELECT r.name AS room_name, COUNT(cs.id) AS usage_count
FROM rooms r
JOIN class_sessions cs ON r.id = cs.room_id
GROUP BY r.id
ORDER BY usage_count DESC
LIMIT 1;

-- 5️⃣ Advanced Queries & Insights

-- Find which class has the highest average student mark
SELECT c.name AS class_name, ROUND(AVG(m.mark), 2) AS avg_mark
FROM marks m
JOIN students s ON m.student_id = s.id
JOIN classes c ON s.class_id = c.id
GROUP BY c.id
ORDER BY avg_mark DESC;

-- Find the hardest subject (lowest average mark)
SELECT sub.name AS subject_name, ROUND(AVG(m.mark), 2) AS avg_mark
FROM marks m
JOIN subjects sub ON m.subject_id = sub.id
GROUP BY sub.id
ORDER BY avg_mark ASC
LIMIT 1;


-- Find students who have perfect scores in at least one subject
SELECT DISTINCT s.first_name, s.last_name
FROM marks m
JOIN students s ON m.student_id = s.id
WHERE m.mark = 20;


-- Find which teachers have the highest student success rate (average grade of students they teach)
SELECT t.id, t.first_name, t.last_name, ROUND(AVG(m.mark), 2) AS avg_student_grade
FROM teachers t
JOIN subjects sub ON t.id = sub.teacher_id
JOIN marks m ON sub.id = m.subject_id
GROUP BY t.id
ORDER BY avg_student_grade DESC;

-- test

SELECT
    t.first_name AS teacher_first_name,
    t.last_name AS teacher_last_name,
    s.name AS subject_name,
    c.name AS class_name,
    cs.session_date
FROM
    teachers t
JOIN
    class_sessions cs ON t.id = cs.teacher_id
JOIN
    subjects s ON cs.subject_id = s.id
JOIN
    classes c ON cs.class_id = c.id
ORDER BY
    t.first_name, t.last_name, cs.session_date;
    
    -- test 2
    
    SELECT
    t.first_name AS teacher_first_name,
    t.last_name AS teacher_last_name,
    m.name AS module_name
FROM
    teachers t
JOIN
    modules m ON t.id = m.head_id
ORDER BY
    t.first_name, t.last_name;