from flask_restful import Resource
from flask import request, jsonify, session, redirect
from model.models import ReservaModel, AquarioModel

import datetime

class Reserva(Resource):


    def post(self, predio, andar, numero):
        try:
            corpo = request.get_json(force=True)
        except:
            return {'mensagem': 'Problema ao parsear o JSON'}, 400

        aquario, sucesso = AquarioModel.find_aquario(predio, andar, numero)

        if sucesso:
            horario = datetime.datetime(corpo["year"], corpo["month"], corpo["day"], corpo["hour"], corpo["minute"], corpo["second"])

            reserva = ReservaModel(usuario_id=session["user_id"], aquario_id=aquario.id, horario=horario, blocos=corpo["blocos"])
            reserva.save()

            return redirect("reserva", code=201)
            
        return {'mensagem': 'Aquário não foi encontrado'}, 404