import os
import requests
import secrets
from PIL import Image
import boto3
from app.config import Config as AppConfig
from botocore.config import Config
from app import create_app
from preview_generator.manager import PreviewManager

MYDIR = os.path.dirname(__file__)

authorize_emails = [
    'kennankole@gmail.com'
]

def list_all_uploaded_files():
    s3 = boto3.client('s3')
    contents = []
    for item in s3.list_objects(Bucket=os.getenv('AWS_BUCKET_NAME'))['Contents']:
        contents.append(item)
    return f"All images {contents}"



ALLOWED_EXTENSIONS={'pdf'}

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_google_provider_cfg():
    return requests.get(AppConfig.GOOGLE_DISCOVERY_URL).json()


def save_photo(picture):
    app = create_app()
    
    random_no = secrets.token_hex(8)
    _, f_ext = os.path.splitext(picture)
    picture_name = random_no + f_ext 
    picture_path = os.path.join(MYDIR, 'static/photos', picture_name)
    
    output_size = (250, 250)
    i = Image.open(picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_name
    
    
# @home.route('/detail/<int:id>/', methods=['GET', 'POST'])
# def book_detail(id):
#     book = models.Author.query.get(id)
#     bucket_name = os.getenv('AWS_BUCKET_NAME')
#     bucket_location = os.getenv('BUCKET_REGION
#')     return render_template(
#         "detail.html",
#         book=book,
#         bucket_location=bucket_location,
#         bucket_name=bucket_name
#     )
 


def s3_pdf_file_upload(path, filename):
    s3_client = boto3.client(
        's3',
        aws_access_key_id=AppConfig.AWS_ACCESS_ID,
        aws_secret_access_key=AppConfig.AW_SECRET_KEY,
        config=Config(signature_version='s3v4'),
        region_name='eu-central-1'
    )
    
    response = s3_client.generate_presigned_post(
    Bucket=AppConfig.AWS_BUCKET_NAME,
    Key=filename,
    ExpiresIn=3600,
    Fields={"acl": 'public-read', "Content-Type": "application/pdf"},
    Conditions=[
            {"acl": 'public-read'},
            ["starts-with", "$Content-Type", ""]
    ]
    )

    with open(path, 'rb') as f:
        files = {'file': (path, f)}
        http_response = requests.post(response['url'], data=response['fields'], files=files)

    return http_response


def s3_pdf_thumbnail_file_upload(path, filename):
    s3_client = boto3.client(
        's3',
        aws_access_key_id=AppConfig.AWS_ACCESS_ID,
        aws_secret_access_key=AppConfig.AW_SECRET_KEY,
        config=Config(signature_version='s3v4'),
        region_name='eu-central-1'
    )
    
    response = s3_client.generate_presigned_post(
    Bucket=AppConfig.AWS_BUCKET_NAME,
    Key=filename,
    ExpiresIn=3600,
    Fields={"acl": 'public-read', "Content-Type": "image/jpeg"},
    Conditions=[
            {"acl": 'public-read'},
            ["starts-with", "$Content-Type", ""]
    ]
    )
    with open(path, 'rb') as f:
        files = {'file': (path, f)}
        http_response = requests.post(response['url'], data=response['fields'], files=files)

    return http_response


def pdf_thumbnail(pdf_name):
    app = create_app()
    cache_path = os.path.join(MYDIR, "static/docs/thumbnails")
    thumbnail_preview_path = os.path.join(MYDIR, "static/docs/"+ pdf_name)
    manager = PreviewManager(cache_path, create_folder=True)
    pdf_to_preview_path = manager.get_jpeg_preview(thumbnail_preview_path)
    return pdf_to_preview_path

