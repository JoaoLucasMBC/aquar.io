import datetime
 
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from pathlib import Path

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from resources.aquario_rotas import Aquario, ListaAquarios
from resources.reserva_rotas import Reserva


from model.sql_alchemy_flask import db
from model.models import UsuarioModel, AquarioModel, ReservaModel
from resources.usuario_rotas import Usuario
from resources.reserva_rotas import MinhaReserva, Reserva

from resources.auth_rotas import auth
from flask_login import LoginManager, login_required

from werkzeug.security import generate_password_hash, check_password_hash

from flask_cors import CORS


# Resistente a sistema operacional
FILE = Path(__file__).resolve()
src_folder = FILE.parents[0]
# caminho para a base
rel_arquivo_db = Path('model/aquario.db')
caminho_arq_db = src_folder / rel_arquivo_db

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{caminho_arq_db.resolve()}'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://dwlijhricezcmf:68bd4bc1ff93594ee7937d3f2e97e4937afbc1384996b61013f78c88b0bc13f0@ec2-54-161-255-125.compute-1.amazonaws.com:5432/ddsvjv69vdumm7'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


app.secret_key = 'r4AKmLM41NljU9iU1IRlZw'
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
app.register_blueprint(auth, url_prefix='/')
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return UsuarioModel.query.get(int(id))

admin = Admin(app, name='aquar.io', template_mode='bootstrap3')
admin.add_view(ModelView(AquarioModel, db.session))
admin.add_view(ModelView(UsuarioModel, db.session))
admin.add_view(ModelView(ReservaModel, db.session))
#https://docs.sqlalchemy.org/en/14/core/engines.html
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()

    '''
    new_user = UsuarioModel(email= 'joaolmbc@al.insper.edu.br', password=generate_password_hash('1234567890',method= 'sha256'), user = 'joaolmbc')
    new_user.save()
    new_user1 = UsuarioModel(email= 'liviat1@al.insper.edu.br', password=generate_password_hash('1234567890',method= 'sha256'), user = 'liviat1')
    new_user1.save()

    new_aquario = AquarioModel(building=1, floor=0, number=12, capacity=5)
    new_aquario.save()
    new_aquario1 = AquarioModel(building=1, floor=0, number=13, capacity=5)
    new_aquario1.save()
    new_aquario2 = AquarioModel(building=2, floor=2, number=4, capacity=8)
    new_aquario2.save()
    new_aquario3 = AquarioModel(building=2, floor=5, number=1, capacity=8)
    new_aquario3.save()

    new_reserva = ReservaModel(usuario_id=1, aquario_id=1, horario_inicial=datetime.datetime(2022, 10, 30, 12, 0, 0), horario_final=datetime.datetime(2022, 10, 30, 14, 0, 0))
    new_reserva.save()
    new_reserva1 = ReservaModel(usuario_id=2, aquario_id=2, horario_inicial=datetime.datetime(2022, 11, 2, 11, 0, 0), horario_final=datetime.datetime(2022, 11, 2, 15, 30, 0))
    new_reserva1.save()
    '''


@app.after_request
def exclui_reservas(response):
    reservas = ReservaModel.list_all()
    for reserva in reservas:
        if reserva:
            if reserva.horario_final < datetime.datetime.now():
                reserva.esta_aberta = False
                reserva.save()
            if reserva.horario_final.month < datetime.datetime.now().month:
                reserva.delete()
    return response


@app.route("/")
def hello_world():
    return f"<p>Hello, World!</p>"


api.add_resource(ListaAquarios, '/aquario/<int:predio>')
api.add_resource(Aquario, '/aquario/<int:predio>/<int:andar>/<int:numero>')
api.add_resource(Usuario, '/usuario')
api.add_resource(Reserva, '/aquario/<int:predio>/<int:andar>/<int:numero>/reserva')
api.add_resource(MinhaReserva, '/reserva')


db.init_app(app)
if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True)