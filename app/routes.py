from email.mime import image
import os
import secrets
from PIL import Image
from flask import Blueprint, redirect, render_template, request, url_for
from app.forms import AuthorForm, AuthorUpdateForm
from app import models, db, create_app
from werkzeug.utils import secure_filename



home = Blueprint('home', __name__)

@home.route('/', methods=['GET', 'POST'])
def home_page():
    books = models.Author.query.all()
    return render_template('home.html', books=books)


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
        if form.photo.data:
            photo_file = save_photo(form.photo.data)
            book.photo = photo_file
            db.session.add(book)
            db.session.commit()
        return redirect(url_for('home.book_detail', id=book.id))
    elif request.method == 'GET':
        pass 
    return render_template('update.html', form=form, book=book)
    