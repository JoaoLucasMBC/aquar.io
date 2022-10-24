from flask_restful import Resource
from flask import request, jsonify
from model.models import ReservaModel

import datetime

class Reserva(Resource):




    def post(self, predio, andar, numero):
        pass