from model.sql_alchemy_flask import db

class ReservaModel(db.Model):
    __tablename__ = "reserva_model"

    id = db.Column(db.Integer, primary_key=True)
    aquario_info = db.Column(db.String, db.ForeignKey('aquario_model'))
    user = db.Column(db.String, db.ForeignKey('usuario_model'))