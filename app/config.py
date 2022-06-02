import os
from dotenv import load_dotenv

load_dotenv()
class Config:
    FLASK_ENV = os.getenv('FLASK_ENV')
    FLASK_APP = os.getenv('FLASK_APP')
    SECRET_KEY = os.getenv('SECRET_KEY') or "qwerty1234567890"
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    # postgresql://vugibyuzfknulz:f693d14fed9a1d975df923280fd878dea9d261a4c1dc40ea304e84ce2ac93845@ec2-34-230-153-41.compute-1.amazonaws.com:5432/dbdh3og7qq27er"
    AW_SECRET_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_ACCESS_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_BUCKET_NAME = os.getenv('BUCKET_NAME')
    BUCKET_REGION = os.getenv("BUCKET_REGION")
    
    
class Development(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:////tmp/book.db" 
    #"postgresql://vugibyuzfknulz:f693d14fed9a1d975df923280fd878dea9d261a4c1dc40ea304e84ce2ac93845@ec2-34-230-153-41.compute-1.amazonaws.com:5432/dbdh3og7qq27er"