from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    if app.config['ENV'] == 'development':
        app.config.from_object('app.config.Development')
    else:
        app.config.from_object('app.config.Config')
    db.init_app(app)
    with app.app_context():
        from app.routes import home 
        from app.auth.routes import auth
        app.register_blueprint(home)
        app.register_blueprint(auth)
        if app.config['ENV'] == 'development':
            db.create_all()
        migrate.init_app(app, db, render_as_batch=True)
        
        login_manager.init_app(app)
        
    return app