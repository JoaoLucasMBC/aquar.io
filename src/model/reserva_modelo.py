from model.sql_alchemy_flask import db
from sqlalchemy.orm import backref

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