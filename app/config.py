import os

class Config:
    FLASK_ENV = os.getenv('FLASK_ENV')
    FLASK_APP = os.getenv('FLASK_APP')
    SECRET_KEY = os.getenv('SECRET_KEY') or "qwerty1234567890"
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI') or "sqlite:////tmp/book.db"