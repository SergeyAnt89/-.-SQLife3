import sqlite3
from pprint import pprint

con = sqlite3.connect('students.db')
cursor = con.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS students(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    age INTEGER)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS grades(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id INTEGER,
                    subject TEXT,
                    grade FLOAT,
                    FOREIGN KEY (student_id) REFERENCES students(id))''')
con.commit()

class University:
    def __init__(self, name):
        self.name = name
        self.conn = sqlite3.connect('students.db')
        self.cur = self.conn.cursor()

    def add_student(self, name: str, age: int):
        sql = (f"INSERT INTO students (name, age) "
               f"VALUES ('{name}', {age})")
        self.cur.execute(sql)
        id_student = self.cur.lastrowid
        self.conn.commit()
        return id_student

    def add_grade(self, student_id: int, subject: str, grade: float):

        sql = (f"INSERT INTO grades (student_id, subject, grade) "
               f"VALUES ({student_id}, '{subject}', {grade})")
        self.cur.execute(sql)
        self.conn.commit()

    def get_students(self, subject=None):

        if subject:
            self.cur.execute('SELECT s.name, s.age, g.subject, g.grade '
                             'FROM students s, grades g '
                             'WHERE s.id = g.student_id AND g.subject = ?', (subject,))
        else:
            self.cur.execute('SELECT s.name, s.age, g.subject, g.grade '
                             'FROM students s, grades g '
                             'WHERE s.id = g.student_id')
        return self.cur.fetchall()


u1 = University('Urban')
u1.add_student('Сергей', 24)
u1.add_student('Дмитрий', 22)
u1.add_student('Светлана', 21)
u1.add_student('Ольга', 21)
u1.add_grade(1, 'Python', 3)
u1.add_grade(1, 'PHP', 5)
u1.add_grade(2, 'Python', 4)
u1.add_grade(2, 'PHP', 5)
u1.add_grade(3, 'Python', 5)
u1.add_grade(3, 'PHP', 3)
u1.add_grade(4, 'Python', 4)
u1.add_grade(4, 'PHP', 3)
pprint(u1.get_students())
pprint(u1.get_students('Python'))