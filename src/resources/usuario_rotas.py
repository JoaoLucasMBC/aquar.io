from types import CoroutineType
from flask_restful import Resource
from flask import request, jsonify
from model.models import UsuarioModel

class Usuario(Resource):

    def get(self):
        '''
        Rota para encontrar um determinado usuário

        Entrada: 
        Saida: 
            Sucesso: dicionário do usuário
            Erro: 'Mensagem de erro'
        '''
        corpo = request.get_json(force=True)
        usuario = UsuarioModel.find_by_email(email = corpo['email'])

        if usuario:
            return usuario.to_dict(),200
        
        return {'email não encontrado'}, 404
        