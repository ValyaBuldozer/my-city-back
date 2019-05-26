from models.RouteInfo import RouteInfo


class Place:

    def __init__(self, p_id, name, logo_path, image_path, description, question_title, address,
                 routes=None, answers=None):
        self.id = p_id
        self.name = name
        self.logo_path = logo_path
        self.image_path = image_path
        self.description = description
        self.question_title = question_title
        self.address = address
        self.routes = routes if routes is not None else []
        self.answers = answers if answers is not None else []

    def add_route(self, route):
        self.routes.append(route.__dict__)

    def add_answer(self, answer):
        self.answers.append(answer.__dict__)

    def set_route_from_db_tuple(self, db_tuple):
        for db_row in db_tuple:
            self.add_route(RouteInfo(db_row))


