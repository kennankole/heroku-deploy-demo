from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
db = SQLAlchemy()

migrate = Migrate()

def create_app():
    app = Flask(__name__)
    
    app.config.from_object('app.config.Config')
    db.init_app(app)
    
    with app.app_context():
        from app.routes import home 
        app.register_blueprint(home)
        db.create_all()
        migrate.init_app(app, db, render_as_batch=True)
        
    return app