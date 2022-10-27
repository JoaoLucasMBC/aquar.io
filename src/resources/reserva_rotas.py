from flask_restful import Resource
from flask import request, jsonify, redirect
from model.models import ReservaModel, AquarioModel

from flask_login import current_user

import datetime

def formata_data(string_data):
    valido = string_data[:10]
    ano,mes,dia = valido.split('-')
    dict_data = {'year': ano, 'month': mes, 'day': dia}
    return dict_data

def formata_hora(string_hora):
    hora,minuto = string_hora.split('h')
    dict_hora = {'hour':hora, 'minute': minuto}
    return dict_hora 




class Reserva(Resource):
    def get(self, predio, andar, numero):
        '''
        Rota para encontrar as reservas de um determinado aquário

        Entrada: 'predio, andar, numero'
        Saida: 
            Sucesso: dicionário da reserva
            Erro: 'Mensagem de erro'
        '''
        aquario, sucesso = AquarioModel.find_aquario(predio, andar, numero)

        if sucesso:
            reserva = ReservaModel.find_by_aquario(aquario)
            if reserva:
                return jsonify(reserva), 200
            else:
                return {'mensagem': 'Reserva não encontrada'}, 404
        
        return {'mensagem': 'Aquário não encontrado'}, 404


    def post(self, predio, andar, numero):
        '''
        Rota para adicionar uma reserva em um determinado aquário

        Entrada: 'predio, andar, numero'
        Saida: 
            Sucesso: Redireciona para página de reservas individuais
            Erro: 'Mensagem de erro'
        '''
        try:
            corpo = request.get_json(force=True)
        except:
            return {'mensagem': 'Problema ao parsear o JSON'}, 400

        aquario, sucesso = AquarioModel.find_aquario(predio, andar, numero)

        if sucesso:
            dict_data = formata_data(corpo['data'])
            dict_hora = formata_hora(corpo['hora'])
            blocos = corpo['duracao'][1]

            horario_inicial = datetime.datetime(dict_data['year'], dict_data["month"], dict_data["day"], dict_hora["hour"], dict_hora["minute"], 0)
            horario_final = ReservaModel.hour_calculator(data=horario_inicial, blocos=blocos)

            success = ReservaModel.reserva_check(horario_inicial,horario_final,aquario.id)

            if success:
                if len(current_user.reservas) < 2:
                    reserva = ReservaModel(usuario_id=current_user.id, aquario_id=aquario.id, horario_inicial=horario_inicial, horario_final=horario_final)
                    reserva.save()
                    return redirect("reserva", code=201)
                else:
                    return {"mensagem: 'As reservas são limitadas a um número máximo de dois'"},400
        
            return {'mensagem': "Esses horário estão indisponíveis"}, 400

        return {'mensagem': 'Aquário não foi encontrado'}, 404  


    def delete():
        pass



class MinhaReserva(Resource):

    def get(self):
        '''
        Rota para encontrar as reservas de um determinado usuário

        Entrada: 
        Saida: 
            Sucesso: dicionário das reservas
            Erro: 'Mensagem de erro'
        '''
        if current_user:
            reservas = ReservaModel.find_by_user(current_user)
            if reservas:
                reservas = [reserva.to_dict() for reserva in reservas]
                return {'reservas': reservas}, 200
            else:
                return {'mensagem': 'Reserva não encontrada'}, 404
