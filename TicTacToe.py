import pygame
from pygame.locals import *
import time
import random

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)

x_size, y_size = 500, 500
res = (x_size, y_size)
FPS = 30
pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption("Hello World")
window_surface = pygame.display.set_mode(res, pygame.DOUBLEBUF)
window_surface.fill(white)
player = 1
running = True
won = False
finish_timer = 0

cases = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

pygame.font.init()
myfont = pygame.font.SysFont('Arial', 50)
myfont_small = pygame.font.SysFont('Arial', 30)

Circle_win_text_surface = myfont.render('Circle win', False, black)
Cross_win_text_surface = myfont.render('Cross win', False, black)
No_one_win_text_surface = myfont.render('No one win', False, black)


def play(players, case):
    if players == 1:
        draw_cross(case[0], case[1])
        cases[case[0]][case[1]] = 1
    elif players == 2:
        draw_circle(case[0] + 1, case[1] + 1)
        cases[case[0]][case[1]] = 2
        print('auto play in ', case)
        print('-------------------------------')


def draw_back_lines():
    pygame.draw.line(window_surface, black, (167, 0), (167, 500), 5)
    pygame.draw.line(window_surface, black, (332, 0), (332, 500), 5)
    pygame.draw.line(window_surface, black, (0, 167), (500, 167), 5)
    pygame.draw.line(window_surface, black, (0, 332), (500, 332), 5)


def draw_cross(column, line):
    pygame.draw.line(window_surface, red, (15 + 167 * (column - 1), 15 + 167 * (line - 1)),
                     (151 + 167 * (column - 1), 151 + 167 * (line - 1)), 10)
    pygame.draw.line(window_surface, red, (151 + 167 * (column - 1), 15 + 167 * (line - 1)),
                     (15 + 167 * (column - 1), 151 + 167 * (line - 1)), 10)


def draw_circle(column, line):
    pygame.draw.circle(window_surface, blue, (83 + 167 * (column - 1), 83 + 167 * (line - 1)), 72, 10)


def verify_winn():
    for way in range(2):
        for players in range(2):
            for x in range(3):
                count = 0
                for y in range(3):
                    if way == 0:
                        if cases[x][y] == players + 1:
                            count += 1
                    elif way == 1:
                        if cases[y][x] == players + 1:
                            count += 1
                if count == 3:
                    return True, players+1

    for way in range(2):
        for players in range(2):
            count = 0
            for i in range(3):
                if way == 0:
                    if cases[i][i] == players + 1:
                        count += 1
                elif way == 1:
                    if cases[2 - i][i] == players + 1:
                        count += 1
            if count == 3:
                return True, players+1

    final_count = 0
    for x in range(3):
        for y in range(3):
            if cases[x][y] != 0:
                final_count += 1
    if final_count == 9:
        return True, 0
    return False


def search_two_in_line(players=1):
    player2 = 2
    if players == 1:
        player2 = 2
    elif players == 2:
        player2 = 1
    elif players == 0:
        # noinspection PyStatementEffect
        player2 == 1

    for way in range(2):
        for x in range(3):
            count = 0
            case = []
            for y in range(3):
                if way == 0:
                    if cases[x][y] == players:
                        count += 1
                        case.append([x, y])
                    elif cases[x][y] == player2:
                        count = -2
                        break
                elif way == 1:
                    if cases[y][x] == players:
                        count += 1
                        case.append([x, y])
                    elif cases[y][x] == player2:
                        count = -2
                        break
            if count == 2:
                print(way, ", ", x, ", ", case)
                return way, x, case

    for way in range(2):
        count = 0
        case = []
        for i in range(3):
            if way == 0:
                if cases[i][i] == players:
                    count += 1
                    case.append([i, i])
                elif cases[i][i] == player2:
                    count = -2
                    break
            elif way == 1:
                if cases[2 - i][i] == players:
                    count += 1
                    case.append([2 - i, i])
                elif cases[2 - i][i] == player2:
                    count = -2
                    break
        if count == 2:
            print(way + 2, ", ", case)
            return way + 2, case
    return False


def search_empty_cases():
    empty_cases = []
    for x in range(3):
        for y in range(3):
            if cases[x][y] == 0:
                empty_cases.append([x, y])
    return empty_cases


def ai_random_play():
    empty = search_empty_cases()
    # print("empty : " + str(empty))
    try:
        case = empty[random.randint(1, len(empty)-1)]
    except ValueError:
        case = empty[0]
    # print("cases : " + str(cases))

    print('random play in', case)
    draw_circle(case[0]+1, case[1]+1)
    cases[case[0]][case[1]] = 2


