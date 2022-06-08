from flask_login import UserMixin
from app import db

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True)
    author = db.Column(db.String(100), index=True)
    photos = db.Column(db.String(254), index=True)
    image = db.Column(db.String(254))
    price = db.Column(db.Integer, index=True)
    
    def __repr__(self) -> str:
        return f'{self.name, self.author, self.price, self.photos}'
    
    
class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True)
    photo = db.Column(db.String(), default='avatar.jpeg')
    
    def __repr__(self) -> str:
        return f'{self.name, self.photo}'


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unique_id = db.Column(db.String())
    username = db.Column(db.String(), index=True)
    email = db.Column(db.String(), index=True)
    profile_pic = db.Column(db.String())
    
    
    def __init__(self, unique_id, username, email, profile_pic):
        self.unique_id = unique_id
        self.username = username
        self.email = email
        self.profile_pic = profile_pic
        
        
    def get_id(self):
        return self.unique_id
    
    def __repr__(self) -> str:
        return f"User {self.username}"