""" class ReservaModel(db.Model):
    __tablename__ = "reserva_model"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    aquario_id = db.Column(db.Integer, db.ForeignKey('aquario.id'))

    usuario = db.relationship('UsuarioModel', secondary=reserva_table, backref=backref('reserva', cascade='all, delete-orphan'))
    aquario = db.relationship('AquarioModel', secondary=reserva_table, backref=backref('reserva', cascade='all, delete-orphan'))
 """