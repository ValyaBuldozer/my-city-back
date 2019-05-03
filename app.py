from flask import Flask, abort, request
from database import DbConnection
import logging
import json

app = Flask(__name__)

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


@app.route('/')
def root():
    return 'My city!'


@app.route('/static/<path:path>', methods=['GET'])
def get_static(path):
    return app.send_static_file(path)


@app.route('/db/routes', methods=['GET'])
def get_all_routes():
    query_result = db.fetch_all_routes()
    return json.dumps(query_result)


@app.route('/db/places', methods=['GET'])
def get_db_places():
    query_result = db.fetch_all_places()
    return json.dumps(query_result)


@app.route('/db/route', methods=['PUT'])
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


@app.route('/db/place/<place_id>/answers', methods=['PUT'])
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


@app.route('/db/place', methods=['PUT'])
def put_new_place():
    content = request.json
    name = content['name']
    logo_path = content['logo_path']
    image_path = content['image_path']
    description = content['description']
    question_title = content['question_title']
    address = content['address']
    answers = content['answers']
    routes = content['routes']

    if name is None or logo_path is None or image_path is None:
        return abort(400, 'Invalid request')

    result = db.insert_new_place(
        name, logo_path, image_path, description, question_title, address, answers, routes
    )

    if result == 0:
        return 'Success.'
    if result == 1:
        return abort(400, 'Invalid place data')
    elif result == 2:
        return abort(400, 'Invalid answers data. Place was added.')
    elif result == 3:
        return abort(400, 'Invalid routes data. Place was added')
    else:
        return abort(500, 'Unknown error')


@app.route('/places', methods=['GET'])
def get_places():
    places = db.fetch_places_info()
    return to_json(places)


@app.route('/routes', methods=['GET'])
def get_routes():
    routes = db.fetch_routes_info()
    return to_json(routes)


@app.route('/places/<place_id>', methods=['GET'])
def get_place_by_id(place_id):
    place = db.fetch_place(place_id)

    if place is None:
        return abort(404, 'Place not found.')

    return to_json(place)


if __name__ == '__main__':
    logging.basicConfig(filename='my_city.log', level=logging.DEBUG)
    app.run(host="0.0.0.0", port="5000")
