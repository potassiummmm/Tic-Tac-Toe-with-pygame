import pygame
import sys

screen_height = 1280
screen_width = 720

board_height = 300
board_width = 300

text_font = "SimHei"

board = [[0 for i in range(3)] for j in range(3)]
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
game_over = False
winner = 0
player = 1
again_rect = pygame.Rect(900, 400, 160, 50)


def draw_board(screen):
    grid = (50, 50, 50)
    screen.fill(white)
    for x in range(0, 4):
        pygame.draw.line(screen, grid, (400, 120 + 160 * x), (880, 120 + 160 * x), 3)
        pygame.draw.line(screen, grid, (400 + 160 * x, 120), (400 + 160 * x, 600), 3)
    font = pygame.font.SysFont(text_font, 40)
    player_img = font.render("玩家1: X", True, black)
    pygame.draw.rect(screen, white, (300 // 2 - 160, 300 // 2 - 60, 200, 50))
    screen.blit(player_img, (200, 200))
    player_img = font.render("玩家2: O", True, black)
    screen.blit(player_img, (200, 400))


def init_board():
    global board
    board = [[0 for i in range(3)] for j in range(3)]


def draw_markers(screen):
    x_pos = 0
    for x in board:
        y_pos = 0
        for y in x:
            if y == 1:
                pygame.draw.line(screen, red, (x_pos * 160 + 440, y_pos * 160 + 160),
                                 (x_pos * 160 + 520, y_pos * 160 + 240), 3)
                pygame.draw.line(screen, red, (x_pos * 160 + 520, y_pos * 160 + 160),
                                 (x_pos * 160 + 440, y_pos * 160 + 240), 3)
            if y == -1:
                pygame.draw.circle(screen, green, (x_pos * 160 + 480, y_pos * 160 + 200), 50, 3)
            y_pos += 1
        x_pos += 1


def is_valid(x: int, y: int) -> bool:
    global board
    return 0 <= x < 3 and 0 <= y < 3 and board[x][y] == 0


def show_invalid_msg(screen):
    font = pygame.font.SysFont(text_font, 40)
    invalid_img = font.render("落子的位置不合法!", True, red)
    pygame.draw.rect(screen, white, (300 // 2 - 160, 300 // 2 - 60, 200, 50))
    screen.blit(invalid_img, (480, 50))


def place_marker(x: int, y: int, screen):
    global board
    global player
    if is_valid(x, y):
        board[x][y] = player
        player *= -1
        draw_board(screen)
        check_game_over()
    else:
        show_invalid_msg(screen)


def check_game_over():
    global board
    global game_over
    global winner
    x_pos = 0
    for x in board:
        if abs(sum(x)) == 3:
            winner = 1 if sum(x) == 3 else 2
            game_over = True
        if abs(board[0][x_pos] + board[1][x_pos] + board[2][x_pos]) == 3:
            winner = 1 if board[0][x_pos] == 1 else 2
            game_over = True
        x_pos += 1

    if abs(board[0][0] + board[1][1] + board[2][2]) == 3 or abs(board[2][0] + board[1][1] + board[0][2]) == 3:
        winner = 1 if board[1][1] == 1 else 2
        game_over = True

    if sum([board[i].count(0) for i in range(3)]) == 0 and not game_over:
        winner = 0
        game_over = True


def restart_game(screen):
    global game_over
    global player
    global winner
    init_board()
    draw_board(screen)

    game_over = False
    winner = 0
    player = 1


def draw_game_over(screen):
    global winner
    if winner != 0:
        end_text = "玩家 " + str(winner) + " 胜利!"
    else:
        end_text = "平局"
    font = pygame.font.SysFont(text_font, 40)
    end_img = font.render(end_text, True, black)
    pygame.draw.rect(screen, white, (300 // 2 - 160, 300 // 2 - 60, 200, 50))
    screen.blit(end_img, (900, 200))

    again_text = "再来一局"
    again_img = font.render(again_text, True, white)
    pygame.draw.rect(screen, red, again_rect)
    screen.blit(again_img, (900, 400))


def run_game():
    global player
    global winner
    global game_over
    pygame.init()
    screen = pygame.display.set_mode((screen_height, screen_width))
    pygame.display.set_caption("井字棋")
    init_board()
    draw_board(screen)
    while True:
        draw_markers(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if not game_over:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    x_pos = (pos[0] - 400) // 160
                    y_pos = (pos[1] - 120) // 160
                    place_marker(x_pos, y_pos, screen)
        if game_over:
            draw_game_over(screen)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if again_rect.collidepoint(pygame.mouse.get_pos()):
                    restart_game(screen)

        pygame.display.update()


if __name__ == '__main__':
    run_game()
