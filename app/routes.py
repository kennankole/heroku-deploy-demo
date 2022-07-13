import os
from werkzeug.utils import secure_filename
from flask import Blueprint, redirect, render_template, flash, request, url_for, send_from_directory
from preview_generator.manager import PreviewManager

from flask_login import login_required, current_user

from app.utils import (
    allowed_file, save_photo, 
    authorize_emails, s3_pdf_file_upload, s3_pdf_thumbnail_file_upload,
    pdf_thumbnail
)

from app import create_app, db
from app.config import Config
from app.models import Document, User

home = Blueprint('home', __name__)
app = create_app()


@home.route('/', methods=['GET', 'POST'])
def home_page():
    email = authorize_emails
    return render_template('base.html', email=email)

@home.route('/support', methods=['GET'])
def support():
    return render_template('support.html')

@home.route('/school', methods=['GET', 'POST'])
def school():
    return render_template('school.html')


@login_required
@home.route('/articles/<int:id>/', methods=['POST', 'GET'])
def upload_articles(id):
    if current_user.email in authorize_emails:
        user = User.query.filter_by(id=id).first()
        if request.method == 'POST':
            if 'file' not in request.files:
                flash('No file part')
            file = request.files['file']
            name = request.form['name']
            if file.filename == '':
                flash('No file selected')
                return redirect(url_for('home.upload_articles'))
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # save the Uploaded file
                file.save(os.path.join(app.root_path, 'static/documents', filename))
                #Generate a thumbnail from the PDF
                file_thumbnail = pdf_thumbnail(filename)
                image_name = file_thumbnail.split('/')
                #Save the generated thumbnail
                thumbnail_path = save_photo(file_thumbnail)
            

                new_article = Document(
                    title=name,
                    pdf_file=filename,
                    pdf_thumbnail=thumbnail_path,
                    author=user.unique_id
                )
                db.session.add(new_article)
                db.session.commit()
                
            # Upload pdf file to s3 bucket.
            doc_path = os.path.join(app.root_path, 'static/documents', filename)
            s3_pdf_file_upload(path=doc_path, filename=filename)
            
            # Upload pdf thumbnail to s3
            picture_path = os.path.join(app.root_path, 'static/photos', file_thumbnail)
            s3_pdf_thumbnail_file_upload(path=picture_path, filename=image_name[-1])
            
            
            return redirect(url_for('home.list_documents'))  
        return render_template('articles.html')
    else:
        return render_template('upload_404.html')


@home.route('/uploaded/files/<name>', methods=['GET', 'POST'])
def uploaded_file(name):
    return send_from_directory(os.path.join(app.root_path, 'static/documents'), name)

@home.route('/documents', methods=['GET', 'POST'])
def list_documents():
    docs = Document.query.all()
    emails = authorize_emails
    return render_template('article_list.html', docs=docs, emails=emails)

# @home.route('/s3-detail/view', methods=['GET'])
# def view_s3_files():
#     bucket_name = Config.AWS_BUCKET_NAME
#     bucket_location = Config.BUCKET_REGION
#     return render_template("articles.html", bucket_location=bucket_location,bucket_name=bucket_name)
    
    


