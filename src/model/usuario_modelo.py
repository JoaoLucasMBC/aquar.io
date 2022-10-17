from model.sql_alchemy_flask import db

class UsuarioModel(db.Model):
    _tablename_ = 'usuario_model'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80))
    password = db.Column(db.String(20))
    user = db.Column(db.String(20))
    
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
