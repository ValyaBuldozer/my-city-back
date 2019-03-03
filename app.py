from flask import Flask, abort, request
from flaskext.mysql import MySQL
from models.Place import Place
from models.PlaceInfo import PlaceInfo
from models.RouteInfo import RouteInfo
from models.Answer import Answer
import json

app = Flask(__name__)

with open('dbconfig.json') as config_file:
	db_config = json.load(config_file)

mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = db_config["user"]
app.config['MYSQL_DATABASE_PASSWORD'] = db_config["password"]
app.config['MYSQL_DATABASE_DB'] = db_config["db_name"]
app.config['MYSQL_DATABASE_HOST'] = db_config["host"]
mysql.init_app(app)

db_connection = mysql.connect()
db_cursor = db_connection.cursor()


insert_new_place = """
    INSERT INTO places (
        place_name, 
        place_logo_path, 
        place_image_path, 
        place_description, 
        place_question_title,
        place_address) 
      VALUES ("{0}", "{1}", "{2}", "{3}", "{4}", "{5}");
      """

insert_new_answer = """
    INSERT INTO answer (
        place_id, 
        answer_title, 
        answer_is_right, 
        answer_description
    )
    VALUES ("{0}", "{1}", "{2}", "{3}");
"""

select_place_routes = """
    SELECT route_id, route_name, route_logo_path
    FROM routes NATURAL JOIN route_place
    WHERE place_id = "{0}";
"""

select_place_by_id = """
    SELECT *
    FROM places
    WHERE place_id = "{0}";
"""

select_route_places = """
    SELECT place_id
    FROM route_place
    WHERE route_id = "{0}"
"""

select_answers_by_place = """
    SELECT answer_id, answer_title, answer_is_right, answer_description
    FROM answer
    WHERE place_id = "{0}"
"""


@app.route('/')
def hello_world():
    return 'My city!'


@app.route('/static/<path:path>', methods=['GET'])
def get_static(path):
    return app.send_static_file(path)


@app.route('/db/routes', methods=['GET'])
def get_all_routes():
    db_cursor.execute('SELECT * FROM routes')
    query_result = db_cursor.fetchall()
    return json.dumps(query_result)


@app.route('/db/places', methods=['GET'])
def get_db_places():
    db_cursor.execute('SELECT * FROM places')
    query_result = db_cursor.fetchall()
    return json.dumps(query_result)


@app.route('/db/route', methods=['PUT'])
def put_new_route():
    content = request.json

    name = content['name']
    logo_path = content['logo_path']

    if name is None or logo_path is None:
        return abort(400, 'invalid data')

    db_cursor.execute(
        'INSERT INTO routes (route_name, route_logo_path) VALUES ("{0}", "{1}")'.format(
            name, logo_path
        )
    )
    db_connection.commit()

    return 'Success!'


@app.route('/db/place/<place_id>/answers', methods=['PUT'])
def put_new_answer(place_id):
    content = request.json

    if not isinstance(content, list):
        return abort(400, 'INVALID DATA')

    for content_answer in content:
        db_request = insert_new_answer.format(
            place_id,
            content_answer['title'],
            1 if content_answer['is_right'] else 0,
            content_answer['description']
        )
        db_cursor.execute(db_request)
        db_connection.commit()

    return 'Success'


@app.route('/places/all', methods=['GET'])
def get_all_places():
    db_cursor.execute('SELECT * FROM places')
    query_result = db_cursor.fetchall()

    result_arr = []
    for row in query_result:
        result_arr.append(Place(row))

    for place in result_arr:
        db_cursor.execute(select_place_routes.format(place.place_id))
        place.set_route_from_db_tuple(db_cursor.fetchall())

    return json.dumps(result_arr, default=lambda obj: obj.__dict__)


@app.route('/places/', methods=['GET'])
def get_places():
    db_cursor.execute('SELECT place_id, place_name, place_logo_path FROM places')
    query_result = db_cursor.fetchall()

    result_arr = []
    for row in query_result:
        result_arr.append(PlaceInfo(row).__dict__)

    return json.dumps(result_arr)


@app.route('/routes', methods=['GET'])
def get_routes():
    db_cursor.execute('SELECT route_id, route_name, route_logo_path FROM routes')
    query_result = db_cursor.fetchall()

    result_arr = []
    for row in query_result:
        result_arr.append(RouteInfo(row))

    for route in result_arr:
        db_cursor.execute(select_route_places.format(route.route_id))
        route_places = db_cursor.fetchall()
        route.set_places(list(map(lambda places: places[0], route_places)))

    return json.dumps(result_arr, default=lambda obj: obj.__dict__)


@app.route('/places/<place_id>', methods=['GET'])
def get_place_by_id(place_id):
    # base place info
    db_cursor.execute(select_place_by_id.format(place_id))
    query_result = db_cursor.fetchall()

    if len(query_result) == 0:
        abort(404)
        return "NOT FOUND"

    place = Place(query_result[0])

    # add place's routes
    db_cursor.execute(select_place_routes.format(place_id))
    routes_query_result = db_cursor.fetchall()

    for routes_row in routes_query_result:
        # selecting all places for single route by id
        db_cursor.execute(select_route_places.format(routes_row[0]))
        route_places_result = db_cursor.fetchall()
        route = RouteInfo(routes_row)

        # fetching only place_id, not tuple
        route.set_places(list(map(lambda db_tuple: db_tuple[0], route_places_result)))
        place.add_route(route)

    # add places's answers
    db_cursor.execute(select_answers_by_place.format(place_id))
    answers_query_result = db_cursor.fetchall()

    for answer_query_row in answers_query_result:
        answer = Answer(answer_query_row)
        place.add_answer(answer)

    return json.dumps(place, default=lambda obj: obj.__dict__)


@app.route('/db/place', methods=['PUT'])
def put_new_place():
    content = request.json
    name = content['name']
    logo_path = content['logo_path']
    image_path = content['image_path']
    description = content['description']
    question_title = content['question_title']
    address = content['address']

    if name is None or logo_path is None or image_path is None:
        return abort(400, 'Invalid request')

    insert_request = insert_new_place.format(
            name, logo_path, image_path, description, question_title, address
        )

    db_cursor.execute(insert_request)
    db_connection.commit()

    return "Successes!"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
