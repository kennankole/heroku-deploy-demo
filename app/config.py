import os

class Config:
    FLASK_ENV = os.getenv('FLASK_ENV')
    FLASK_APP = os.getenv('FLASK_APP')
    SECRET_KEY = os.getenv('SECRET_KEY') or "qwerty1234567890"
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI') or "postgresql://vugibyuzfknulz:f693d14fed9a1d975df923280fd878dea9d261a4c1dc40ea304e84ce2ac93845@ec2-34-230-153-41.compute-1.amazonaws.com:5432/dbdh3og7qq27er"