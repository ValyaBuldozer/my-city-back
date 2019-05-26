class RouteInfo:

    def __init__(self, id, name, logo_path, places=None):
        self.id = id
        self.name = name
        self.logo_path = logo_path
        self.places = places if places is not None else []

    def set_places(self, places):
        self.places = places


