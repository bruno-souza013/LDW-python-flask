from flask import Flask

from flask_restful import Api

from flask_pymongo import PyMongo

from flask_marshmallow import Marshmallow

app = Flask(__name__)

ma = Marshmallow(app)

api = Api(app)

#Configurando flask com mongoDB
app.config['MONGO_URI'] = 'mongodb://localhost:27017/api-movies'

#carregando com o pymongo
mongo = PyMongo(app)

#importando recursos
from .resources import movies_resources