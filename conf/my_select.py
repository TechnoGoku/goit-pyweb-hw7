from sqlalchemy import func, desc, select, and_, create_engine
from sqlalchemy.orm import sessionmaker
from conf.models import Base, Grade, Group, Teacher, Student, Subject
from conf.db import session

engine = create_engine('postgresql://postgres:567234@localhost/test', client_encoding='utf8')
Session = sessionmaker(bind=engine)
session = Session()


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
    """
    SELECT
        AVG(grade) AS average_grade
    FROM
        grades;

    """
    result = session.query(func.avg(Grade.grade).label('average_grade')).scalar()
    return result


def select_05():
    """
    SELECT
    subjects.name AS subject_name
FROM
    subjects
JOIN
    teachers ON subjects.teacher_id = teachers. id
WHERE
    teachers.id = 1;
    """
    result = session.query(Subject.name).join(Teacher, Subject.teacher_id == Teacher.id).filter(Teacher.id == 1).all()
    return result


def select_06(group_id=None):
    """
    SELECT
        students.id,
        students.fullname
    FROM
        students
    WHERE
        students.group_id = 2;  -- Замените 1 на нужный id группы

    """
    result = session.query(Student.id, Student.fullname).filter(Student.group_id == group_id).all()
    return result


def select_07():
    """
    SELECT
        students.fullname AS student_name,
        grades.grade,
        grades.grade_date
    FROM
        grades
    JOIN
        students ON grades.student_id = students.id
    JOIN
        subjects ON grades.subject_id = subjects.id
    JOIN
        groups ON students.group_id = groups.id
    WHERE
        groups.id = 1
        AND subjects.id = 1;
    """
    result = session.query(Student.fullname.label("student_name"),
                           Grade.grade,
                           Grade.grade_date) \
        .join(Grade, Student.id == Grade.student_id) \
        .join(Subject, Grade.subjects_id == Subject.id) \
        .join(Group, Student.group_id == Group.id) \
        .filter(Group.id == 1) \
        .filter(Subject.id == 1).all()
    return result


def select_08():
    """
    SELECT
        AVG(grades.grade) AS average_grade
    FROM
        grades
    JOIN
        subjects ON grades.subject_id = subjects.id
    JOIN
        teachers ON subjects.teacher_id = teachers.id
    WHERE
        teachers.id = 1;  -- Замените 1 на нужный id преподавателя
    """
    result = session.query(func.avg(Grade.grade).label('average_grade')) \
        .join(Subject, Grade.subjects_id == Subject.id) \
        .join(Teacher, Subject.teacher_id == Teacher.id) \
        .filter(Teacher.id == 1).scalar()
    return result


def select_09():
    """
    SELECT
        subjects.name AS subject_name
    FROM
        grades
    JOIN
        subjects ON grades.subject_id = subjects.id
    JOIN
        students ON grades.student_id = students.id
    WHERE
        students.id = 1;  -- Замените 1 на нужный id студента
    """
    result = session.query(Subject.name) \
        .join(Grade, Subject.id == Grade.subjects_id) \
        .join(Student, Grade.student_id == Student.id) \
        .filter(Student.id == 1).all()
    return result


def select_10():
    """
    SELECT
        subjects.name AS subject_name
    FROM
        grades
    JOIN
        subjects ON grades.subject_id = subjects.id
    JOIN
        students ON grades.student_id = students.id
    JOIN
        teachers ON subjects.teacher_id = teachers.id
    WHERE
        students.id = 1  -- Замените 1 на нужный id студента
        AND teachers.id = 2;  -- Замените 2 на нужный id преподавателя
    """




if __name__ == '__main__':
    print(f"query_1: {select_01()}")
    print('---------------')
    print(f"query_2: {select_02()}")
    print('---------------')
    print(f"query_3: {select_03()}")
    print('---------------')
    print(f"query_4: {select_04()}")
    print('---------------')
    print(f"query_5: {select_05()}")
    print('---------------')
    print(f"query_6: {select_06(2)}")  # введіть id групи
    print('---------------')
    print(f"query_7: {select_07()}")
    print('---------------')
    print(f"query_8: {select_08()}")
    print('---------------')
    print(f"query_9: {select_09()}")
    print('---------------')
    print(f"query_10: {select_10()}")
