from models.RouteInfo import RouteInfo


class Place:

    def __init__(self, p_id, name, logo_path, image_path, description, question_title, address):
        self.id = p_id
        self.name = name
        self.logo_path = logo_path
        self.image_path = image_path
        self.description = description
        self.question_title = question_title
        self.address = address
        self.routes = []
        self.answers = []

    def __init__(self, init_tuple):
        self.id = init_tuple[0]
        self.name = init_tuple[1]
        self.logo_path = init_tuple[2]
        self.image_path = init_tuple[3]
        self.description = init_tuple[4]
        self.question_title = init_tuple[5]
        self.address = init_tuple[6]
        self.routes = []
        self.answers = []

    def add_route(self, route):
        self.routes.append(route.__dict__)

    def add_answer(self, answer):
        self.answers.append(answer.__dict__)

    def set_route_from_db_tuple(self, db_tuple):
        for db_row in db_tuple:
            self.add_route(RouteInfo(db_row))


