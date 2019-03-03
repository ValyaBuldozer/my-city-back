class Answer:

    def __init__(self, a_id, title, is_right, description):
        self.answer_id = a_id
        self.answer_title = title
        self.answer_is_right = is_right
        self.answer_description = description

    def __init__(self, db_tuple):
        self.answer_id = db_tuple[0]
        self.answer_title = db_tuple[1]
        self.answer_is_right = True if db_tuple[2] == 1 else False
        self.answer_description = db_tuple[3]
