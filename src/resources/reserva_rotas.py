from flask_restful import Resource
from flask import request, jsonify, session
from model.models import ReservaModel, AquarioModel

import datetime

class Reserva(Resource):


    def post(self, predio, andar, numero):
        corpo = request.get_json(force=True)
        aquarios = AquarioModel.list_all()
        horario = datetime.datetime(corpo["year"], corpo["month"], corpo["day"], corpo["hour"], corpo["minute"], corpo["second"])
        for aquario in aquarios:
            if aquario.building == predio:
                if aquario.floor == andar:
                    if aquario.number == numero:
                        reserva = ReservaModel(usuario_id=session["user_id"], aquario_id=aquario.id, horario=horario, blocos=corpo["blocos"])
                        reserva.save()
                        return reserva.to_dict()