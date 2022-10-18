from flask_restful import Resource
from flask import request, jsonify
from model.aquario_modelo import AquarioModel



class ListaAquarios(Resource):
    def get(self, predio):
        todos_aquarios = AquarioModel.filter_by_building(predio)

        lista_livres = []
        lista_reservados = []
        for aquario in todos_aquarios:
            if aquario.status == True:
                lista_reservados.append(aquario.to_dict())
            else:
                lista_livres.append(aquario.to_dict())
        

        return {'aquarios_livres': lista_livres, 'aquarios_reservados': lista_reservados}, 200