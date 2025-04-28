#importando flask do pacote API
from api import app, mongo
from api.models.movie_model import Movie
from api.services import movie_services
from flask_marshmallow import Marshmallow

#rodando aplicação
if __name__ == '__main__':
    #criando o banco com suas coleções
    with app.app_context():
        #cria coleção se não existir
        if 'movies' not in mongo.db.list_collection_names():
            movie = Movie(
                title = '',
                desscription= '',
                year=0
            )
            movie_services.add_movie(movie)
    app.run(host='localhost',port='5000',debug=True)