from sqlalchemy import func, desc, select, and_, create_engine
from sqlalchemy.orm import sessionmaker
from conf.models import Base, Grade, Group, Teacher, Student, Subject
from conf.db import session

engine = create_engine('postgresql://postgres:567234@localhost/test', client_encoding='utf8')
Session = sessionmaker(bind=engine)
session = Session()

# Проверка существования предмета с id=1
# subject_exists = session.query(Subject).filter(Subject.id == 1).first()
# if subject_exists:
#     print(f"Subject with id=1 exists: {subject_exists.name}")
# else:
#     print("Subject with id=1 does not exist")
#
# # Проверка наличия оценок по предмету с id=1
# grades_for_subject = session.query(Grade).filter(Grade.subjects_id == 1).count()
# print(f"Number of grades for subject with id=1: {grades_for_subject}")
#
# # Проверка существования групп, у которых студенты имеют оценки по предмету с id=1
# groups_with_grades_for_subject = session.query(Group.name, func.avg(Grade.grade)).join(Student).join(Grade).filter(
#     Grade.subject_id == 1).group_by(Group.name).all()
# print(f"Groups with grades for subject with id=1: {groups_with_grades_for_subject}")


def select_01():
    """
    SELECT
        s.id,
        s.fullname,
        ROUND(AVG(g.grade), 2) AS average_grade
    FROM students s
    JOIN grades g ON s.id = g.student_id
    GROUP BY s.id
    ORDER BY average_grade DESC
    LIMIT 5;
    """
    result = session.query(Student.id, Student.fullname, func.round(func.avg(Grade.grade), 2).label('average_grade')) \
        .select_from(Student).join(Grade).group_by(Student.id).order_by(desc('average_grade')).limit(5).all()
    return result


def select_02():
    """
    SELECT
        s.id,
        s.fullname,
        ROUND(AVG(g.grade), 2) AS average_grade
    FROM grades g
    JOIN students s ON s.id = g.student_id
    where g.subject_id = 1
    GROUP BY s.id
    ORDER BY average_grade DESC
    LIMIT 1;
    """
    result = session.query(Student.id, Student.fullname, func.round(func.avg(Grade.grade), 2).label('average_grade')) \
        .select_from(Grade).join(Student).filter(Grade.subjects_id == 1).group_by(Student.id) \
        .order_by(desc('average_grade')).limit(1).all()
    return result


def select_03():
    """
    SELECT
        groups.name AS group_name,
        AVG(grades.grade) AS average_grade
    FROM
        grades
    JOIN
        students ON grades.student_id = students.id
    JOIN
        groups ON students.group_id = groups.id
    JOIN
        subjects ON grades.subject_id = subjects.id
    WHERE
        subjects.id = 1
    GROUP BY
        groups.name;

    """
    result = session.query(Group.name.label("group_name"),
                           func.avg(Grade.grade).label("average_grade")
                           ).select_from(Grade).join(Student, Student.id == Grade.student_id) \
        .join(Group, Group.id == Student.group_id) \
        .join(Subject, Subject.id == Grade.subjects_id) \
        .filter(Subject.id == 1) \
        .group_by(Group.name) \
        .all()
    return result


def select_04():
    pass


if __name__ == '__main__':
    print(select_01())
    print('---------------')
    print(select_02())
    print('---------------')
    print(select_03())
