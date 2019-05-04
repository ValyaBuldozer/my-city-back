class RouteInfo:

    def __init__(self, r_id, name, logo_path):
        self.id = r_id
        self.name = name
        self.logo_path = logo_path
        self.places = []

    def __init__(self, r_tuple):
        self.id = r_tuple[0]
        self.name = r_tuple[1]
        self.logo_path = r_tuple[2]
        self.places = []

    def set_places(self, places):
        self.places = places


