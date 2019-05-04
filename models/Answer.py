class Answer:

    def __init__(self, a_id, title, is_right, description):
        self.id = a_id
        self.title = title
        self.is_right = is_right
        self.description = description

    def __init__(self, db_tuple):
        self.id = db_tuple[0]
        self.title = db_tuple[1]
        self.is_right = True if db_tuple[2] == 1 else False
        self.description = db_tuple[3]
