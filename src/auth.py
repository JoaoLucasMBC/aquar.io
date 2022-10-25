from flask import Blueprint, redirect, render_template, request,flash, session, url_for
from model.models import UsuarioModel
from flask_login import login_user,login_required,logout_user,current_user
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = UsuarioModel.find_by_email(email=email)
        if user:
            if check_password_hash(user.password, password):
                flash('Login Sucess', category='sucess')
                login_user(user, remember=True)
                return redirect(url_for('auth.logout'))
        else:
            flash('Deu errado', category='error')
    return render_template('login.html', user=current_user)    

@auth.route('/logout')
def logout():
    return 'z'

@auth.route('/sign-up', methods= ['GET','POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = request.form.get('user')
        if email[-17:] != "@al.insper.edu.br":
            flash("Deve ser utilizado o email do insper", category='error')
        elif len(password) <8:
            flash('Senha deve ter mais de 8 caracteres', category='error')
        elif len(user) <3:
            flash('Seu usuário deve conter mais de 3 letras',category='error')
        else:
            flash('Conta criada!', category='sucess')
            new_user = UsuarioModel(email= email, password=generate_password_hash(password,method= 'sha256'), user =user)
            new_user.save()
            return redirect(url_for('auth.login'))
    return render_template('sign_up.html', user=current_user)