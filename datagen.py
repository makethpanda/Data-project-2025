import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()

# Fixed parameters
YEAR_ID = 1  # L1 2025
NUM_CLASSES = 4  # INT 1, INT 2, PLUS 1, PLUS 2
NUM_STUDENTS_PER_CLASS = (30, 40)
NUM_TEACHERS = 10
NUM_MODULES = 4
NUM_SUBJECTS = 4
NUM_ROOMS = 5  # Ensure rooms exist in DB
SESSIONS_PER_SUBJECT = 3

# Predefined modules and subjects
MODULES = ['Mathematics', 'Computer Science', 'Physics', 'Chemistry']
SUBJECTS = {
    'Mathematics': ['Algebra', 'Calculus'],
    'Computer Science': ['Programming', 'Data Structures'],
    'Physics': ['Mechanics', 'Electromagnetism'],
    'Chemistry': ['Organic Chemistry', 'Inorganic Chemistry']
}

# Function to generate random date + time in SQL DATETIME format
def generate_random_datetime():
    # Generate a random date this year
    random_date = fake.date_this_year()

    # Generate a random time
    random_hour = random.randint(0, 23)
    random_minute = random.randint(0, 59)
    random_second = random.randint(0, 59)

    # Combine the date and time into a single datetime string in SQL format
    random_datetime = datetime.combine(random_date, datetime.min.time()) + timedelta(hours=random_hour, minutes=random_minute, seconds=random_second)
    
    # Return as string in SQL DATETIME format
    return random_datetime.strftime('%Y-%m-%d %H:%M:%S')

def generate_teacher():
    first_name = fake.first_name()
    last_name = fake.last_name()
    email = f"{first_name.lower()}.{last_name.lower()}@efrei.net"
    return {
        'first_name': first_name,
        'last_name': last_name,
        'email': email
    }

def generate_student(class_id):
    first_name = fake.first_name()
    last_name = fake.last_name()
    email = f"{first_name.lower()}.{last_name.lower()}@efrei.net"
    return {
        'first_name': first_name,
        'last_name': last_name,
        'email': email
    }

def generate_class_sessions(class_id, subject_id, teacher_id, room_id, existing_sessions, class_sessions_map):
    session_dates = sorted(fake.date_this_year() for _ in range(SESSIONS_PER_SUBJECT))
    new_sessions = []
    for date in session_dates:
        # Convert date to DATETIME format by adding a random time
        session_datetime = generate_random_datetime()
        
        # Check if the current class already has a session on this datetime
        if any(session['class_id'] == class_id and session['session_datetime'] == session_datetime for session in existing_sessions):
            continue  # Skip adding this session, as the class already has one at this time

        # If the room is Visio, we can overlap
        if room_id == NUM_ROOMS:
            new_sessions.append({
                'class_id': class_id,
                'subject_id': subject_id,
                'session_datetime': session_datetime,
                'teacher_id': teacher_id,
                'room_id': room_id
            })
        else:
            # Check if the room and teacher are already booked at the same time
            overlapping = False
            for session in existing_sessions:
                if session['session_datetime'] == session_datetime and session['room_id'] == room_id:
                    overlapping = True
                    break
            # Ensure the class doesn't have more than one session at the same time
            if not overlapping and class_id not in class_sessions_map.get(session_datetime, set()):
                new_sessions.append({
                    'class_id': class_id,
                    'subject_id': subject_id,
                    'session_datetime': session_datetime,
                    'teacher_id': teacher_id,
                    'room_id': room_id
                })
                # Track the datetime for this class
                if session_datetime not in class_sessions_map:
                    class_sessions_map[session_datetime] = set()
                class_sessions_map[session_datetime].add(class_id)
    return new_sessions


def generate_marks(student_id, subject_id):
    return {
        'student_id': student_id,
        'subject_id': subject_id,
        'mark': round(random.uniform(0, 20), 2),
        'coefficient': random.choice([1.0, 1.5, 2.0, 2.5, 3.0])
    }

# Generate SQL data
def generate_sql_data():
    sql_lines = []

    # Insert year (L1 2025)
    sql_lines.append("INSERT INTO years (id, name) VALUES (1, '2025');")

    # Insert rooms (Ensure valid room_id values exist, including a "Visio" room)
    room_id_map = {}
    for i in range(1, NUM_ROOMS + 1):
        room_name = f"Room {i}"
        if i == NUM_ROOMS:
            room_name = "Visio"  # Special Visio room
        room_id_map[i] = room_name
        sql_lines.append(f"INSERT INTO rooms (id, name) VALUES ({i}, '{room_name}');")

    # Insert teachers
    for i in range(1, NUM_TEACHERS + 1):
        teacher = generate_teacher()
        sql_lines.append(f"INSERT INTO teachers (id, first_name, last_name, email) VALUES ({i}, '{teacher['first_name']}', '{teacher['last_name']}', '{teacher['email']}');")

    # Insert classes (INT 1-2, PLUS 1-2)
    class_names = ["INT 1", "INT 2", "PLUS 1", "PLUS 2"]
    for i, class_name in enumerate(class_names, 1):
        sql_lines.append(f"INSERT INTO classes (id, name, year_id) VALUES ({i}, '{class_name}', {YEAR_ID});")

    # Insert modules
    module_id_map = {}
    for i, module in enumerate(MODULES, 1):
        sql_lines.append(f"INSERT INTO modules (id, name, head_id, year_id) VALUES ({i}, '{module}', {random.randint(1, NUM_TEACHERS)}, {YEAR_ID});")
        module_id_map[module] = i  # Store module ID

    # Insert subjects
    subject_id_map = {}
    subject_counter = 1
    for module, subject_list in SUBJECTS.items():
        for subject in subject_list:
            if subject_counter > NUM_SUBJECTS:
                break
            sql_lines.append(f"INSERT INTO subjects (id, name, module_id, teacher_id) VALUES ({subject_counter}, '{subject}', {module_id_map[module]}, {random.randint(1, NUM_TEACHERS)});")
            subject_id_map[subject] = subject_counter  # Store subject ID
            subject_counter += 1

    # Insert students (30-40 per class)
    student_id = 1
    for class_id in range(1, NUM_CLASSES + 1):
        num_students = random.randint(*NUM_STUDENTS_PER_CLASS)
        for _ in range(num_students):
            student = generate_student(class_id)
            sql_lines.append(f"INSERT INTO students (id, first_name, last_name, email, class_id) VALUES ({student_id}, '{student['first_name']}', '{student['last_name']}', '{student['email']}', {class_id});")
            student_id += 1

    # Insert class sessions (3 per subject)
    session_id = 1
    existing_sessions = []
    class_sessions_map = {}  # Track which classes have sessions on each date
    for class_id in range(1, NUM_CLASSES + 1):
        for subject_id in range(1, NUM_SUBJECTS + 1):
            teacher_id = random.randint(1, NUM_TEACHERS)
            room_id = random.randint(1, NUM_ROOMS)  # Ensure valid foreign key
            sessions = generate_class_sessions(class_id, subject_id, teacher_id, room_id, existing_sessions, class_sessions_map)
            for session in sessions:
                sql_lines.append(f"INSERT INTO class_sessions (id, class_id, subject_id, session_date, teacher_id, room_id) VALUES ({session_id}, {session['class_id']}, {session['subject_id']}, '{session['session_datetime']}', {session['teacher_id']}, {session['room_id']});")
                existing_sessions.extend(sessions)
                session_id += 1

    # Insert marks for each student in each subject
    for student_id in range(1, student_id):  # student_id already incremented
        for subject_id in range(1, NUM_SUBJECTS + 1):
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
