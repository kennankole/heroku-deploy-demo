from cmath import exp
import json
import os
import secrets
from PIL import Image
import boto3
from botocore.exceptions import ClientError
from flask import Blueprint, redirect, render_template, request, url_for
from app.forms import AuthorForm, AuthorUpdateForm
from app import models, db, create_app
from werkzeug.utils import secure_filename

from app.config import Config


home = Blueprint('home', __name__)

@home.route('/', methods=['GET', 'POST'])
def home_page():
    try:
        books = models.Author.query.all()
        return render_template('home.html', books=books)
    except:
        return "No Authors!!"


def save_photo(picture):
    app = create_app()
    try:
        random_no = secrets.token_hex(8)
        _, f_ext = os.path.splitext(picture.filename)
        picture_name = random_no + f_ext 
        picture_path = os.path.join(app.root_path, 'static/photos', picture_name)
        
        output_size = (250, 250)
        i = Image.open(picture)
        i.thumbnail(output_size)
        i.save(picture_path)
        return picture_name
    except:
        pass 
    return

@home.route('/create', methods=['GET', 'POST'])
def create_book():
    book = models.Author()
    form = AuthorForm()
    if form.validate_on_submit():
        form.populate_obj(book)
        db.session.add(book)
        db.session.commit()
        return redirect(url_for('home.home_page'))
    return render_template('create.html', form=form)
        
        
@home.route('/detail/<int:id>/', methods=['GET', 'POST'])
def book_detail(id):
    book = models.Author.query.get(id)
    return render_template('detail.html', book=book)
 
@home.route('/update/<int:id>/', methods=['GET', 'POST'])
def update_books(id):
    book = models.Author.query.get(id)
    form = AuthorUpdateForm()
    if form.validate_on_submit():
        app = create_app()
        if form.photo.data:
            photo_file = save_photo(form.photo.data)
            image_name = os.path.join(app.root_path, 'static/photos', photo_file)
            s3_client = boto3.client('s3')
            response = s3_client.upload_file(image_name, Config.AWS_BUCKET_NAME, photo_file)
            book.photo = photo_file
            db.session.add(book)
            db.session.commit()
            print(response)
        return redirect(url_for('home.book_detail', id=book.id))
    elif request.method == 'GET':
        pass 
    return render_template('update.html', form=form, book=book)
    
    
@home.route('/images', methods=['GET', 'POST'])
def list_all_uploaded_files():
    s3 = boto3.client('s3')
    contents = []
    for item in s3.list_objects(Bucket=Config.AWS_BUCKET_NAME)['Contents']:
        contents.append(item)
    return f"All images {contents}"


@home.route('/sign_s3')
def sign_s3():
    S3_BUCKET = Config.AWS_BUCKET_NAME
    
    file_name = request.args.get('file_name')
    file_type = request.args.get('file_type')
    #the AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY set in heroku CLI 
    # are automatically read from the environment.
    s3 = boto3.client('s3')
    
    # The pre-signed POST request data is then generated using 
    # the generate_presigned_post function.
    presigned_post = s3.generate_presigned_post(
        Bucket = S3_BUCKET,
        Key = file_name,
        Fields = {'acl': 'public-read', "Content-Type":file_type},
        Conditions = [
            {'acl':'public-read'},
            {'Content-Type': file_type}
        ],
        ExpiresIn = 3600 # seconds
    )
    
    # The pre-signed request data and the location of 
    # the eventual file on S3 are returned to the client as JSON.
    return json.dumps({
        'data': presigned_post, 
        'url':'https://%s.s3.amazonaws.com/%s' % (S3_BUCKET, file_name)
    })
    

def update_profile(username, avatar_url):
    if request.method == 'POST':
        avatar_url = request.files['avatar-url']
        if avatar_url.filename != '':
            save_photo(avatar_url)
            new_user = models.Author(
                name=username,
                photo=avatar_url.filename
            )
            db.session.add(new_user)
            db.session.commit()
        return
    return
 
@home.route("/submit-form", methods=['POST'])
def submit_form():
    username = request.form['username']
    avatar_url = request.form['avatar-url']
    
    update_profile(username, avatar_url)
    return redirect(url_for('home.home_page'))