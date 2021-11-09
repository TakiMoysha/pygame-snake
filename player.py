class Player:
    __slots__ = (
        'position_x',
        'position_y',
        'velocity_x',
        'velocity_y',
        'snake_len',
        'snake_body_pos_list',
    )

    def __init__(self) -> None:
        self.position_x = 0
        self.position_y = 0
        self.velocity_x = 0
        self.velocity_y = 0
        self.snake_len = 0
        self.snake_body_pos_list = list()

    def get_head_position(self):
        return (self.position_x, self.position_y)

    def get_snake_body_pos_list(self):
        body_list = list()
        body_list.append(self.get_head_position())
        if self.snake_len > 0:
            for x in self.snake_body_pos_list:
                body_list.append(x)

        return (body_list)

    def set_position(self, position_x, position_y):
        self.position_x = position_x
        self.position_y = position_y

    def change_velocity(self, vector_x, vector_y):
        def get_neck_pos_by_x():
            return (self.position_x + vector_x, self.position_y + vector_y)

        def get_neck_pos_by_y():
            return (self.position_x - vector_x, self.position_y - vector_y)

        if get_neck_pos_by_x() in self.snake_body_pos_list:
            return
        if get_neck_pos_by_y() in self.snake_body_pos_list:
            return

        self.velocity_x = vector_x
        self.velocity_y = vector_y

    def update_position(self):
        current_pos = self.get_head_position()

        if self.snake_len > 0:
            self.snake_body_pos_list.append((current_pos))
            self.snake_body_pos_list.remove(self.snake_body_pos_list[0])

        self.position_x += self.velocity_x
        self.position_y -= self.velocity_y

    def add_len(self, value):
        self.snake_len += value
        self.snake_body_pos_list.append((self.position_x, self.position_y))
