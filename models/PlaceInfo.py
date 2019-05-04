class PlaceInfo:

    def __init__(self, db_tuple):
        self.id = db_tuple[0]
        self.name = db_tuple[1]
        self.logo_path = db_tuple[2]
        self.lat = str(db_tuple[3]) if db_tuple[3] is not None else None
        self.lng = str(db_tuple[4]) if db_tuple[4] is not None else None

