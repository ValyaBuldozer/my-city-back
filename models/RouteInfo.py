class RouteInfo:

    def __init__(self, r_id, name, logo_path):
        self.route_id = r_id
        self.route_name = name
        self.route_logo_path = logo_path
        self.route_places = []

    def __init__(self, r_tuple):
        self.route_id = r_tuple[0]
        self.route_name = r_tuple[1]
        self.route_logo_path = r_tuple[2]
        self.route_places = []

    def set_places(self, places):
        self.route_places = places


