from types import CoroutineType
from flask_restful import Resource
from flask import request, jsonify
from model.usuario_modelo import UsuarioModel

class Usuario(Resource):

    def get(self):
        corpo = request.get_json(force=True)
        usuario = UsuarioModel.find_by_email(email = corpo['email'])

        if usuario:
            return usuario.to_dict(),200
        
        return {'email não encontrado'}, 404
    
    def post(self):
        corpo = request.get_json(force=True)

        usuario = UsuarioModel( email = corpo['email'], password = corpo['password'],user = corpo['user'])
        try:
            usuario.save()
        except:
            return {"mensagem":"Ocorreu um erro interno ao tentar inserir um aluno (DB)"}, 500

        return usuario.to_dict(), 201
        