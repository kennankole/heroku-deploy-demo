from flask import Blueprint, render_template, redirect

school = Blueprint('school', __name__)

@school.route('/school/home')
def school_home():
    return render_template('school/home.html')