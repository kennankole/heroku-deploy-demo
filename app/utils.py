import requests
import boto3
from app.config import Config as AppConfig
from botocore.client import Config



acl = 'public-read'
fields = {"acl": acl, "Content-Type":  "application/pdf"}
conditions = [
    {"acl": acl},
    ["starts-with", "$Content-Type", ""]
]

def s3_direct_upload(file_name):
    s3_client = boto3.client(
        's3',
        aws_access_key_id=AppConfig.AWS_ACCESS_ID,
        aws_secret_access_key=AppConfig.AW_SECRET_KEY,
        config=Config(signature_version='s3v4'),
        region_name='eu-central-1' 
    )

    response = s3_client.generate_presigned_post(
                    Bucket=AppConfig.AWS_BUCKET_NAME,
                    Key=file_name,
                    ExpiresIn=3600,
                    Fields=fields,
                    Conditions=conditions
                )
    return response


def list_all_uploaded_files():
    s3 = boto3.client('s3')
    contents = []
    for item in s3.list_objects(Bucket=AppConfig.AWS_BUCKET_NAME)['Contents']:
        contents.append(item)
    return f"All images {contents}"



ALLOWED_EXTENSIONS={'pdf'}

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_google_provider_cfg():
    return requests.get(AppConfig.GOOGLE_DISCOVERY_URL).json()

# from flask import Blueprint, redirect, render_template, request, url_for
# from app.forms import AuthorForm, AuthorUpdateForm
# from app import models, db, create_app

# from app.utils import s3_direct_upload


# from app.config import Config as AppConfig


# def save_photo(picture):
#     app = create_app()
#     try:
#         random_no = secrets.token_hex(8)
#         _, f_ext = os.path.splitext(picture.filename)
#         picture_name = random_no + f_ext 
#         picture_path = os.path.join(app.root_path, 'static/photos', picture_name)
        
#         output_size = (250, 250)
#         i = Image.open(picture)
#         i.thumbnail(output_size)
#         i.save(picture_path)
#         return picture_name
#     except:
#         pass 
#     return 

# @home.route('/create', methods=['GET', 'POST'])
# def create_book():
#     book = models.Author()
#     form = AuthorForm()
#     if form.validate_on_submit():
#         form.populate_obj(book)
#         db.session.add(book)
#         db.session.commit()
#         return redirect(url_for('home.home_page'))
#     return render_template('create.html', form=form)
        
        
# @home.route('/detail/<int:id>/', methods=['GET', 'POST'])
# def book_detail(id):
#     book = models.Author.query.get(id)
#     bucket_name = AppConfig.AWS_BUCKET_NAME
#     bucket_location = AppConfig.BUCKET_REGION
#     return render_template(
#         "detail.html",
#         book=book,
#         bucket_location=bucket_location,
#         bucket_name=bucket_name
#     )
 
# @home.route('/update/<int:id>/', methods=['GET', 'POST'])
# def update_books(id):
#     book = models.Author.query.get(id)
#     form = AuthorUpdateForm()
#     app = create_app()
#     if request.method == 'POST':
#         photo_file = request.files['photo']
#         if photo_file.filename != '':
#             random_no = secrets.token_hex(8)
#             _, f_ext = os.path.splitext(photo_file.filename)
#             picture_name = random_no + f_ext 
#             picture_path = os.path.join(app.root_path, 'static/photos', picture_name)
#             output_size = (250, 250)
#             i = Image.open(photo_file)
#             i.thumbnail(output_size)
#             i.save(picture_path)
            
#             resp = s3_direct_upload(picture_name)
#             #Direct upload to s3
#             with open(picture_path, 'rb') as f:
#                 files = {'file': (picture_path, f)}
#                 r = requests.post(
#                     resp['url'],
#                     data=resp['fields'],
#                     files=files
#                 )
#             book.photo = picture_name
#             db.session.add(book)
#             db.session.commit()
#             print(r.status_code, resp)
#             return redirect(url_for('home.book_detail', id=book.id))
#         else:
#             print(form.errors)
#     return render_template('update.html', form=form, book=book)
    
    
# @home.route('/images', methods=['GET', 'POST'])
