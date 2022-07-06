
from oauthlib.oauth2 import WebApplicationClient
import requests
import json


from flask import redirect, render_template, request, url_for, Blueprint
from flask_login import (
    login_required,
    login_user,
    logout_user
)
from app import db
from app.models import User
from app.config import Config
from app import login_manager
from app.utils import get_google_provider_cfg, authorize_emails

auth = Blueprint('auth', __name__)

client = WebApplicationClient(Config.GOOGLE_CLIENT_ID)


@auth.route('/login', methods=['POST', 'GET'])
def login():
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg['authorization_endpoint']
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)


@auth.route('/login/callback')
def callback():
    code = request.args.get('code')
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]
    
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_reponse = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(Config.GOOGLE_CLIENT_ID, Config.GOOGLE_CLIENT_SECRET),
    )
    client.parse_request_body_response(json.dumps(token_reponse.json()))
    
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)
    
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()['sub']
        users_email = userinfo_response.json()['email']
        picture = userinfo_response.json()['picture']
        users_name = userinfo_response.json()['given_name']
    else:
        return "User email not available or not verified by Google", 400
    user = User(
        unique_id=unique_id, 
        username=users_name,
        email=users_email,
        profile_pic=picture   
    )
    
    if not User.query.filter_by(unique_id=unique_id).first():
        db.session.add(user)
        db.session.commit()
    login_user(
        user,
        force=True,
        remember=True
    )
    return redirect(url_for('auth.account'))


@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('home.home_page'))

@login_required
@auth.route('/account', methods=['GET'])
def account():
    emails = authorize_emails
    return render_template('auth/account.html', emails=emails)
    
 
@login_manager.user_loader
def load_user(user_unique_id):
    return User.query.filter_by(unique_id=user_unique_id).first()

