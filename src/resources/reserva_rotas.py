from flask_restful import Resource
from flask import request, jsonify, redirect
from model.models import ReservaModel, AquarioModel, UsuarioModel

from token_aquario import fernet
import cryptography

import datetime

def formata_data(string_data):
    valido = string_data[:10]
    ano,mes,dia = valido.split('-')
    dict_data = {'year': int(ano), 'month': int(mes), 'day': int(dia)}
    return dict_data

def formata_hora(string_hora):
    hora,minuto = string_hora.split('h')
    dict_hora = {'hour':int(hora), 'minute': int(minuto)}
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
                return jsonify(reserva.to_dict()), 200
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
            blocos = int(corpo['duracao'][2])

            horario_inicial = datetime.datetime(dict_data['year'], dict_data["month"], dict_data["day"], dict_hora["hour"], dict_hora["minute"], 0)
            horario_final = ReservaModel.hour_calculator(horario=horario_inicial, blocos=blocos)

            success = ReservaModel.reserva_check(horario_inicial,horario_final,aquario.id)

            if success:
                if 'token' in corpo:
                    token = str(corpo['token']).encode()
                    email = fernet.decrypt(token)
                    email = email.decode()

                    try:
                        usuario = UsuarioModel.find_by_email(email)
                    except cryptography.exceptions.InvalidSignature:
                        return {'mensagem': 'Token inválido'}, 400

                    if len(usuario.reservas) < 2:
                        reserva = ReservaModel(usuario_id=usuario.id, aquario_id=aquario.id, horario_inicial=horario_inicial, horario_final=horario_final)
                        reserva.save()
                        
                        return {
                            'mensagem': 'Reserva feita com sucesso',
                            'reserva': reserva.to_dict()
                            }, 201
                    else:
                        return {"mensagem": "As reservas são limitadas a um número máximo de dois"},400
                
                return {"mensagem": "Usuário não autenticado"}, 401
            
            return {'mensagem': "Esses horário estão indisponíveis"}, 400

        return {'mensagem': 'Aquário não foi encontrado'}, 404  



class MinhaReserva(Resource):

    def get(self, token):
        '''
        Rota para encontrar as reservas de um determinado usuário

        Entrada: 
        Saida: 
            Sucesso: dicionário das reservas
            Erro: 'Mensagem de erro'
        '''

        if token:
            token = str(token).encode()
            email = fernet.decrypt(token)
            email = email.decode()

            try:
                usuario = UsuarioModel.find_by_email(email)
            except cryptography.exceptions.InvalidSignature:
                return {'mensagem': 'Token inválido'}, 400

            reservas = ReservaModel.find_by_user(usuario)
            if reservas:
                reservas = [reserva.to_dict() for reserva in reservas]
                return {'reservas': reservas}, 200
            else:
                return {'mensagem': 'Reservas não encontradas'}, 404
        
        return {'mensagem': 'Usuário não autenticado'}, 401


    def delete(self, token):
        '''
        Rota para deletar uma reserva de um determinado usuário
            
            Entrada: "reserva_id" no JSON
            Saida: 
                Sucesso: mensagem de sucesso
                Erro: mensagem de erro
        '''

        try:
            corpo = request.get_json(force=True)
        except:
            return {'mensagem': 'Problema ao parsear o JSON'}, 400

        reserva = ReservaModel.find_by_id(id=corpo['reserva_id'])

        if reserva:
            reserva.delete()
            return {'mensagem': 'Reserva deletada com sucesso'}, 200
        
        return {'mensagem': 'Reserva não encontrada'}, 404