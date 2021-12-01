import random
import sys
import time
from copy import deepcopy
import matplotlib.pyplot as plt


def final_print(solution, path):
    print("\n\n")
    print_map(solution)
    number = 1
    print()
    for i in path:
        print("\tRoute number: " + str(number) + "\tRoute length: " + str(len(i)) + "\n\t\t==>\t" + str(i) + "\n\n")
        number += 1


def start(file_name, tabu_size, run, threshold):
    garden = create_map("subor" + str(file_name))
    rocks = print_map(garden)
    height = len(garden)
    width = len(garden[0])

    max_tiles = height * width

    print("\nDimensions:\t" + str(width) + "x" + str(height) + "\tRocks: " + str(rocks))

    solution, path, fitness, best_fitness, generations = tabu_search(garden, tabu_size, max_tiles, height, width, threshold)

    plt.plot(generations, fitness, label='Fitness', color='red')
    plt.legend()
    plt.plot(generations, best_fitness, label='Best fitness', color='black')
    plt.legend()
    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    plt.title("Max tabu list size: " + str(tabu_size) + " Run: " + str(run) +
              " Generations: " + str(generations[len(generations) - 1]) + " Threshold: " + str(threshold))
    plt.show()

    print()
    handle_print = str(input("Do you want to print final map and paths? [y/n] "))
    if handle_print == "y":
        final_print(solution, path)

    return generations[len(generations) - 1]


"""
Algoritmus na vykonanie tabu search
"""


def tabu_search(garden, tabu_size, tiles, height, width, threshold, gens=3000):
    best_garden = deepcopy(garden)
    border = init_borders(height, width)
    gen = 1
    random.shuffle(border)
    best_garden_fitness = tiles
    tabu_list, fitnesses = [], []
    path, best_path = [], []
    all_fitness, all_best_fitness, generations = [], [], []
    while True:
        if gen == gens:         # Podmienka na breaknutie cyklu v pripade, ze nastane predvoleny pocet generacii
            return best_garden, best_path, all_fitness, all_best_fitness, generations
        iterator = 0
        # Cyklus na generovanie susedov
        while True:
            if iterator == threshold:
                break
            neighbour = get_neighbour(deepcopy(border))
            garden_copied = deepcopy(garden)
            temp, temp_path = solve(garden_copied, neighbour, height, width)
            fitnesses.append([get_fitness(temp, tiles), neighbour, temp, temp_path])
            iterator += 1

        sorted_borders = sorted(fitnesses, key=lambda x: x[0])  # Zoradenie map podla fitness hodnoty od najmensej po najvacsiu
        fitnesses = []
        filled_map = []
        # Kontrola ci je tabu list plny
        if len(tabu_list) >= tabu_size:
            tabu_list.pop(0)
        # Kontrolovanie, ci sa mapa nachadza v tabu liste, ak nie, prida sa do tabu listu
        for curr in sorted_borders:
            if map_to_string(curr[1]) in tabu_list:
                continue
            border = curr[1]
            path = curr[3]
            tabu_list.append(map_to_string(curr[1]))
            filled_map = curr[2]
            break

        fitness = get_fitness(filled_map, tiles)

        all_fitness.append(fitness)
        all_best_fitness.append(best_garden_fitness)

        # Porovnanie, ci je novo vygenerovana zahrada lepsia ako doteraz najlepsia
        if fitness < best_garden_fitness:
            best_garden = deepcopy(filled_map)
            best_garden_fitness = fitness
            best_path = path
        # V pripade, ze su vsetky policka pohrabane, program sa skonci
        if best_garden_fitness == 0:
            generations.append(gen)
            return best_garden, best_path, all_fitness, all_best_fitness, generations

        sys.stdout.write("\r" + "Generation: " + str(gen) + " Fitness: " + str(best_garden_fitness) +
                         " Tabu length: " + str(len(tabu_list)))
        gen += 1
        generations.append(gen)


def map_to_string(garden):
    string = ""
    for i in garden:
        string = string + str(i)
    return string


"""
Funkcia na vygenerovanie 2 nahodnych indexov z pola a vymenenim pozicii tychto indexov
"""


def get_neighbour(border):
    pos1 = random.randrange(0, len(border))
    pos2 = random.randrange(0, len(border))
    while pos1 == pos2:
        pos2 = random.randrange(0, len(border))
    border[pos1], border[pos2] = border[pos2], border[pos1]
    return border


def get_fitness(garden, tiles):
    fitness = tiles
    for y in garden:
        for x in y:
            if x != "0":
                fitness -= 1
    return fitness


"""
Funkcia na vyriesenie zahrady zavolanim funkcie move()
"""


def solve(garden, border, height, width):
    incomplete = 0
    moves = 1
    garden_copied = deepcopy(garden)
    full = []
    for i in range(len(border)):
        start = border[i]

        if garden_copied[start[0]][start[1]] != "0":
            continue

        temp_map = deepcopy(garden_copied)
        temp_full = deepcopy(full)
        garden_copied, path, incomplete = move(garden_copied, start, height, width, moves)

        full.append(path)

        if incomplete:
            return temp_map, temp_full
        moves += 1

    return garden_copied, full


def init_borders(height, width):
    borders = []
    for y in range(height):
        for x in range(width):
            if y == 0 or y == height - 1:
                borders.append([y, x])
            else:
                if x == 0 or x == width - 1:
                    borders.append([y, x])
    return borders


def create_map(file_name):
    with open(file_name + ".txt", "r") as file:
        lines = file.readlines()
        start_matrix = []
        for line in lines:
            line = line.strip()
            row = line.split(' ')
            start_matrix.append(row)
    return start_matrix


