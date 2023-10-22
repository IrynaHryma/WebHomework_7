from sqlalchemy import func,desc,select,and_

from src.models import Teacher, Student,Subject,Group,Grade
from src.db import session


def select_one():
    """
    Знайти 5 студентів із найбільшим середнім балом з усіх  предметів.
    :return: list[dict]
    
    """

    r = session.query(Student.fullname,
                           func.round(func.avg(Grade.grade), 2).label("avg_grade")\
                            )\
                        .select_from(Grade)\
                        .join(Student)\
                        .group_by(Student.id)\
                        .order_by(desc("avg_grade"))\
                        .limit(5).all()
    return r



def select_two(subject_id):
    """
    Знайти студента із найвищим середнім балом з певного предмета.
    
    """
    
    r = session.query(Subject.name,
                      Student.fullname,
                      func.round(func.avg(Grade.grade), 2).label("avg_grade"))\
        .select_from(Grade)\
        .join(Student)\
        .join(Subject)\
        .filter(Subject.id==subject_id)\
        .group_by(Student.id, Subject.name)\
        .order_by(desc("avg_grade"))\
        .limit(1).all() 

    return r

def select_three(subject_id):
    """
    Знайти середній бал у групах з певного предмета.
    """

    
    r = session.query(Group.name,
                      Subject.name,
                      func.round(func.avg(Grade.grade), 2).label("avg_grade"))\
            .select_from(Grade)\
            .join(Subject,Grade.subject_id==Subject.id)\
            .join(Student,Student.id==Grade.student_id)\
            .join(Group,Group.id== Student.group_id)\
            .filter(Subject.id==subject_id)\
            .group_by(Group.name,Subject.name)\
            .order_by(desc("avg_grade"))\
            .all()
    return r
                      
                      

def select_four():
    """
    Знайти середній бал на потоці (по всій таблиці оцінок).
    """

    r = session.query(func.round(func.avg(Grade.grade), 2).label("avg_grade"))\
            .select_from(Grade).all()      
    return r


def select_five(teacher_id):
    """
    Знайти які курси читає певний викладач.
    
    """
    r = session.query(Teacher.fullname,
                      Subject.name)\
        .join(Subject,Teacher.id == Subject.teacher_id)\
        .filter(Teacher.id==teacher_id)\
        .order_by(Subject.name)\
        .all() 

    return r


def select_six(group_id):
    """
    Знайти список студентів у певній групі.
    
    """
    r = session.query(Student.fullname)\
        .filter(Student.group_id ==group_id)\
        .order_by(Student.fullname)\
        .all()
    return r


def select_seven(group_id):
     """
     Знайти оцінки студентів у окремій групі з певного предмета.
     """

     r = session.query(Subject.name,
                      Student.fullname,
                      Grade.grade)\
        .select_from(Grade)\
        .join(Student, Student.id == Grade.student_id)\
        .join(Subject,Subject.id == Grade.subject_id)\
        .join(Group, Group.id== Student.group_id)\
        .filter(Group.id == group_id)\
        .order_by(Grade.grade.desc())\
        .limit(10)\
        .all() 

     return r


def select_eight(teacher_id):
     """
     Знайти середній бал, який ставить певний викладач зі своїх предметів.
     """

     r = session.query(Teacher.fullname,
                      Subject.name,
                      func.round(func.avg(Grade.grade), 2).label("avg_grade"))\
            .select_from(Grade)\
            .join(Subject, Subject.id == Grade.subject_id)\
            .join(Teacher,Teacher.id == Grade.student_id)\
            .filter(Teacher.id==teacher_id)\
            .group_by(Teacher.fullname,Subject.name)\
            .order_by(desc("avg_grade"))\
            .all()
     return r



def select_nine(student_id):
     """
     Знайти список курсів, які відвідує певний студент.
     """

     r = session.query(Subject.name,
                       Student.fullname)\
        .join(Grade, Grade.student_id == Student.id)\
        .join(Subject,Grade.subject_id == Subject.id)\
        .filter(Student.id == student_id)\
        .group_by(Subject.name,Student.fullname)\
        .order_by(Subject.name)\
        .all() 

     return r


def select_ten(teacher_id,student_id):
    """
    Список курсів, які певному студенту читає певний викладач.
    
    """
   
    r = session.query(Subject.name,
                      Teacher.fullname)\
            .join(Teacher, Teacher.id== Subject.teacher_id)\
            .join(Grade,Grade.subject_id == Subject.id)\
            .filter(Teacher.id==teacher_id,Grade.student_id==student_id)\
            .all()
    return r

    


def select_last(subject_id,group_id):
     subquery =(select(Grade.date_of)).join(Student).join(Group).where(
        and_(Grade.subject_id==subject_id,Group.id==group_id)
     ).order_by(desc(Grade.date_of)).limit(1).scalar_subquery()


     r = session.query(Subject.name,
                      Student.fullname,
                      Group.name,
                      Grade.date_of,
                      Grade.grade
                      ) \
            .select_from(Grade)\
            .join(Student)\
            .join(Subject)\
            .join(Group)\
            .filter(and_(Subject.id==subject_id,Group.id==group_id, Grade.date_of==subquery))\
            .order_by(desc(Grade.date_of))\
            .all() 
     return r

if __name__=="__main__":
    # print(select_one())
    # print (select_two(1))
    # print(select_last(1,1))
    # print(select_three(1))
    # print(select_four())
    # print(select_five(1))
    # print(select_six(1))
    # print(select_seven(1))
    # print(select_eight(1))
    # print(select_nine(1))
    print(select_ten(1,2))