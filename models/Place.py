from models.RouteInfo import RouteInfo

class Place:

    def __init__(self, p_id, name, logo_path, image_path, description, question_title, address):
        self.place_id = p_id
        self.place_name = name
        self.place_logo_path = logo_path
        self.place_image_path = image_path
        self.place_description = description
        self.question_title = question_title
        self.place_address = address
        self.place_routes = []
        self.place_answers = []

    def __init__(self, init_tuple):
        self.place_id = init_tuple[0]
        self.place_name = init_tuple[1]
        self.place_logo_path = init_tuple[2]
        self.place_image_path = init_tuple[3]
        self.place_description = init_tuple[4]
        self.place_question_title = init_tuple[5]
        self.place_address = init_tuple[6]
        self.place_routes = []
        self.place_answers = []

    def add_route(self, route):
        self.place_routes.append(route.__dict__)

    def add_answer(self, answer):
        self.place_answers.append(answer.__dict__)

    def set_route_from_db_tuple(self, db_tuple):
        for db_row in db_tuple:
            self.add_route(RouteInfo(db_row))

