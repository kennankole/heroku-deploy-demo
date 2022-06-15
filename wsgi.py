from app import create_app
from flask_talisman import Talisman
from app.config import Config

app = create_app()


# Talisman(app, content_security_policy=None)
if __name__ == '__main__':
    # app.run(debug=True)
    if Config.FLASK_ENV == "development":
        app.run(ssl_context="adhoc", debug=True)
    else:
        Talisman(app, content_security_policy=None)
        app.run(ssl_context="adhoc", debug=False)
    
# ssl_context="adhoc",
# Procfile command gunicorn 
# web: gunicorn wsgi:app

