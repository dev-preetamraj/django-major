from sqlalchemy import Column, String, Integer, TIMESTAMP, text, ForeignKey
from sqlalchemy.dialects.mysql import TINYINT, LONGTEXT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True)
    email = Column(String(150), unique=True, index=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    password = Column(String(300), nullable=False)
    profile_picture = Column(String(300))
    dob = Column(String(10))
    age = Column(Integer)
    gender = Column(String(10))
    address = Column(LONGTEXT)
    is_hod = Column(TINYINT, server_default=text('0'))
    is_staff = Column(TINYINT, server_default=text('0'))
    is_teacher = Column(TINYINT, server_default=text('0'))
    is_student = Column(TINYINT, server_default=text('0'))
    is_active = Column(TINYINT, server_default=text('1'))
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

class Staff(Base):
    __tablename__ = 'staffs'

    staff_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False, index=True)
    position = Column(String(50), nullable=False)
    education = Column(LONGTEXT)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    user = relationship('User')

class Teacher(Base):
    __tablename__ = 'teachers'

    teacher_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False, index=True)
    position = Column(String(50), nullable=False)
    education = Column(LONGTEXT)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    user = relationship('User')

class HOD(Base):
    __tablename__ = 'hods'

    hod_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False, index=True)
    position = Column(String(50), nullable=False)
    education = Column(LONGTEXT)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    user = relationship('User')

class Student(Base):
    __tablename__ = 'students'

    student_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False, index=True)
    session_under_id = Column(Integer, ForeignKey('session_years.session_id'), index=True)
    courses_id = Column(Integer, ForeignKey('courses.course_id'), index=True)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    user = relationship('User')
    session_year = relationship('SessionYear')
    courses = relationship('Course')

class SessionYear(Base):
    __tablename__ = 'session_years'

    session_id = Column(Integer, primary_key=True, index=True)
    session_start_year = Column(String(12), nullable=False)
    session_end_year = Column(String(12), nullable=False)

class Course(Base):
    __tablename__ = 'courses'

    course_id = Column(Integer, primary_key=True, index=True)
    course_name = Column(String(100), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))