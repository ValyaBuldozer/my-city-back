class Answer:

    def __init__(self, id, title, is_right, description):
        self.id = id
        self.title = title
        self.is_right = True if is_right == 1 else False
        self.description = description
