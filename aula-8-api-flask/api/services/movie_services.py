from api import mongo
from ..models import movie_model
from bson import ObjectId

#método para cadastrar
def add_movie(movie):
    result = mongo.db.movies.insert_one({
        'title' : movie.title,
        'description': movie.description,
        'year' : movie.year
    })

    # Buscar filme recém cadastrado
    new_movie = mongo.db.movies.find_one({'_id': result.inserted_id})
    return new_movie

#método estático nao precisa de instancia
#método para listar
@staticmethod
def get_movies():
    return list(mongo.db.movies.find())

@staticmethod
def delete_movie(id):
    mongo.db.movies.delete_one({'_id': ObjectId(id)})
    
#me´todo listar unicoi fil,me
def get_movie_by_id(id):
    return mongo.db.movies.find_one({'_id': ObjectId(id)})

#método para alterar o filme
def update_movies(self, id):
    mongo.db.movies.update_one({'_id': ObjectId(id)},
                               {'$set': 
                                   {
                                    'title' : self.title,
                                    'description': self.description,
                                    'year': self.year
                                   }
                                   })