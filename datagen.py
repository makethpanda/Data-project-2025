import random
from faker import Faker

# Initialize the Faker object
fake = Faker()

# Helper functions to generate random data
def generate_years():
    return [str(year) for year in range(2024, 2034)]

def generate_teacher():
    return {
        'first_name': fake.first_name(),
        'last_name': fake.last_name(),
        'email': fake.email()
    }

def generate_module(teacher_id, year_id):
    module_names = ['Mathematics', 'Computer Science', 'Physics', 'Chemistry', 'History', 
                    'Biology', 'Geography', 'Economics', 'Philosophy', 'Art']
    return {
        'name': random.choice(module_names),
        'head_id': teacher_id,
        'year_id': year_id
    }

def generate_subject(module_id, teacher_id):
    subject_names = ['Algebra', 'Programming', 'Mechanics', 'Organic Chemistry', 'World History', 
                     'Biology Basics', 'Human Geography', 'Microeconomics', 'Ethical Theory', 'Sculpture']
    return {
        'name': random.choice(subject_names),
        'module_id': module_id,
        'teacher_id': teacher_id
    }

def generate_student(class_id):
    return {
        'first_name': fake.first_name(),
        'last_name': fake.last_name(),
        'email': fake.email(),
        'class_id': class_id
    }

def generate_class_sessions(class_id, subject_id, teacher_id, room_id):
    session_dates = [fake.date_this_year() for _ in range(10)]
    return [{
        'class_id': class_id,
        'subject_id': subject_id,
        'session_date': date,
        'teacher_id': teacher_id,
        'room_id': room_id
    } for date in session_dates]

def generate_attendance(student_id, session_id):
    return {
        'student_id': student_id,
        'session_id': session_id,
        'status': random.choice(['Present', 'Absent', 'Late'])
    }

def generate_marks(student_id, subject_id):
    return {
        'student_id': student_id,
        'subject_id': subject_id,
        'mark': round(random.uniform(10, 20), 2),
        'coefficient': random.choice([1.0, 1.5, 2.0, 2.5, 3.0])
    }

# Generate SQL data
def generate_sql_data(num_teachers=10, num_classes=10, num_students=100, num_subjects=10):
    sql_lines = []

    # Insert years
    sql_lines.append("INSERT INTO years (name) VALUES " + ",".join([f"('{year}')" for year in generate_years()]) + ";")
    
    # Insert teachers
    for i in range(num_teachers):
        teacher = generate_teacher()
        sql_lines.append(f"INSERT INTO teachers (first_name, last_name, email) VALUES ('{teacher['first_name']}', '{teacher['last_name']}', '{teacher['email']}');")
    
    # Insert modules and subjects
    module_id = 1
    for year in range(1, 11):  # For each year
        for teacher_id in range(1, num_teachers+1):
            module = generate_module(teacher_id, year)
            sql_lines.append(f"INSERT INTO modules (name, head_id, year_id) VALUES ('{module['name']}', {module['head_id']}, {year});")
            subject = generate_subject(module_id, teacher_id)
            sql_lines.append(f"INSERT INTO subjects (name, module_id, teacher_id) VALUES ('{subject['name']}', {module_id}, {teacher_id});")
            module_id += 1
    
    # Insert classes
    for i in range(1, num_classes+1):
        sql_lines.append(f"INSERT INTO classes (name, year_id) VALUES ('Class {chr(64+i)}', {random.choice(range(1, 11))});")

    # Insert students
    class_id = 1
    for i in range(num_students):
        student = generate_student(class_id)
        sql_lines.append(f"INSERT INTO students (first_name, last_name, email, class_id) VALUES ('{student['first_name']}', '{student['last_name']}', '{student['email']}', {student['class_id']});")
        class_id = random.choice(range(1, num_classes+1))  # Assign randomly to different classes
    
    # Insert class sessions
    for class_id in range(1, num_classes+1):
        for subject_id in range(1, num_subjects+1):
            for teacher_id in range(1, num_teachers+1):
                room_id = random.choice(range(1, 11))  # 10 rooms available
                sessions = generate_class_sessions(class_id, subject_id, teacher_id, room_id)
                for session in sessions:
                    sql_lines.append(f"INSERT INTO class_sessions (class_id, subject_id, session_date, teacher_id, room_id) VALUES ({session['class_id']}, {session['subject_id']}, '{session['session_date']}', {session['teacher_id']}, {session['room_id']});")
    
    # Insert attendance
    for student_id in range(1, num_students+1):
        for session_id in range(1, num_teachers * num_subjects * 10 + 1):
            attendance = generate_attendance(student_id, session_id)
            sql_lines.append(f"INSERT INTO attendance (student_id, session_id, status) VALUES ({attendance['student_id']}, {attendance['session_id']}, '{attendance['status']}');")
    
    # Insert marks
    for student_id in range(1, num_students+1):
        for subject_id in range(1, num_subjects+1):
            marks = generate_marks(student_id, subject_id)
            sql_lines.append(f"INSERT INTO marks (student_id, subject_id, mark, coefficient) VALUES ({marks['student_id']}, {marks['subject_id']}, {marks['mark']}, {marks['coefficient']});")
    
    return sql_lines

# Write SQL to a file
def write_sql_to_file(filename, sql_lines):
    with open(filename, 'w') as f:
        for line in sql_lines:
            f.write(line + "\n")

# Generate data and write to file
sql_data = generate_sql_data()
write_sql_to_file('generated_data.sql', sql_data)

print("SQL file 'generated_data.sql' created successfully!")
