import enum
from datetime import date
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from . import db


class UserRole(enum.Enum):
    TEACHER = "teacher"
    STUDENT = "student"


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.Enum(UserRole), default=UserRole.STUDENT, nullable=False)
    assignments = db.relationship('Assignment', backref='user', lazy='select')


class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    test_code = db.Column(db.Text, nullable=False)
    assignments = db.relationship('Assignment', backref='task', lazy='select')


class AssignmentState(enum.Enum):
    ISSUED = 'issued'
    REISSUED = 'reissued'
    FINISHED = 'finished'
    EXPIRED = 'expired'


class Assignment(db.Model):
    __tablename__ = 'assignments'
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    state = db.Column(db.Enum(AssignmentState), default=AssignmentState.ISSUED, nullable=False)
    issued = db.Column(db.Date, default=date.today)
    deadline = db.Column(db.Date)
    answer_code = db.Column(db.Text)
    tests_result = db.Column(db.Text)
    grade = db.Column(db.String(10))
    teacher_comment = db.Column(db.Text)
