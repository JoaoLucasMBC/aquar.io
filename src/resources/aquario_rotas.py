from flask_restful import Resource
from flask import request, jsonify
from model.aquario_modelo import AquarioModel



class ListaAquarios(Resource):
    def get(self):
        todos_aquarios = AquarioModel.list_all()

        lista = []
        for aquario in todos_aquarios:
            lista.append(aquario.to_dict())
        

        return {'aquarios': lista}, 200

    def put(self):
        corpo = request.get_json(force=True)
        aquario = AquarioModel.find_by_id(corpo['id'])

        if aquario:
            aquario.status = corpo['status']
            return aquario.to_dict()            
        
        return {'Usuário não encontrado'}, 404