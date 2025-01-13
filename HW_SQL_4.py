import os
import sqlite3

if os.path.exists("HW_SQL_4.db"):
    os.remove("HW_SQL_4.db")
else:
    print("The file does not exist")

conn = sqlite3.connect('HW_SQL_4.db')

conn.row_factory = sqlite3.Row

cursor = conn.cursor()
""".1 כתוב שאילתות SQL ליצירת 3 הטבלאות )יש להשתמש ב Autoincrement )"""

cursor.execute('CREATE TABLE courses(\
   course_id INTEGER PRIMARY KEY AUTOINCREMENT ,\
   topic TEXT ,\
   hours INT\
);')

cursor.execute('CREATE TABLE students(\
   student_id INTEGER PRIMARY KEY AUTOINCREMENT,\
   name TEXT ,\
   email UNIQUE\
);')

cursor.execute('CREATE TABLE grades (\
    student_id INTEGER NOT NULL,\
    course_id INTEGER NOT NULL,\
    grade INTEGER ,\
	PRIMARY KEY(student_id,course_id)\
	FOREIGN KEY (student_id) REFERENCES students(student_id)\
	FOREIGN KEY (course_id) REFERENCES courses(course_id)\
);')

""".2 כתוב שאילתות SQL להוספת 2 קורסים(או יותר)"""

cursor.execute("INSERT into courses (topic,hours)VALUES('Python','2');")
cursor.execute("INSERT into courses (topic,hours)VALUES('SQLite','3');")

"""כתוב שאילתות SQL להוספת הוספת 2 תלמידים (או יותר)"""

cursor.execute("INSERT into students (name,email)VALUES('Rebecca','Rebecca123@gmail.com');")
cursor.execute("INSERT into students (name,email)VALUES('Lior','Lior123@gmail.com');")

"""כעת כתוב שאילתות SQL להוספת ציון לכל תלמיד לכל אחד מהקורסים"""

cursor.execute("INSERT INTO grades (student_id, course_id,grade) VALUES (1, 1, 100);")
cursor.execute("INSERT INTO grades (student_id, course_id,grade) VALUES (1, 2, 97);")
cursor.execute("INSERT INTO grades (student_id, course_id,grade) VALUES (2, 1, 78);")
cursor.execute("INSERT INTO grades (student_id, course_id,grade) VALUES (2, 2, 100);")

""".3 כתוב שאילתת SQL המחשבת את ממוצע הציונים לכל קורס בנפרד"""

cursor.execute("SELECT c.topic AS course_name,\
    AVG(g.grade) AS average_grade\
    FROM grades g\
    JOIN courses c ON g.course_id = c.course_id\
    GROUP BY c.topic;")

rows = cursor.fetchall()
for row in rows:
    print(tuple(row))

""".4 כתוב קוד בפייטון המציג את כל הקורסים"""

cursor.execute("SELECT * FROM courses")
courses = cursor.fetchall()
for course in courses:
    print(tuple(course))

""".5 כתוב קוד בפייטון הקולט מהמשתמש את נושא הקורס + מס' שעות,
ומוסיף אותו לטבלת הקורסים
*בונוס/אתגר- לפני הוספת הקורס בדוק קודם אם קיים כבר קורס באותו הנושא. אם אכן
קיים קורס שכזה, אז הדפס הודעת שגיאה ואל תוסיף את הקורס"""

course_name = input('enter a course name')
course_hour = int(input('enter course hour'))
for row in courses:
    if course_name in row:
        print('This course already exists')
        break
    else:
        cursor.execute("INSERT into courses (topic,hours) VALUES (?,?)", (course_name, course_hour))
        conn.commit()
        break

cursor.execute("SELECT * FROM courses")
courses = cursor.fetchall()
for course in courses:
    print(tuple(course))

conn.close()
