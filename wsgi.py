from app import create_app
from flask_talisman import Talisman

app = create_app()


# Talisman(app, content_security_policy=None)
if __name__ == '__main__':
    app.run(debug=True)
    # if app.config["ENV"] == "development":
    #     app.run()
    # else:
    #     app.run()
    
# ssl_context="adhoc",
# Procfile command gunicorn 
# web: gunicorn wsgi:app

