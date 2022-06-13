import os
from pickle import TRUE
from re import T
from dotenv import load_dotenv

load_dotenv()
class Config:
    FLASK_ENV = os.getenv('FLASK_ENV')
    FLASK_APP = os.getenv('FLASK_APP')
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    AW_SECRET_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_ACCESS_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')
    BUCKET_REGION = os.getenv("BUCKET_REGION")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
    GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"

    # https://127.0.0.1:5000
    # https://127.0.0.1:5000/login/callback

class Development(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:////tmp/book.db"
    
  
class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = True
    
    
    
