from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from app.validate import validate_actor, validate_movie

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
    def create_actors():
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

    return app
