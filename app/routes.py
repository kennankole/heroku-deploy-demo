from flask import Blueprint, render_template


home = Blueprint('home', __name__)

@home.route('/home', methods=['GET', 'POST'])
def home_page():
    return render_template('index.html')


 
    


