from model.sql_alchemy_flask import db
import datetime


class ReservaModel(db.Model):
    __tablename__ = "reserva_model"

    usuario_id = db.Column(db.ForeignKey('usuario_model.id'), primary_key=True)
    aquario_id = db.Column(db.ForeignKey('aquario_model.id'), primary_key=True)
    esta_aberta = db.Column(db.Boolean, default=True)

    usuario = db.relationship("UsuarioModel", back_populates='reservas')
    aquario = db.relationship("AquarioModel", back_populates='reservas')

    horario = db.Column(db.Datetime)
    blocos = db.Column(db.Integer)

    def __init__(self, usuario_id, aquario_id):
        self.usuario_id = usuario_id
        self.aquario_id = aquario_id
        self.esta_aberta = True


    def __repr__(self):
        return f"ReservaModel(usuario_id={self.usuario_id}, aquario_id={self.aquario_id})"



class UsuarioModel(db.Model):
    _tablename_ = 'usuario_model'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(20))
    user = db.Column(db.String(20))

    reservas = db.relationship("ReservaModel", back_populates="usuario")
    
    def __init__(self, email, password, user):
        self.user= user
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
        return cls.query.filter_by(email = email).first()
    
    @classmethod
    def find_by_user(cls, user):
        return cls.query.filter_by(user = user).first()
    
    # @classmethod
    # def find_by_id(cls, id):
    #     return cls.query.filter_by(id = id).first()



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
    last_updated = db.Column(db.DateTime, onupdate=datetime.datetime.now)

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
        return cls.query.all()
    
    @classmethod
    def filter_by_building(cls, predio:int):
        return cls.query.filter_by(building = predio)

    @classmethod
    def find_by_id(cls, id:int):
        return cls.query.filter_by(id=id).first()
    

    def to_dict(self):
        return {
            'id': self.id,
            'building': self.building,
            'floor': self.floor,
            'number': self.number,
            'status': self.status,
            'capacity': self.capacity,
            'num_people': self.num_people,
            'last_updated': self.last_updated
        }