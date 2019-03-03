class PlaceInfo:

    def __init__(self, db_tuple):
        self.place_id = db_tuple[0]
        self.place_name = db_tuple[1]
        self.place_logo_path = db_tuple[2]