def ai_inteligent_play():
    # Attack
    lined_two_player_two = search_two_in_line(2)
    if lined_two_player_two is not False:
        if lined_two_player_two[0] == 0:  # attack in columns
            if lined_two_player_two[2][0][1] + lined_two_player_two[2][1][1] == 1:
                play(2, [lined_two_player_two[1], 2])
            elif lined_two_player_two[2][0][1] + lined_two_player_two[2][1][1] == 2:
                play(2, [lined_two_player_two[1], 1])
            elif lined_two_player_two[2][0][1] + lined_two_player_two[2][1][1] == 3:
                play(2, [lined_two_player_two[1], 0])
        elif lined_two_player_two[0] == 1:  # attack in lines
            if lined_two_player_two[2][0][1] + lined_two_player_two[2][1][1] == 1:
                play(2, [2, lined_two_player_two[1]])
            elif lined_two_player_two[2][0][1] + lined_two_player_two[2][1][1] == 2:
                play(2, [1, lined_two_player_two[1]])
            elif lined_two_player_two[2][0][1] + lined_two_player_two[2][1][1] == 3:
                play(2, [0, lined_two_player_two[1]])
        elif lined_two_player_two[0] == 2:  # attack in the first diagonal
            if lined_two_player_two[1][0][1] + lined_two_player_two[1][1][1] == 1:
                play(2, [2, 2])
            elif lined_two_player_two[1][0][1] + lined_two_player_two[1][1][1] == 2:
                play(2, [1, 1])
            elif lined_two_player_two[1][0][1] + lined_two_player_two[1][1][1] == 3:
                play(2, [0, 0])
        elif lined_two_player_two[0] == 3:  # attack in the second diagonal
            if lined_two_player_two[1][0][1] + lined_two_player_two[1][1][1] == 1:
                play(2, [0, 2])
            elif lined_two_player_two[1][0][1] + lined_two_player_two[1][1][1] == 2:
                play(2, [1, 1])
            elif lined_two_player_two[1][0][1] + lined_two_player_two[1][1][1] == 3:
                play(2, [0, 2])
    elif search_two_in_line(1) is not False and search_two_in_line(2) is False:
        # Defend
        lined_two_player_one = search_two_in_line(1)
        if lined_two_player_one is not False:
            if lined_two_player_one[0] == 0:  # defend in columns
                if lined_two_player_one[2][0][1] + lined_two_player_one[2][1][1] == 1:
                    play(2, [lined_two_player_one[1], 2])
                elif lined_two_player_one[2][0][1] + lined_two_player_one[2][1][1] == 2:
                    play(2, [lined_two_player_one[1], 1])
                elif lined_two_player_one[2][0][1] + lined_two_player_one[2][1][1] == 3:
                    play(2, [lined_two_player_one[1], 0])
            elif lined_two_player_one[0] == 1:  # defend in lines
                if lined_two_player_one[2][0][1] + lined_two_player_one[2][1][1] == 1:
                    play(2, [2, lined_two_player_one[1]])
                elif lined_two_player_one[2][0][1] + lined_two_player_one[2][1][1] == 2:
                    play(2, [1, lined_two_player_one[1]])
                elif lined_two_player_one[2][0][1] + lined_two_player_one[2][1][1] == 3:
                    play(2, [0, lined_two_player_one[1]])
            elif lined_two_player_one[0] == 2:  # defend in the first diagonal
                if lined_two_player_one[1][0][1] + lined_two_player_one[1][1][1] == 1:
                    play(2, [2, 2])
                elif lined_two_player_one[1][0][1] + lined_two_player_one[1][1][1] == 2:
                    play(2, [1, 1])
                elif lined_two_player_one[1][0][1] + lined_two_player_one[1][1][1] == 3:
                    play(2, [0, 0])
            elif lined_two_player_one[0] == 3:  # defend in the second diagonal
                if lined_two_player_one[1][0][1] + lined_two_player_one[1][1][1] == 1:
                    play(2, [0, 2])
                elif lined_two_player_one[1][0][1] + lined_two_player_one[1][1][1] == 2:
                    play(2, [1, 1])
                elif lined_two_player_one[1][0][1] + lined_two_player_one[1][1][1] == 3:
                    play(2, [0, 2])
    elif search_two_in_line(1) is False and search_two_in_line(2) is False:
        if cases == [[0, 0, 0], [0, 0, 0], [0, 0, 0]]:
            play(2, [0, 0])
        else:
            ai_random_play()



draw_back_lines()
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if not won:
            if event.type == pygame.MOUSEBUTTONUP:
                pos = list(pygame.mouse.get_pos())
                if cases[int(pos[0]/167)][int(pos[1]/167)] == 0:

                    if player == 1:
                        draw_cross(int(pos[0] / 167 + 1), int(pos[1] / 167 + 1))
                        cases[int(pos[0] / 167)][int(pos[1] / 167)] = 1
                        # print(cases)
                        player = 2
                        # ai_random_play()

    if verify_winn():
        won = True
        winner = verify_winn()[1]
        time.sleep(0.1)

    if not won:
        if player == 2:
            # ai_random_play()
            ai_inteligent_play()
            player = 1
    else:
        if finish_timer < 5:
            window_surface.fill(white)
            finish_timer += 1
            window_surface.fill(white)
            if verify_winn()[1] == 0:
                window_surface.blit(No_one_win_text_surface, (150, 200))
            elif verify_winn()[1] == 1:
                window_surface.blit(Cross_win_text_surface, (150, 200))
            elif verify_winn()[1] == 2:
                window_surface.blit(Circle_win_text_surface, (150, 200))
            text_surface = myfont_small.render('New game in : ' + str(5 - finish_timer) + ' seconds', False, black)

            window_surface.blit(text_surface, (80, 350))
            time.sleep(1)
            pygame.event.get()
        else:
            # noinspection PyUnboundLocalVariable
            if winner == 0:
                if player == 1:
                    player = 2
                else:
                    player = 1
            elif winner == 1:
                player = 2
            elif winner == 2:
                player = 1
            finish_timer = 0
            won = False
            cases = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
            window_surface.fill(white)
            draw_back_lines()
    clock.tick(FPS)
    pygame.display.flip()
