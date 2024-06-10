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
    group = Group(name=fake.word())
    session.add(group)

for _ in range(3):
    teacher = Teacher(fullname=fake.name())
    session.add(teacher)

session.commit()

teachers = session.query(Teacher).all()
groups = session.query(Group).all()

for teacher in teachers:
    for _ in range(2):
        subjects = Subject(name=fake.word(), teacher_id=teacher.id)
        session.add(subjects)

session.commit()

subjects = session.query(Subject).all()

for group in groups:
    for _ in range(10):
        student = Student(fullname=fake.name(), group_id=group.id)
        session.add(student)
        session.commit()
        for subject in subjects):
            for _ in range(3):
                grade = Grade(student_id=student.id, subjects_id = subjects.id, grade=random.randint(0, 100), grade_date = fake.date_this_decade()


try:
    conn.commit()
except DatabaseError as err:
    logging.error(err)
    conn.rollback()
finally:
    cur.close()
    conn.close()
