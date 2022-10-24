from flask import Blueprint, request

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return '<p>login<p>'

@auth.route('/logout')
def logout():
    return '<p>logout<p>'

@auth.route('/sign-up')
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = request.form.get('user')
    return '<p>sign-up<p>'