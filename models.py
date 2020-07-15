# -*- coding: <utf-8> -*-
from flask_sqlalchemy import SQLAlchemy
from app import app

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user_info'
    user_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    phone = db.Column(db.String(11),nullable=False)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50),nullable=False)


    __table_args__ = ()


class Book(db.Model):
    __tablename__ = 'book'
    book_url = db.Column(db.String(100),primary_key=True,nullable=False)
    title = db.Column(db.String(100), nullable=False)
    img_url = db.Column(db.String(200),nullable=False)


    __table_args__ = ()



class CSS_Blog(db.Model):
    __tablename__ = 'css_blog'
    url = db.Column(db.String(500),nullable=False)
    title = db.Column(db.String(100),primary_key=True, nullable=False)
    detail_info = db.Column(db.String(500),nullable=False)


class JS_Blog(db.Model):
    __tablename__ = 'js_blog'
    url = db.Column(db.String(500),nullable=False)
    title = db.Column(db.String(100),primary_key=True,nullable=False)
    detail_info = db.Column(db.String(500),nullable=False)


class Vue_Blog(db.Model):
    __tablename__ = 'vue_blog'
    url = db.Column(db.String(500),nullable=False)
    title = db.Column(db.String(100),primary_key=True, nullable=False)
    detail_info = db.Column(db.String(500),nullable=False)


class React_Blog(db.Model):
    __tablename__ = 'react_blog'
    url = db.Column(db.String(500),nullable=False)
    title = db.Column(db.String(100),primary_key=True, nullable=False)
    detail_info = db.Column(db.String(500),nullable=False)

class Python_Base_Blog(db.Model):
    __tablename__ = 'python_base_blog'
    url = db.Column(db.String(500),nullable=False)
    title = db.Column(db.String(100),primary_key=True, nullable=False)
    detail_info = db.Column(db.String(500),nullable=False)



class Spider_Blog(db.Model):
    __tablename__ = 'spider_blog'
    url = db.Column(db.String(500),nullable=False)
    title = db.Column(db.String(100),primary_key=True, nullable=False)
    detail_info = db.Column(db.String(500),nullable=False)


class Flask_Blog(db.Model):
    __tablename__ = 'flask_blog'
    url = db.Column(db.String(500),nullable=False)
    title = db.Column(db.String(100),primary_key=True, nullable=False)
    detail_info = db.Column(db.String(500),nullable=False)


class AI_Blog(db.Model):
    __tablename__ = 'ai_blog'
    url = db.Column(db.String(500),nullable=False)
    title = db.Column(db.String(100),primary_key=True, nullable=False)
    detail_info = db.Column(db.String(500),nullable=False)


class MySQL_Blog(db.Model):
    __tablename__ = 'mysql_blog'
    url = db.Column(db.String(500),nullable=False)
    title = db.Column(db.String(100),primary_key=True, nullable=False)
    detail_info = db.Column(db.String(500),nullable=False)


class Redis_Blog(db.Model):
    __tablename__ = 'redis_blog'
    url = db.Column(db.String(500),nullable=False)
    title = db.Column(db.String(100),primary_key=True, nullable=False)
    detail_info = db.Column(db.String(500),nullable=False)


if __name__ == '__main__':
    db.create_all(app=app)
    # db.drop_all(app=app)

