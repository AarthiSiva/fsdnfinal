import json
import os

from flask import Flask, abort, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy


from auth import requires_auth, AuthError
from models import Actors, Movies, setup_db, db


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)
    RESULTS_PER_PAGE=10

    def paginate_result(myrequest, resultset):
        page = myrequest.args.get("page", 1, type=int)
        start = (page - 1) * RESULTS_PER_PAGE
        end = start + RESULTS_PER_PAGE
        resultdata = [data.format() for data in resultset]
        current_resultdata = resultdata[start:end]
        return current_resultdata


    @app.route('/', methods=['GET'])
    def root_helper():
        return "Welcome to Udacity Casting Agency!"

    @app.route('/login', methods=['GET'])
    @requires_auth()
    def login_helper(payload):
        return "Welcome to Udacity Casting Agency login page!"

    #####MOVIES#############

    #GET Movies

    def get_movies_helper():
        try:
            movies = Movies.query.order_by(Movies.id).all()
            Current_Movies=paginate_result(request,movies)
            if(len(Current_Movies)==0):
                abort(404)
            return jsonify(
                    {
                        'success':True,
                        'movies':Current_Movies,
                        'total_movies':len(Movies.query.all())
                    }
                )
        except Exception:
            abort(404)

    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(payload):
        return get_movies_helper()

    #GET Movies by ID
    def get_movie_by_id_helper(movie_id):
        try:
            movie = Movies.query.get(movie_id)
            current_movie = movie.format()
            return jsonify(
                    {
                        'success':True,
                        'movie':current_movie
                    }
                )
        except Exception:
            abort(404)


    @app.route('/movies/<movie_id>', methods=['GET'])
    @requires_auth('get:movies')
    def get_movie_by_id(payload, movie_id):
        return get_movie_by_id_helper(movie_id)

    #POST Movies

    def post_movies_helper(myrequest):
        
        body = myrequest.get_json()
        title = body.get("title", None)
        releasedate = body.get("releasedate", None)
        genre = body.get("genre", None)

        try:
            movie = Movies(title=title, releasedate=releasedate, genre=genre)
            movie.insert()
            
            movie_list = Movies.query.order_by(Movies.id).all()
            current_movies = paginate_result(myrequest, movie_list)

            return jsonify(
                {
                    "success": True,
                    "created": movie.id,
                    "movies": current_movies,
                    "total_movies": len(Movies.query.all())
                }
            )
        except Exception:
            abort(422)


    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def post_movies(payload):
        return post_movies_helper(request)

    #Delete movie
    def delete_movie_helper(movie_id):
        try:
            movie = Movies.query.get_or_404(movie_id)
            movie.delete()
            return jsonify({'success': True,
            'deleted':movie_id,
            'total_movies': Movies.query.count() })
        except Exception:
            db.session.rollback()
            return jsonify({'success': False,
            'deleted':None,
            'total_movies': Movies.query.count() }),404
        finally:
            db.session.close()
                

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(payload, movie_id):
        return delete_movie_helper(movie_id)

    #Patch movie

    #PATCH /movies/<id>
    def update_movies_helper(id, myrequest):
        movie = Movies.query.filter(Movies.id == id).one_or_none()
        if movie is None:
            abort(404)
    
        body = myrequest.get_json()
        if body is None:
            abort(400)

        title = body.get("title", None)
        releasedate = body.get("releasedate", None)
        genre = body.get("genre", None)

        if title is not None:
            movie.title = title
        
        if releasedate is not None:
            movie.releasedate = releasedate

        if genre is not None:
            movie.genre = genre

        movie.update()

        return jsonify(
                {
                    'success':True,
                    'updated':movie.id,
                    'movie':[movie.format()]
                }
            )

    @app.route('/movies/<id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movies(payload, id):
        return update_movies_helper(id, request)


    #####ACTORS#############

    #GET Actors

    def get_actors_helper():
        try:
            actors = Actors.query.order_by(Actors.id).all()
            Current_actors=paginate_result(request,actors)
            if(len(Current_actors)==0):
                abort(404)
            return jsonify(
                    {
                        'success':True,
                        'actors':Current_actors,
                        'total_actors':len(Actors.query.all())
                    }
                )
        except Exception:
            abort(400)

    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(payload):
        return get_actors_helper()
    
    #GET Actors by ID
    def get_actor_by_id_helper(actor_id):
        try:
            actor = Actors.query.get(actor_id)
            current_actor = actor.format()
            return jsonify(
                    {
                        'success':True,
                        'actor':current_actor
                    }
                )
        except Exception:
            abort(404)


    @app.route('/actors/<actor_id>', methods=['GET'])
    @requires_auth('get:actors')
    def get_actor_by_id(payload, actor_id):
        return get_actor_by_id_helper(actor_id)


    #POST Actors

    def post_actors_helper(myrequest):
        body = myrequest.get_json()
        name = body.get("name", None)
        age = body.get("age", None)
        gender = body.get("gender", None)

        try:
            actor = Actors(name=name, age=age, gender=gender)
            actor.insert()
            actor_list = Actors.query.order_by(Actors.id).all()
            current_actors = paginate_result(myrequest, actor_list)

            return jsonify(
                {
                    "success": True,
                    "created": actor.id,
                    "actors": current_actors,
                    "total_actors": len(Actors.query.all()),
                }
            )
        except Exception:
            abort(422)


    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def post_actors(payload):
        return post_actors_helper(request)


    #Delete actor
    def delete_actor_helper(actor_id):
        try:
            actor = Actors.query.get_or_404(actor_id)
            actor.delete()
            return jsonify({'success': True,
            'deleted':actor_id,
            'total_actors': Actors.query.count() })
        except Exception:
            db.session.rollback()
            return jsonify({'success': False,
            'deleted':None,
            'total_actors': Actors.query.count() }),404
        finally:
            db.session.close()
                

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(payload, actor_id):
        return delete_actor_helper(actor_id)

    # PATCH /actors/<id>
    def update_actors_helper(id, myrequest):
        actor = Actors.query.filter(Actors.id == id).one_or_none()
        if actor is None:
            abort(404)
    
        body = myrequest.get_json()
        if body is None:
            abort(400)

        name = body.get("name", None)
        age = body.get("age", None)
        gender = body.get("gender", None)

        if name is not None:
            actor.name = name
        
        if age is not None:
            actor.age = age

        if gender is not None:
            actor.gender = gender

        actor.update()

        return jsonify(
                {
                    'success':True,
                    'updated':actor.id,
                    'actor':actor.format()
                }
            )

    @app.route('/actors/<id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actors(payload, id):
        return update_actors_helper(id, request)

    # Error Handling

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(405)
    def notfound(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "The requested method is not allowed"
        }), 405

    @app.errorhandler(404)
    def notfound(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "The requested resource is not found"
        }), 404

    @app.errorhandler(400)
    def notfound(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400

    @app.errorhandler(500)
    def notfound(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Server Error"
        }), 500

    @app.errorhandler(AuthError)
    def autherror(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": "Authorization failed"
        }), error.status_code

    return app

app = create_app()

if __name__ == "__main__":
    app.debug = True
    app.run()
