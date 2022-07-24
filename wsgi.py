from matplotlib.style import context
from app import create_app
from flask_talisman import Talisman
from app.config import Config
import exiftool

app = create_app()

# Talisman(app, content_security_policy=None)
if __name__ == '__main__':
    # Talisman(app, content_security_policy=None)
    app.run(ssl_context="adhoc")
    # # app.run(debug=True)
    # if Config.FLASK_ENV == "development":
    #     print("development")
    #     # Talisman(app, content_security_policy=None)
    #     app.run(ssl_context="adhoc", debug=True, host='0.0.0.0', port=443) #docker https 
    #     # Talisman(app, content_security_policy=None)
    #     # app.run(ssl_context="adhoc")
    # else:
    #     Talisman(app, content_security_policy=None)
    #     app.run(ssl_context="adhoc", debug=False)
    
# ssl_context="adhoc",
# Procfile command gunicorn 
# web: gunicorn wsgi:app

