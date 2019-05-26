from flask import Flask, abort, request, jsonify
from werkzeug.utils import secure_filename
from models.Place import Place
from models.RouteInfo import RouteInfo
from models.Answer import Answer
from database import DbConnection
import logging
import json
import os
import uuid

app = Flask(__name__)

UPLOAD_PATH = 'UPLOAD_PATH'
ALLOWED_EXTENSIONS = 'ALLOWED_EXTENSIONS'
DIRNAME = os.path.dirname(os.path.abspath(__file__))
app.config[UPLOAD_PATH] = 'static'
app.config[ALLOWED_EXTENSIONS] = {'png', 'jpg', 'jpeg'}

with open('dbconfig.json') as config_file:
    db_config = json.load(config_file)

db = DbConnection(db_config, app)


# TODO(remove indents in production)
def to_json(obj):
    return json.dumps(
        obj,
        default=lambda o: o.__dict__,
        ensure_ascii=False,
        indent=4
    ).encode('utf-8')


def shutdown_server():
    db.close()

    shutdown_func = request.environ.get('werkzeug.server.shutdown')
    if shutdown_func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    shutdown_func()


@app.errorhandler(400)
def log_error(error):
    message = error.description
    app.logger.error(message)

    return error


@app.route('/')
def root():
    return 'My city!'


@app.route('/shutdown', methods=['GET'])
def shutdown():
    shutdown_server()
    return "Good night, sweet prince..."


@app.route('/static/<path:path>', methods=['GET'])
def get_static(path):
    return app.send_static_file(path)


@app.route('/static/', methods=['PUT'])
def upload_file():
    if 'file' not in request.files:
        return abort(400, 'No files to save')

    file = request.files['file']

    if file.filename == '':
        return abort(400, 'No files to save')

    ext = file.filename.rsplit('.', 1)[::-1][0]

    if ext not in app.config[ALLOWED_EXTENSIONS]:
        return abort(400, 'This file type is not allowed')

    file.filename = str(uuid.uuid1()) + '.' + ext
    file.save(os.path.join(DIRNAME, app.config[UPLOAD_PATH], file.filename))

    # add static path for real URL
    return 'static/' + file.filename


@app.route('/api/places', methods=['GET'])
def get_places():
    places = db.fetch_places_info()
    return to_json(places)


@app.route('/api/routes', methods=['GET'])
def get_routes():
    routes = db.fetch_routes()
    return to_json(routes)


@app.route('/api/places/<place_id>', methods=['GET'])
def get_place_by_id(place_id):
    place = db.fetch_place(place_id)

    if place is None:
        return abort(404, 'Place not found.')

    return to_json(place)


@app.route('/admin/places', methods=['GET'])
def get_full_places():
    places = db.fetch_full_places()
    return to_json(places)


@app.route('/admin/routes', methods=['GET'])
def get_full_routes():
    routes = db.fetch_routes()
    return to_json(routes)


@app.route('/admin/routes', methods=['PUT'])
def put_new_route():
    content = request.json
    name = content['name']
    logo_path = content['logo_path']

    if name is None or logo_path is None:
        return abort(400, 'invalid data')

    result = db.insert_new_route(name, logo_path)

    if result != 0:
        return abort(400, 'Something goes wrong...')

    return 'Success!'


@app.route('/admin/place/<place_id>/answers', methods=['PUT'])
def put_new_answer(place_id):
    content = request.json

    if not isinstance(content, list):
        return abort(400, 'INVALID DATA')

    for content_answer in content:
        result = db.insert_new_answer(
            place_id,
            content_answer['title'],
            content_answer['is_right'],
            content_answer['description']
        )
        if result != 0:
            return abort(400, 'Something goes wrong...')

    return 'Success'


@app.route('/admin/places', methods=['PUT'])
def put_new_place():
    content = request.json
    place = Place(
        p_id=content['id'],
        name=content['name'],
        logo_path=content['logo_path'],
        image_path=content['image_path'],
        description=content['description'],
        question_title=content['question_title'],
        address=content['address'],
        answers=list(map(lambda ans: Answer(ans['id'], ans['title'], ans['is_right'], ans['description']), content['answers'])),
        routes=list(map(lambda route: RouteInfo(route['id'], route['name'], route['logo_path']), content['routes']))
    )

    result = db.insert_new_place(place)

    if result == 1:
        return abort(400, 'Invalid place data')
    elif result == 2:
        return abort(400, 'Invalid answers data. Place was added.')
    elif result == 3:
        return abort(400, 'Invalid routes data. Place was added')
    else:
        # return place id todo(need something else here)
        return to_json(result)


@app.route('/admin/routes/<route_id>', methods=['DELETE'])
def delete_route(route_id):
    result = db.delete_route(route_id)

    if result != 0:
        return abort(404, 'Route not found')

    return 'Success'


@app.route('/admin/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    result = db.delete_place(place_id)

    if result != 0:
        return abort(404, 'Place not found')

    return 'Success'


@app.route('/admin/routes/<route_id>', methods=['POST'])
def update_route(route_id):
    content = request.json

    result = db.update_route(
        route_id,
        content['name'],
        content['logo_path']
    )

    if result == 1:
        return abort(404, 'Route not found')
    else:
        return 'Success'


@app.route('/admin/places/<place_id>', methods=['POST'])
def update_place(place_id):
    content = request.json

    result = db.update_place(Place(
        place_id,
        content['name'],
        content['logo_path'],
        content['image_path'],
        content['description'],
        content['question_title'],
        content['address'],
        list(map(lambda route: RouteInfo(**route), content['routes'])),
        list(map(lambda answer: Answer(**answer), content['answers']))
    ))

    if result is None:
        return abort(400, 'Invalid request')
    else:
        return to_json(result)


if __name__ == '__main__':
    logging.basicConfig(filename='my_city.log', level=logging.DEBUG)
    app.run(host="0.0.0.0", port="5000")
