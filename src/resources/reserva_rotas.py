from flask_restful import Resource
from flask import request, jsonify, session
from model.models import ReservaModel, AquarioModel

import datetime

class Reserva(Resource):


    def post(self, predio, andar, numero):
        corpo = request.get_json(force=True)

        horario_incial = datetime.datetime(corpo["year"], corpo["month"], corpo["day"], corpo["hour"], corpo["minute"], corpo["second"])
        horario_final = ReservaModel.hour_calculator(data=horario_incial, blocos=corpo["blocos"])
        aquarios = AquarioModel.list_all()
        for aquario in aquarios:
            if aquario.building == predio:
                if aquario.floor == andar:
                    if aquario.number == numero:
                        success = ReservaModel.reserva_check(horario_incial,horario_final,aquario.id)
                        if success:
                            aquarios = AquarioModel.list_all()
                            for aquario in aquarios:
                                if aquario.building == predio:
                                    if aquario.floor == andar:
                                        if aquario.number == numero:
                                            reserva = ReservaModel(usuario_id=1, aquario_id=aquario.id, horario_inicial=horario_incial, horario_final=horario_final)
                                            reserva.save()
                                            return reserva.to_dict()
                        else:
                            return {'mensagem': "Esses horário estão indisponíveis"}, 400