def print_map(matrix):
    rocks = 0
    for i in matrix:
        for j in i:
            if j == "X":
                rocks += 1
            print(j, end='\t')
        print()

    return rocks


"""
Funkcie na kontrolovanie moznych pohybov do stran
"""


def check_down(garden, height, x, y):
    if y + 1 < height and garden[y + 1][x] == "0":
        return 1
    return 0


def check_up(garden, x, y):
    if y - 1 >= 0 and garden[y - 1][x] == "0":
        return 1
    return 0


def check_right(garden, width, x, y):
    if x + 1 < width and garden[y][x + 1] == "0":
        return 1
    return 0


def check_left(garden, x, y):
    if x - 1 >= 0 and garden[y][x - 1] == "0":
        return 1
    return 0


"""
Funkcia na zistenie moznych pohybov a vybranie jedneho nahodneho z nich
"""


def possible_moves(garden, start, height, width):
    directions = []
    x = start[1]
    y = start[0]
    if check_down(garden, height, x, y) and not (x == 0 or x == width - 1) or y == 0:
        directions.append(0)
    if check_up(garden, x, y) and not (x == 0 or x == width - 1) or y == height - 1:
        directions.append(2)
    if check_right(garden, width, x, y) and not (y == 0 or y == height - 1) or x == 0:
        directions.append(1)
    if check_left(garden, x, y) and not (y == 0 or y == height - 1) or x == width - 1:
        directions.append(3)

    direction = random.choice(directions)
    return direction


"""
Funkcia na kontrolu, ci som na hranici
"""


def check_border(x, y, height, width):
    if y == height - 1:
        return 1
    if y == 0:
        return 1
    if x == width - 1:
        return 1
    if x == 0:
        return 1
    return 0


"""
Funkcia na vykonanie pohybu
"""


def make_move(direction, x, y):
    if direction == 0:
        y += 1
    elif direction == 1:
        x += 1
    elif direction == 2:
        y -= 1
    else:
        x -= 1
    return y, x


"""
Funkcia na skontrolovanie, ci je pozicia mimo vyhradenej mapy
"""


def check_map_borders(x, y, height, width):
    if (x >= width or x < 0) or y >= height or y < 0:
        return 1
    return 0


"""
Funkcia na zmenenie pohybu v pripade, ze cesta nemoze pokracovat, kvoli bud kamenu alebo uz pohrabanemu policku
"""


def move_left_right(garden, direction, x, y, height, width):
    r_direction = (direction + 1) % 4
    l_direction = (direction - 1) % 4

    left = right = 1

    new_y, new_x = make_move(l_direction, x, y)
    if check_map_borders(new_x, new_y, height, width) or garden[new_y][new_x] != "0":
        left = 0

    new_y, new_x = make_move(r_direction, x, y)
    if check_map_borders(new_x, new_y, height, width) or garden[new_y][new_x] != "0":
        right = 0

    # Kontrola, ci je mozny pohyb dolava, doprava alebo aj aj. V pripade, ze su mozne oba pohyby, nahodne sa vyberie
    # pohyb
    # V pripade, ze sa nemoze pohnut nikam, vrati sa -1
    selections = []
    if left and right:
        selections.extend((r_direction, l_direction))
        return random.choice(selections)
    elif left and not right:
        return l_direction
    elif right and not left:
        return r_direction

    return -1


"""
Funkcia na vykonanie pohybov a potupne zaplnovanie zahrady pohybmi
"""


def move(garden, start, height, width, move_count):
    iterations = 0
    path = [start]
    x = path[0][1]
    y = path[0][0]
    direction = possible_moves(garden, start, height, width)    # Vygenerovanie moznych pohybov
    while 1:
        temp = []

        if check_map_borders(x, y, height, width):  # Kontrola, ci je pozicia na kraji
            if iterations > 2 and len(path) <= 1:   # Kontrola, aby musela byt dlzka pohybu aspon 2 dlha
                return None, None, 1
            path.pop(len(path) - 1)
            return garden, path, 0

        if garden[y][x] != "0":     # V pripade, ze v smere stoji prekazka
            path.pop(len(path) - 1)
            iterations -= 1
            x = path[iterations][1]
            y = path[iterations][0]
            direction = move_left_right(garden, direction, x, y, height, width)    # Vygenrovanie novych moznych pohybov
            if direction == -1:     # V tomto pripade, ziadny dalsi pohyb nebol mozny
                if len(path) <= 1:  # Kontrola ci je dlzka cesty aspon 2 dlha
                    return None, None, 1
                if not check_border(x, y, height, width):   # Kontrola, ci je koniec cesty na kraji mapy (mnich moze vyjst)
                    path.pop(len(path) - 1)
                    return None, None, 1
                return garden, path, 0

        garden[y][x] = move_count

        y, x = make_move(direction, x, y)

        temp.extend((y, x))
        path.append(temp)

        iterations += 1

        x = path[iterations][1]
        y = path[iterations][0]


file_name = int(input("Select file number: "))
tabu_size = int(input("Select tabu list size: "))
threshold = int(input("Select threshold (amount of generated neighbours): "))
# TESTOVANIE
"""sizes = [500, 50, 10]
thresholds = [5, 10, 20]
for threshold in thresholds:
    for tabu_size in sizes:
        avg_gen = 0
        t_start = time.time()
        for i in range(10):
            avg_gen += start(file_name, tabu_size, i + 1, threshold)
        t_end = time.time()
        avg_gen = avg_gen / 10
        print("\nTabu size: " + str(tabu_size) + "\nNeighbours: " + str(threshold) + "\nAverage generation: " + str(avg_gen))
        print("Average time took:" + str((t_end - t_start) / 10) + "\n\n")"""

start(file_name, tabu_size, 1, threshold)
