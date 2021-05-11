import sys
import math
import pygame

LIGHT_BROWN = (218, 185, 154)
DARK_BROWN = (72, 46, 39)
YELLOW = (255, 255, 0)
PIECE_IMAGES = [
    None,
    pygame.image.load(r"assets/Chess_klt60.png"),
    pygame.image.load(r"assets/Chess_qlt60.png"),
    pygame.image.load(r"assets/Chess_blt60.png"),
    pygame.image.load(r"assets/Chess_rlt60.png"),
    pygame.image.load(r"assets/Chess_nlt60.png"),
    pygame.image.load(r"assets/Chess_plt60.png"),
    pygame.image.load(r"assets/Chess_kdt60.png"),
    pygame.image.load(r"assets/Chess_qdt60.png"),
    pygame.image.load(r"assets/Chess_bdt60.png"),
    pygame.image.load(r"assets/Chess_rdt60.png"),
    pygame.image.load(r"assets/Chess_ndt60.png"),
    pygame.image.load(r"assets/Chess_pdt60.png"),
]


def render(screen, board, selected_tile):
    screen.fill((255, 255, 255))
    for row in range(8):
        for col in range(8):
            color = LIGHT_BROWN
            if col % 2 != row % 2:
                color = DARK_BROWN
            if (
                selected_tile
                and selected_tile[0] == col
                and selected_tile[1] == row
            ):
                color = YELLOW
            pygame.draw.rect(
                screen, color, (60 + col * 60, 60 + row * 60, 60, 60)
            )

            if board[row][col] != 0:
                screen.blit(
                    PIECE_IMAGES[board[row][col]],
                    (60 + col * 60, 60 + row * 60),
                )


def handle_mouse(pos):
    if pos[0] < 60 or pos[0] > 540 or pos[1] < 60 or pos[1] > 540:
        return None
    return (math.floor(pos[0] / 60) - 1, math.floor(pos[1] / 60) - 1)


def main():
    pygame.init()

    board = [
        [10, 11, 9, 8, 7, 9, 11, 10],
        [12, 12, 12, 12, 12, 12, 12, 12],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [6, 6, 6, 6, 6, 6, 6, 6],
        [4, 5, 3, 2, 1, 3, 5, 4],
    ]
    screen = pygame.display.set_mode((600, 600))
    selected_tile = None
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                index = handle_mouse(pos)
                if (
                    board[index[1]][index[0]] != 0
                    and board[index[1]][index[0]] <= 6
                ):
                    selected_tile = index
                else:
                    selected_tile = None

        render(screen, board, selected_tile)
        pygame.display.update()


if __name__ == "__main__":
    main()
