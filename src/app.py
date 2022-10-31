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


@app.after_request
def atualiza_reservas(response):
    reservas = ReservaModel.list_all()
    for reserva in reservas:
        if reserva:
            # Fecha a reserva se ela já passou e ainda está aberta
            if reserva.horario_final < (datetime.datetime.now() - datetime.timedelta(hours=3)) and reserva.esta_aberta == True:
                reserva.esta_aberta = False
                reserva.save()
                aquario = reserva.aquario
                # Libera o aquário se a reserva já passou e o aquário estava como ocupado
                if aquario.status == True:
                    aquario.status = False
                    aquario.last_updated = datetime.datetime.now() - datetime.timedelta(hours=3)
                    aquario.save()
            # Deleta a reserva se ela é do mês passado
            if reserva.horario_final.month < datetime.datetime.now().month:
                reserva.delete()
            # Se está no período da reserva e ela está aberta, atualiza o status do aquário para ocupad
            if reserva.horario_incial < (datetime.datetime.now() - datetime.timedelta(hours=3)) and reserva.horario_final > (datetime.datetime.now() - datetime.timedelta(hours=3)) and reserva.esta_aberta == True:
                aquario = reserva.aquario
                aquario.status = True
                aquario.last_updated = datetime.datetime.now() - datetime.timedelta(hours=3)
                aquario.save()
    return response


@app.route("/")
def hello_world():
    return f"<p>Hello, World!</p>"


api.add_resource(ListaAquarios, '/aquario/<int:predio>')
api.add_resource(Aquario, '/aquario/<int:predio>/<int:andar>/<int:numero>')
api.add_resource(Usuario, '/usuario')
api.add_resource(Reserva, '/aquario/<int:predio>/<int:andar>/<int:numero>/reserva')
api.add_resource(MinhaReserva, '/usuario/<string:token>/reserva')


db.init_app(app)
if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True)