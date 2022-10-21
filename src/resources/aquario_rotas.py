from flask_restful import Resource
from flask import request, jsonify
from model.models import AquarioModel



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

class Aquario(Resource):
    def get(self, predio, andar, numero):
        aquarios = AquarioModel.list_all()

        for aquario in aquarios:
            if aquario.building == predio:
                if aquario.floor == andar:
                    if aquario.number == numero:
                        return aquario.to_dict(),200
        return {'Usuário não encontrado'}, 404

    def put(self, predio, andar, numero):
        aquarios = AquarioModel.list_all()

        for aquario in aquarios:
            if aquario.building == predio:
                if aquario.floor == andar:
                    if aquario.number == numero:
                        if aquario.status == True:
                            aquario.status = False
                        elif aquario.status == False:
                            aquario.status = True
                        aquario.save()
                        return aquario.to_dict(),200          
        
        return {'Usuário não encontrado'}, 404