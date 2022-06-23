import os
import boto3
import requests
from werkzeug.utils import secure_filename
from flask import Blueprint, redirect, render_template, flash, request, url_for, send_from_directory
from app.utils import allowed_file, s3_direct_upload
from app import create_app
from app.config import Config

home = Blueprint('home', __name__)

@home.route('/', methods=['GET', 'POST'])
def home_page():
    return render_template('index.html')


@home.route('/school', methods=['GET', 'POST'])
def school():
    return render_template('school.html')

app = create_app()
app.config['UPLOADED_DOC'] = 'static/documents'


@home.route('/articles', methods=['POST', 'GET'])
def upload_articles():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
        file = request.files['file']
        if file.filename == '':
            flash('No file selected')
            return redirect(url_for('home.upload_articles'))
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.root_path, 'static/documents', filename))
        # Upload to s3 bucket.
        # doc_path = os.path.join(app.root_path, 'static/documents', filename)
        # resp = s3_direct_upload(filename)
        # with open(doc_path, 'rb') as doc:
        #     files = {'file': (doc_path, doc)}
        #     reply = requests.post(
        #         resp['url'],
        #         data=resp['fields'],
        #         files=files
        #     )
            return redirect(url_for('home.list_documents'))      
    return render_template('articles.html')



@home.route('/uploaded/files/<name>', methods=['GET', 'POST'])
def uploaded_file(name):
    return send_from_directory(os.path.join(app.root_path, 'static/documents'), name)

@home.route('/documents')
def list_documents():
    docs = os.listdir(os.path.join(app.root_path, 'static/documents'))
    return render_template('articles.html', docs=docs)
    
@home.route('/s3-bucket/uploads', methods=['GET'])
def list_all_uploaded_files():
    s3 = boto3.client('s3')
    contents = []
    for item in s3.list_objects(Bucket=Config.AWS_BUCKET_NAME)['Contents']:
        contents.append(item)
    return render_template('articles.html', contents=contents)


@home.route('/s3-detail/view', methods=['GET'])
def view_s3_files():
    bucket_name = Config.AWS_BUCKET_NAME
    bucket_location = Config.BUCKET_REGION
    return render_template("articles.html", bucket_location=bucket_location,bucket_name=bucket_name)
    
    


