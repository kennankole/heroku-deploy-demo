from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run()

#Procfile command gunicorn 
#web: gunicorn wsgi:app

