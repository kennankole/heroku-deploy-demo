from app import create_app
from app.config import Config

app = create_app()

if __name__ == '__main__':
    if Config.FLASK_ENV == 'development':
        app.run(ssl_context="adhoc", debug=True)
    else:
        app.run(ssl_context="adhoc", debug=False)
    

# Procfile command gunicorn 
# web: gunicorn wsgi:app

