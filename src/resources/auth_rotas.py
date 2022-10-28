from flask import Blueprint, redirect, render_template, request,flash, session, url_for
from model.models import UsuarioModel
from flask_login import login_user,login_required,logout_user,current_user
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

'''
OBS:
Ambas as rotas de login e cadastro são incompatíveis com flask_restful, pois utilizam a lib flask_login.
Por causa disso, as rotas não seguem o modelo de classes do flask_restful, porém foram modeladas seguindo princípios REST.
'''

@auth.route('/login', methods=['POST'])
def login():
    '''
    Rota para realizar o login
    
    Entrada: 'email', 'senha'
    Saídas:
        - Sucesso: 'email', 'user'
        - Erro: 'mensagem'
    '''
    try:
        corpo = request.get_json(force=True)
    except:
        return {'mensagem': 'Problema ao parsear o JSON'}, 400

    user = UsuarioModel.find_by_email(email=corpo['email'])

    if user:
        if check_password_hash(user.password, corpo['password']):
            flash('Logado com sucesso', category='sucess')
            login_user(user, remember=True, force=True)

            return {'mensagem': 'Logado com sucesso', 'usuário':{
                'email':current_user.email,
                'user':current_user.user
            }}, 200
        
        return {'mensagem': 'Senha incorreta'}, 400
    else:
        flash('Deu errado', category='error')

        return {'mensagem': 'Usuário não encontrado com esse email'}, 404



@auth.route('/cadastro', methods= ['POST'])
def sign_up():
    '''
    Rota para realizar o cadastro de usuário
    
    Entrada: 'email, senha'
    Saida: 
        Sucesso: 'email, user'
        Erro: 'Mensagem de erro'
    '''
    try:
        corpo = request.get_json(force=True)
    except:
        return {'mensagem': 'Problema ao parsear o JSON'}, 400


    if corpo['email'][-17:] != "@al.insper.edu.br":
        flash("Deve ser utilizado o email do insper", category='error')

        return {'mensagem': 'Deve ser utilizado o email do Insper'}, 400

    elif len(corpo['password']) < 8:
        flash('Senha deve ter mais de 8 caracteres', category='error')

        return {'mensagem': 'Senha deve ter mais de 8 caracteres'}, 400

    else:
        flash('Conta criada!', category='sucess')
        new_user = UsuarioModel(email= corpo['email'], password=generate_password_hash(corpo['password'],method= 'sha256'), user = corpo['email'].split('@')[0])
        new_user.save()

        return {'mensagem': 'Conta criada com sucesso!', 'usuário': {
            'email': new_user.email,
            'user': new_user.user
        }}, 201