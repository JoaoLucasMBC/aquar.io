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