class PlaceInfo:

    def __init__(self, db_tuple):
        self.place_id = db_tuple[0]
        self.place_name = db_tuple[1]
        self.place_logo_path = db_tuple[2]
        self.place_lat = str(db_tuple[3]) if db_tuple[3] is not None else None
        self.place_lng = str(db_tuple[4]) if db_tuple[4] is not None else None

