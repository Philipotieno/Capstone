from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from app.validate import validate_actor, validate_movie
from app.auth import AuthError, requires_auth

# local import
from instance.config import app_config

# initialize sql-alchemy
db = SQLAlchemy()


def create_app(config_name):
    from app.models import Actor, Movie
    """
    flask Object and returns it after it is loaded
    with the configurations settings
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def create_actors(payload):
        data = request.get_json()
        try:
            if validate_actor(data):
                return validate_actor(data)
        except(TypeError, KeyError):
            abort(400)

        # check if drink name exists
        name = request.get_json()['name'].rstrip().title()
        if Actor.query.filter_by(name=name).first():
            abort(409)

        try:
            name = ' '.join(data['name'].split())
            actor = Actor(
                name.title(),
                data['age'],
                data['gender'].rstrip().title()
            )
            actor.save()
            obj = {
                'id': actor.id,
                'name': actor.name,
                'age': actor.age,
                'gender': actor.gender
            }
            return jsonify({
                'success': True,
                'actors': [obj]
            }), 201
        except:
            abort(422)
            
    @app.route('/actors')
    def get_all_actors():
        try:
            actors = Actor.query.all()
            actors = [actor.format() for actor in actors]
            
            return jsonify({
                'success': True,
                'actors': actors
            }), 200
        except:
            abort(422)

    @app.route('/actors/<int:id>')
    def get_one_actor(id):
        actor = Actor.query.filter(Actor.id == id).one_or_none()
        if actor:
            try:
                obj = {
                    'id': actor.id,
                    'name': actor.name,
                    'age': actor.age,
                    'gender': actor.gender
                }
                return jsonify({
                    'success': True,
                    'actor': obj
                }), 201
            except:
                abort(422)
        else:
            abort(404)

    @app.route('/actors/<int:id>', methods=['DELETE'])
    def delete_actor(id):
        actor = Actor.query.filter(Actor.id == id).first()
        if actor:
            try:
                actor.delete()
                return jsonify({
                    'success': True,
                    'deleted': id
                }), 201
            except:
                abort(422)
        else:
            abort(404)
    # Error Handling

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad request"
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource not found"
        }), 404

    @app.errorhandler(409)
    def duplicate(error):
        return jsonify({
            "success": False,
            "error": 409,
            "message": "Duplicate found"
        }), 409

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable"
        }), 422
        
    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error
        }), error.status_code
        
    return app
