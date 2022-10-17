from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from pathlib import Path

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from model.aquario_modelo import AquarioModel
from resources.aquario_rotas import ListaAquarios


from model.sql_alchemy_flask import db


# Resistente a sistema operacional
FILE = Path(__file__).resolve()
src_folder = FILE.parents[0]
# caminho para a base
rel_arquivo_db = Path('model/aquario.db')
caminho_arq_db = src_folder / rel_arquivo_db


app = Flask(__name__)
app.secret_key = 'r4AKmLM41NljU9iU1IRlZw'
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
admin = Admin(app, name='aquar.io', template_mode='bootstrap3')
admin.add_view(ModelView(AquarioModel, db.session))
#https://docs.sqlalchemy.org/en/14/core/engines.html
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{caminho_arq_db.resolve()}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


@app.route("/")
def hello_world():
    return f"<p>Hello, World!</p>"


api.add_resource(ListaAquarios, '/aquario/')


if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True)