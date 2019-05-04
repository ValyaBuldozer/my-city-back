from flaskext.mysql import MySQL
from typing import List, TypeVar
from models.Answer import Answer
from models.PlaceInfo import PlaceInfo
from models.Place import Place
from models.RouteInfo import RouteInfo


class DbConnection:

    def __init__(self, db_config, flask_app):
        mysql = MySQL()

        flask_app.config['MYSQL_DATABASE_USER'] = db_config["user"]
        flask_app.config['MYSQL_DATABASE_PASSWORD'] = db_config["password"]
        flask_app.config['MYSQL_DATABASE_DB'] = db_config["db_name"]
        flask_app.config['MYSQL_DATABASE_HOST'] = db_config["host"]

        mysql.init_app(flask_app)

        self._connection = mysql.connect()
        self._cursor = self._connection.cursor()

    def __fetch_from_procedure(self, procedure_name, *args):
        self._cursor.callproc(procedure_name, args)
        return self._cursor.fetchall()

    def __exec_procedure(self, procedure_name, *args):
        # first proc argument - result
        result_args = self._cursor.callproc(procedure_name, [0, *args])
        return result_args

    def fetch_all_routes(self):
        return self.__fetch_from_procedure('get_all_routes')

    def fetch_all_places(self):
        return self.__fetch_from_procedure('get_full_places')

    def fetch_places_info(self) -> List[PlaceInfo]:
        raw_result = self.__fetch_from_procedure('get_places_info')
        return list(map(lambda db_tuple: PlaceInfo(db_tuple), raw_result))

    def fetch_routes_info(self) -> List[RouteInfo]:
        raw_result = self.__fetch_from_procedure('get_routes_info')
        result = []

        for row in raw_result:
            route = RouteInfo(row)
            route.set_places(self.fetch_places_by_route(route.id))
            result.append(route)

        return result

    def fetch_routes_by_place(self, place_id):
        return self.__fetch_from_procedure('get_routes_by_place', place_id)

    def fetch_places_by_route(self, route_id):
        return list(map(
            lambda raw_place: PlaceInfo(raw_place),
            self.__fetch_from_procedure('get_places_by_route', route_id)
        ))

    def fetch_place(self, place_id) -> Place:
        place_raw = self.__fetch_from_procedure('get_place', place_id)

        if len(place_raw) == 0:
            return None

        place = Place(place_raw[0])

        # fetching routes
        routes_raw = self.__fetch_from_procedure('get_routes_by_place', place.id)
        place.routes = list(map(lambda route: RouteInfo(route), routes_raw))

        # fetching answers
        answers_raw = self.__fetch_from_procedure('get_answers_by_place', place.id)
        place.answers = list(map(lambda answer: Answer(answer), answers_raw))

        return place

    def fetch_answers_by_place(self, place_id):
        return self.__fetch_from_procedure('get_answers_by_place', place_id)

    def insert_new_route(self, route_name, route_logo_path):
        return self.__exec_procedure('put_new_route', route_name, route_logo_path)[0]

    def insert_new_answer(self, place_id, title, is_right, description):
        is_right = 1 if is_right else 0
        return self.__exec_procedure('put_new_answer', place_id, title, is_right, description)[0]

    def insert_new_place(self, name: str, logo_path: str, image_path: str,
                         description: str, question_title: str, address: str,
                         answers: List[Answer], routes: List[int]) -> int:
        place_args = self.__exec_procedure('put_new_place', name, logo_path, image_path, description, question_title, address)

        if place_args[0] != 0:
            return 1

        # selecting inserted place id from out args
        place_id = place_args[1]

        # inserting answers
        if answers is not None:
            for answer in answers:
                result = self.insert_new_answer(place_id, answer.title, answer.is_right, answer.answer_description)
                if result != 0:
                    return 2

        # inserting routes
        if routes is not None:
            for route_id in routes:
                result = self.__exec_procedure('put_place_route', place_id, route_id)
                if result[0] != 0:
                    return 3

        return 0

    def delete_route(self, route_id):
        return self.__exec_procedure('drop_route', route_id)[0]

    def delete_place(self, place_id):
        return self.__exec_procedure('drop_place', place_id)[0]

