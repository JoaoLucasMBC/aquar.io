from flask_restful import Resource
from flask import request, jsonify, session, redirect
from model.models import ReservaModel, AquarioModel

import datetime


class Reserva(Resource):
    def get(self, aquario):
        if aquario != 0:
            reserva = ReservaModel.find_by_aquario(aquario)
            if reserva:
                return jsonify(reserva), 200
            else:
                return {'mensagem': 'Reserva não encontrada'}, 404


    def post(self, predio, andar, numero):
        try:
            corpo = request.get_json(force=True)
        except:
            return {'mensagem': 'Problema ao parsear o JSON'}, 400

        aquario, sucesso = AquarioModel.find_aquario(predio, andar, numero)

        if sucesso:
            horario_inicial = datetime.datetime(corpo["year"], corpo["month"], corpo["day"], corpo["hour"], corpo["minute"], corpo["second"])
            horario_final = ReservaModel.hour_calculator(data=horario_inicial, blocos=corpo["blocos"])

            success = ReservaModel.reserva_check(horario_inicial,horario_final,aquario.id)

            if success:
                reserva = ReservaModel(usuario_id=1, aquario_id=aquario.id, horario_inicial=horario_inicial, horario_final=horario_final)
                reserva.save()
                return redirect("reserva", code=201)
        
            return {'mensagem': "Esses horário estão indisponíveis"}, 400

        return {'mensagem': 'Aquário não foi encontrado'}, 404



class MinhaReserva(Resource):

    def get(self, user):
        if user != 0:
            reserva = ReservaModel.find_by_user(user)
            if reserva:
                return jsonify(reserva), 200
            else:
                return {'mensagem': 'Reserva não encontrada'}, 404