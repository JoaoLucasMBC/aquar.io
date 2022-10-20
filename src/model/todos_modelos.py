from model.sql_alchemy_flask import db


class UsuarioModel(db.Model):
    _tablename_ = 'usuario_model'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(20))
    user = db.Column(db.String(20))

    reservas = db.relationship('ReservaModel', secondary='reserva_table', backref='usuario')
    
    def __init__(self, email, password, user):
        self.user= user
        self.email = email
        self.password = password
        self.monthly_limit = 2
        self.pending = True

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

    reservas = db.relationship('ReservaModel', secondary='reserva_table', backref='aquario')

    def __init__(self, building:int, floor:int, number:int, capacity:int, status=False):
        self.building = building
        self.floor = floor
        self.number = number
        self.info = f'{building}-{floor}-{number}'
        self.status = status
        self.capacity = capacity
        self.num_people = 0
    

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
            'num_people': self.num_people
        }
    
    
reserva_table = db.Table(
    'reserva_table',
    db.Column('aquario_id', db.Integer, db.ForeignKey('aquario.id')),
    db.Column('usuario_id', db.Integer, db.ForeignKey('usuario.id'))
)


class ReservaModel(db.Model):
    __tablename__ = "reserva_model"

    id = db.Column(db.Integer, primary_key=True)
    aquario_id = db.Column(db.Integer, db.ForeignKey('aquario.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))

    user = db.relationship('UsuarioModel', backref=backref('reservas', cascade='all, delete-orphan'))
    aquario = db.relationship('AquarioModel', backref=backref('reservas', cascade='all, delete-orphan'))
