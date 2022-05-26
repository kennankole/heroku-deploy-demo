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
    
