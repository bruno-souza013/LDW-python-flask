#importando a classe Resource do flask_restful
from flask_restful import Resource

from api import api

from flask import make_response, jsonify, request
from ..schemas import movie_schema
from ..models import movie_model
from ..services import movie_services

class MovieList(Resource):
    def get(self):
        movies = movie_services.get_movies()
        mv = movie_schema.MovieSchema(many=True)
        #código status OK
        return make_response(mv.jsonify(movies), 200)
    
    def post(self):
        mv = movie_schema.MovieSchema()
        validate = mv.validate(request.json)
        #Tratando se a validação falhar
        if validate:
            return make_response(jsonify(validate), 400)
        else:
            title = request.json["title"]
            description = request.json["description"]
            year = request.json["year"]
            
            new_movie = movie_model.Movie(
                title = title,
                desscription = description,
                year = year
            )
            result = movie_services.add_movie(new_movie)
            res = mv.jsonify(result)
            return make_response(res, 201)

class MovieDetail(Resource):
    def delete(self, id):
        movie = movie_services.get_movie_by_id(id)
        if movie is None:
            return make_response(jsonify("Filme não encontrado!"),400)
        movie_services.delete_movie(id)
        return make_response(jsonify("Filma excluído com sucesso!"), 204)
    #listando um filme unico
    def get(self, id):
        movie = movie_services.get_movie_by_id(id)
        if movie is None:
            return make_response(jsonify("Filme não encontrado."), 404)    
        mv = movie_schema.MovieSchema()
        return make_response(mv.jsonify(movie), 200)
    #alterando filme
    def put(self, id):
        movie_db = movie_services.get_movie_by_id(id)
        if movie_db is None:
            return make_response(jsonify("Filme não encontrado."), 404)
        mv = movie_schema.MovieSchema()
        validate = mv.validate(request.json)
        #Falhou na validação
        if validate:
            return make_response(jsonify(validate), 400) #Bad request
        else:
            title = request.json['title']
            description = request.json['description']
            year = request.json['year']
            new_movie = movie_model.Movie(title=title, desscription=description, year=year)
            movie_services.update_movies(new_movie, id)
            updated_movie = movie_services.get_movie_by_id(id)
            return make_response(mv.jsonify(updated_movie), 200)

api.add_resource(MovieList, '/movies')
api.add_resource(MovieDetail, '/movie/<id>')
