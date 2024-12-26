import pygame
import random
from objects import Snake, Fruit

# Window size
window_x = 720
window_y = 480

# defining colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

pygame.init()
pygame.display.set_caption("Snake by radagv")

surface = pygame.display.set_mode((window_x, window_y))
fps = pygame.time.Clock()

paused = False
running = True

player_1 = Snake("Fermarys", surface=surface, color=green, position=[100, 50])
player_2 = Snake(
    "Angel",
    surface=surface,
    color=blue,
    position=[window_x - 100, 50],
    start_direction="LEFT",
)

player_2.setup_keys(up=pygame.K_w, right=pygame.K_d, bottom=pygame.K_s, left=pygame.K_a)

fruit = Fruit(surface=surface)

players = [player_1, player_2][0:2]


# displaying Score function
def show_score(color, font, size):

    # creating font object score_font
    for index, player in enumerate(players):
        score_font = pygame.font.SysFont(font, size)

        # create the display surface object
        # score_surface
        score_surface = score_font.render(
            f"{player.name} : " + str(player.score), True, color
        )

        # create a rectangular object for the
        # text surface object
        score_rect = score_surface.get_rect()

        # displaying text
        surface.blit(
            score_surface,
            pygame.Rect(
                10.0,
                float(index * score_rect.height),
                score_rect.width,
                score_rect.height,
            ),
        )


def game_over(ofplayer: Snake):

    global running
    # creating font object my_font
    my_font = pygame.font.SysFont("times new roman", 50)

    # creating a text surface on which text
    # will be drawn
    game_over_surface = my_font.render(
        f"{ofplayer.name} Your Score is : " + str(ofplayer.score), True, red
    )

    # create a rectangular object for the text
    # surface object
    game_over_rect = game_over_surface.get_rect()

    # setting position of the text
    game_over_rect.midtop = (window_x // 2, window_y // 4)

    # blit will draw the text on screen
    surface.blit(game_over_surface, game_over_rect)
    pygame.display.flip()

    # after 2 seconds we will quit the
    # program
    # time.sleep(2)

    # deactivating pygame library
    # pygame.quit()
    running = False

    # quit the program
    # quit()


def initialize():
    global running
    global paused

    for player in players:
        player.score = 0
        player.position = [100, 50]
        player.direction = "RIGHT"
        player.change_to = player.direction
        player.body = [[100, 50], [90, 50], [80, 50]]

    fruit.position = [
        random.randrange(1, (window_x // 10)) * 10,
        random.randrange(1, (window_y // 10)) * 10,
    ]

    paused = False


while True:
    # handling key events
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                paused = not paused

            if event.key == pygame.K_r and not running:
                initialize()

            for player in players:
                player.setup_movement(event)

    # If two keys pressed simultaneously
    # we don't want snake to move into two directions
    # simultaneously
    # if not paused:
    for player in players:
        if not paused:
            player.move()

        # Snake body growing mechanism
        # if fruits and snakes collide then scores will be
        # incremented by 10
        player.setup_collissions(fruit=fruit)

    if not fruit.should_spawn:
        fruit.position = [
            random.randrange(1, (window_x // 10)) * 10,
            random.randrange(1, (window_y // 10)) * 10,
        ]

    fruit.should_spawn = True

    surface.fill(black)

    # if not paused:
    for player in players:
        # if not paused:
        player.draw()

    pygame.draw.rect(
        surface, white, pygame.Rect(fruit.position[0], fruit.position[1], 10, 10)
    )

    # Game Over conditions
    for player in players:
        if player.did_collide_with_borders():
            game_over(ofplayer=player)

    # Touching the snake body
    # for block in player_1.body[1:]:
    #     if player_1.position[0] == block[0] and player_1.position[1] == block[1]:
    #         game_over()

    # displaying score continuously
    show_score(white, "times new roman", 20)

    # Refresh game screen
    pygame.display.update()

    # Frame Per Second /Refresh Rate
    fps.tick((player_1.speed + player_2.speed) // 2)
