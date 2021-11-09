import time

import pygame

from player import Player
from consts import CELLSIZE, BLUE, RED, WHITE, SCALINGTEXTTODISPLAY, GAMESPEED
from spawner import Spawner

# ===========Initial game=============
key_game_control = {
    pygame.K_LEFT: lambda:
        player.change_velocity(vector_x=(-1 * CELLSIZE), vector_y=0),
    pygame.K_RIGHT: lambda:
        player.change_velocity(vector_x=CELLSIZE, vector_y=0),
    pygame.K_UP: lambda:
        player.change_velocity(vector_x=0, vector_y=CELLSIZE),
    pygame.K_DOWN: lambda:
        player.change_velocity(vector_x=0, vector_y=(-1 * CELLSIZE)),
    pygame.K_ESCAPE: lambda: on_game_over(),
}

debug_key_control = {
    pygame.K_F1: lambda *args: print(f"Debug message: {args}"),
    pygame.K_F2: lambda: print(
            [player.__getattribute__(atr) for atr in player.__slots__]
        ),
    pygame.K_F3: lambda: player.add_len(1),
    pygame.K_F4: lambda: spawner.create_new_pos()
}

dispaly_size = {
    "width": 800,
    "height": 400
}
center_level_point = (
    int(dispaly_size.get("width")/2),
    int(dispaly_size.get("height")/2)
)

global player
player = Player()
player.set_position(*center_level_point)

global spawner
spawner = Spawner(*dispaly_size.values())

pygame.init()

DISPLAYSURF = pygame.display.set_mode(tuple(dispaly_size.values()))
pygame.display.update()
clock = pygame.time.Clock()

# Flags
food_exist = False
game_over = False


# ===========Functions=============
def on_game_over():
    global game_over
    game_over = True


def on_food_created():
    global food_exist
    food_exist = True


def control_key_handler(event_key):
    if event_key in key_game_control:
        key_game_control.get(event_key)()
    elif event_key in debug_key_control:
        debug_key_control.get(event_key)()


def display_surf_update():
    def draw_snake():
        snake_pos_list = player.get_snake_body_pos_list()
        for pos in snake_pos_list:
            pygame.draw.rect(DISPLAYSURF, BLUE, [*pos, CELLSIZE, CELLSIZE])

    def draw_food():
        food_pos = spawner.current_pos
        pygame.draw.rect(DISPLAYSURF, RED, [*food_pos, CELLSIZE, CELLSIZE])

    DISPLAYSURF.fill(WHITE)
    draw_food()
    draw_snake()


def player_eat_food():
    player.add_len(1)
    spawner.create_new_pos()


def is_player_pos_in_out_game_field(x, y) -> bool:
    if dispaly_size.get("width") - CELLSIZE < x or x < 0:
        return True
    elif dispaly_size.get("height") - CELLSIZE < y or y < 0:
        return True

    return False


def is_player_faced_with_himself(x, y) -> bool:
    if (x, y) in player.snake_body_pos_list:
        return True

    return False


def message(msg, color, text_bias_y=0):
    font_style = pygame.font.SysFont(None, 30)
    text = font_style.render(msg, True, color)
    text_bias_x = len(msg) * SCALINGTEXTTODISPLAY
    x_text_pos = dispaly_size.get("width")/2 - text_bias_x
    y_text_pos = dispaly_size.get("height")/2 - text_bias_y
    center_coord_text = [x_text_pos, y_text_pos]
    DISPLAYSURF.blit(text, center_coord_text)


def end_game():
    message(f"Record: {player.snake_len}", RED, -30)
    message("End game", RED)
    pygame.display.update()
    time.sleep(1)
    pygame.quit()
    quit()


# ===========Game Loop=============
def start_game_loop():
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                on_game_over()
            elif event.type == pygame.KEYDOWN:
                control_key_handler(event.key)

        if not food_exist:
            spawner.create_new_pos()
            while spawner.current_pos in player.get_snake_body_pos_list():
                spawner.create_new_pos()
            on_food_created()

        display_surf_update()
        player.update_position()
        pygame.display.update()

        x, y = player.get_head_position()

        if spawner.current_pos == player.get_head_position():
            player_eat_food()
        elif is_player_pos_in_out_game_field(x, y):
            on_game_over()
        elif is_player_faced_with_himself(x, y):
            on_game_over()

        clock.tick(GAMESPEED)

    end_game()


if __name__ == "__main__":
    start_game_loop()
