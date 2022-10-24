from flask_restful import Resource
from flask import request, jsonify
from model.models import ReservaModel

class Reserva(Resource):
    
    def get(self, aquario):
        if aquario != 0:
            reserva = ReservaModel.find_by_user(aquario)
            if reserva:
                return reserva
            else:
                return {'Reserva não encontrada'}

class MinhaReserva(Resource):

    def get(self, user):
        if user != 0:
            reserva = ReservaModel.find_by_user(user)
            if reserva:
                return reserva
            else:
                return {'Reserva não encontrada'}
                    
