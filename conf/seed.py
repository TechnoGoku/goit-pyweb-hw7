import logging

from faker import Faker
import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Group, Student, Teacher, Subject, Grade

# import psycopg2
# from psycopg2 import DatabaseError


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

fake = Faker("uk_UA")

engine = create_engine('postgresql+psycopg2://postgres:567234@localhost@localhost/test')
Session = sessionmaker(bind=engine)
session = Session()


for _ in range(3):
    cur.execute("INSERT INTO groups (name) VALUES (%s)", (fake.word(),))

for _ in range(3):
    cur.execute("INSERT INTO teachers (fullname) VALUES (%s)", (fake.name(),))

for teacher_id in range(1, 4):
    for _ in range(2):
        cur.execute("INSERT INTO subjects (name, teacher_id) VALUES (%s, %s)", (fake.word(), teacher_id))

for group_id in range(1, 4):
    for _ in range(10):
        cur.execute("INSERT INTO students (fullname, group_id) VALUES (%s, %s) RETURNING id", (fake.name(), group_id))
        student_id = cur.fetchone()[0]
        for subject_id in range(1, 7):
            for _ in range(3):
                cur.execute("INSERT INTO grades (student_id, subject_id, grade, grade_date) VALUES (%s, %s, %s, %s)",
                            (student_id, subject_id, random.randint(0, 100), fake.date_this_decade()))

try:
    conn.commit()
except DatabaseError as err:
    logging.error(err)
    conn.rollback()
finally:
    cur.close()
    conn.close()
