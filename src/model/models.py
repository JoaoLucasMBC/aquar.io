from model.sql_alchemy_flask import db
import datetime
from flask_login import UserMixin


class ReservaModel(db.Model):
    __tablename__ = "reserva_model"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.ForeignKey('usuario_model.id'))
    aquario_id = db.Column(db.ForeignKey('aquario_model.id'))
    esta_aberta = db.Column(db.Boolean, default=True)

    usuario = db.relationship("UsuarioModel", back_populates='reservas')
    aquario = db.relationship("AquarioModel", back_populates='reservas')

    horario_incial = db.Column(db.DateTime)
    horario_final = db.Column(db.DateTime)

    def __init__(self, usuario_id, aquario_id, horario_inicial, horario_final):
        self.usuario_id = usuario_id
        self.aquario_id = aquario_id
        self.esta_aberta = True
        self.horario_incial = horario_inicial
        self.horario_final = horario_final

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    @classmethod
    def list_all(cls):
        return cls.query.all()
    
    @classmethod
    def hour_calculator(cls,horario,blocos):
        '''
        Calcula o horário final da reserva, baseado no tanto de blocos de 30 minutos e no horário inicial

        @param: horario_inicial, blocos
        @return: horario_final (objeto tipo datetime)
        '''
        minute = horario.minute
        hour = horario.hour

        minute += blocos * 30
        while minute >= 60:
            minute -= 60
            hour += 1

        return datetime.datetime(horario.year,horario.month,horario.day,hour,minute,horario.second)

    @classmethod
    def reserva_check(cls,horario_incial,horario_final, aquario_id):
        '''
        Verifica se o horário da reserva sendo criada está livre

        @param: horario_inicial, horario_final, aquario_id
        @return: True (se o horário está livre), False (se não)
        '''

        reservas = ReservaModel.list_all()
        for reserva in reservas:
            if (reserva.horario_incial.month == horario_incial.month) and (reserva.horario_incial.day == horario_incial.day) and (reserva.aquario_id == aquario_id):
                if reserva.horario_incial <= horario_incial and horario_incial < reserva.horario_final:
                    return False
                elif reserva.horario_incial < horario_final and horario_final <= reserva.horario_final:
                    return False
        return True
    
    def to_dict(self):
        return {
            'reserva_id': self.id,
            'usuario_id':self.usuario_id,
            'aquario':self.aquario.to_dict(),
            'esta_aberta':self.esta_aberta,
            'dia': self.horario_incial.strftime("%d/%m"),
            'horario_inicial':self.horario_incial.strftime("%H:%M"),
            'horario_final':self.horario_final.strftime("%H:%M")
        }


    def __repr__(self):
        return f"ReservaModel(usuario_id={self.usuario_id}, aquario_id={self.aquario_id})"


    @classmethod
    def find_by_user(cls, usuario):
        '''
        Filtra as reservas de um usuário específico, e retorna uma query dessas reservas

        @param: usuario
        @return: query das reservas do usuario
        '''
        return cls.query.filter_by(usuario = usuario)
    
    @classmethod
    def find_by_aquario(cls, aquario):
        '''
        Filtra todos as reservas pertencentes a um aquário, e retorna uma query com essas reservas

        @param: aquario
        @return: query das reservas do aquário
        '''
        return cls.query.filter_by(aquario = aquario)
    
    @classmethod
    def find_by_id(cls, id:int):
        '''
        Filtra uma reserva específica, e retorna essa reserva

        @param: id
        @return: reserva
        '''
        return cls.query.filter_by(id=id).first()


class UsuarioModel(db.Model, UserMixin):
    _tablename_ = 'usuario_model'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(20))
    user = db.Column(db.String(20))

    reservas = db.relationship("ReservaModel", back_populates="usuario")
    
    def __init__(self, email, password, user):
        self.user = user
        self.email = email
        self.password = password
        self.monthly_limit = 2
        self.pending = True
    

    def __repr__(self):
        return f"User('{self.user}', '{self.email}')"

    def to_dict(self):
        return {'usuario': self.user, 'email': self.email}
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_email(cls, email):
        '''
        Procura o usuário baseado no email

        @param: email
        @return: usuário com email correspondente
        '''
        return cls.query.filter_by(email = email).first()


class AquarioModel(db.Model):
    __tablename__ = "aquario_model"

    id = db.Column(db.Integer, primary_key=True)
    building = db.Column(db.Integer)
    floor = db.Column(db.Integer)
    number = db.Column(db.Integer)
    info = db.Column(db.String, unique=True)
    status = db.Column(db.Boolean, default=False)
    capacity = db.Column(db.Integer)
    num_people = db.Column(db.Integer, default=0)
    last_updated = db.Column(db.DateTime, onupdate=datetime.datetime.now, default=datetime.datetime.now)

    reservas = db.relationship("ReservaModel", back_populates="aquario")

    def __init__(self, building:int, floor:int, number:int, capacity:int, status=False):
        self.building = building
        self.floor = floor
        self.number = number
        self.info = f'{building}-{floor}-{number}'
        self.status = status
        self.capacity = capacity
        self.num_people = 0
        self.last_updated = datetime.datetime.now()
    
    def __repr__(self):
        return f"Aquario('{self.info}', '{self.status}')"


    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    

    @classmethod
    def list_all(cls):
        '''
        Lista todos os aquários, retornando eles em uma query

        @return: query de todos os aquários
        '''
        return cls.query.all()
    
    @classmethod
    def filter_by_building(cls, predio:int):
        '''
        Filtra os aquários por prédio do Insper, retornando uma query com todos os aquários de um prédio

        @param: predio
        @return: query dos aquários do prédio
        '''
        return cls.query.filter_by(building = predio)

    @classmethod
    def find_by_id(cls, id:int):
        '''
        Encontra um aquário pelo seu id

        @param: id
        @return: aquário correspondente
        '''
        return cls.query.filter_by(id=id).first()
    
    @classmethod
    def find_aquario(cls, building, floor, number):
        '''
        Encontra um aquário utilizando o prédio, o andar e o número do aquário

        @param: prédio, andar, número
        @return: aquário correspondente
        '''
        aquarios = cls.list_all()

        for aquario in aquarios:
            if aquario.building == building:
                if aquario.floor == floor:
                    if aquario.number == number:
                        return aquario, True
        
        return None, False
    

    def to_dict(self):
        return {
            'id': self.id,
            'building': self.building,
            'floor': self.floor,
            'number': self.number,
            'status': self.status,
            'capacity': self.capacity,
            'num_people': self.num_people,
            'last_updated': self.last_updated.strftime("%H:%M")
        }