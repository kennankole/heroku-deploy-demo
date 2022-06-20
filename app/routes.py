from flask import Blueprint, render_template


home = Blueprint('home', __name__)

@home.route('/', methods=['GET', 'POST'])
def home_page():
    return render_template('index.html')


@home.route('/school', methods=['GET', 'POST'])
def school():
    return render_template('school.html')

 
    


