import random
import time


class Node:
    def __init__(self, matrix, depth, direction):
        self.matrix = matrix
        self.depth = depth
        self.direction = direction


    """
    Funkcia na vygenerovanie pohybov postupne v poradi: hore, dole, vlavo, vpravo a v pripade, ze pohyb nie je mozny
    vrati None, inak ulozi stavy po pohyboch do pola
    """


    def move(self, start):
        x, y = find_char(start, "X")
        moves = [[x, y - 1], [x, y + 1], [x - 1, y], [x + 1, y]]
        move_word = ["up", "down", "left", "right"]
        nodes = []
        count = 0
        for move in moves:
            children = check_move(start, x, y, move[0], move[1])
            if children:
                new = Node(children, 0, move_word[count])
                nodes.append(new)
            count += 1
        return nodes


"""
Funkcia na kontrolu, ci je mozny pohyb, kontroluje, ci policko po pohybe nevyjde z matice
"""


def check_move(data, x, y, x1, y1):
    if 0 <= x1 < len(data[0]) and 0 <= y1 < len(data):
        new_map = copy(data)
        help = data[y1][x1]
        new_map[y1][x1] = new_map[y][x]
        new_map[y][x] = help
        return new_map
    else:
        return None



"""
Pomocna funckia na prekopirovanie stavu do noveho pola
"""


def copy(data):
    copy = []
    for node in data:
        temp = []
        for char in node:
            temp.append(char)
        copy.append(temp)
    return copy


"""
Funkcia ktora vrati x a y suradnicu pre lubovolny znak zo stavu matice
"""


def find_char(map, character):
    for y in range(len(map)):
        for x in range(len(map[y])):
            if map[y][x] == character:
                return x, y


"""
Heuristika 1, spocita pocet cisel, ktore su na zlej pozicii oproti cielovemu stavu
"""


def heuristic_one(start, goal):
    number = 0
    for i in range(len(start)):
        for j in range(len(start[i])):
            if start[i][j] != goal[i][j]:
                number += 1
    return number


"""
Funkcia na vytvorenie 2. heuristiky, kontroluje kolko pohybov potrebuje kazde cislo spravit, aby dosiahlo cielovy stav
"""


def heuristic_two(node, goal):
    distance = 0
    for n in node:
        for char in n:
            if char != "X":
                x_start, y_start = find_char(node, char)
                x_goal, y_goal = find_char(goal, char)
                distance += manhattan_distance(x_start, x_goal, y_start, y_goal)
    return distance


def manhattan_distance(x1, x2, y1, y2):
    return abs(x2 - x1) + abs((y2 - y1))


"""
Funckia na ziskanie ohoddnotenia podla heuristiky a vratenie tejto hodnoty
"""


def get_distances(node, goal, heuristics):
    if heuristics == 1:
        return heuristic_one(node, goal)
    elif heuristics == 2:
        return heuristic_two(node, goal)
    elif heuristics == 3:
        return heuristic_one(node, goal) + heuristic_two(node, goal)


"""
Hlavna funckia na riesenie stavov
"""


def solve(start, goal, heuristic):
    #Pomocne polia
    # V opened su stavy, ktore este nie su zapisane
    # V closed su stavy, ktore speju k spravnemu rieseniu
    opened = []
    closed = []
    moves = 0
    #Inicializacia prveho stavu a pridanie do opened listu
    init = Node(start, 0, "start")
    opened.append(init)
    while True:

        #Spracovanie prveho stavu z opened list, ktory je utriedeny podla heuristik od najmensej po najvacsiu

        current = opened[0]

        #Kontrola, ci nebol najdeny koncovy stav, v pripade, ze bol, funkcia vrati vsetky vykonane stavy a pocet vykonanych
        # pohybuv

        if get_distances(current.matrix, goal, heuristic) == 0 and get_distances(current.matrix, start, heuristic) != 0:
            closed.append(current)
            return closed, moves

        #Volanie funkcie na vygenerovanie pohybov a ulozenie do pola
        nodes = current.move(current.matrix)
        appended = 0
        for node in nodes:
            node.depth = current.depth + 1
            if closed:
                flag = 1
                # Kontrola, ci sa stav uz nenachadza v poli, kde su ulozene stavy spejuce k rieseniu
                for close in closed:
                    if get_distances(node.matrix, close.matrix, heuristic) == 0:
                        flag = 0
                        break
                #Ak sa taky stav este nenachadza, prida sa do opened listu
                if flag:
                    #new = Node(node, current.depth + 1)
                    opened.append(node)
                    appended += 1
            else:
                #new = Node(node, current.depth + 1)
                opened.append(node)
                appended += 1
        #V pripade, ze vsetky vygenerovane stavy sa uz nachadzaju v closed poli, vyberie sa jeden nahodny z pola, kde
        #kde su ulozene pohyby z current stavu
        if appended == 0:
            max_range = len(nodes) - 1
            index = random.randrange(0, max_range)
            #new = Node(nodes[index], current.depth + 1)
            opened.append(nodes[index])

        #Pridanie current stavu nakoniec closed pola
        closed.append(current)

        #Odstranenie prveho zaznamu z opened pola
        opened = opened[1:]

        #Zoradenie opened listu podla heuristik od najmensej
        opened.sort(key=lambda x: get_distances(x.matrix, goal, heuristic))

        #Kontrola, ci na prvom mieste v poli sa nenachadza stav, ktory sa vykonal skor ako current stav. Ak ano, tento stav
        # sa vymaze a cyklus pokracuje dovtedy, dokym stav v opened liste sa nenachadza hlbsie ako current stav
        while opened[0].depth <= current.depth:
            opened = opened[1:]

        #Osetrenie ci pocet vykonanych pohybov nie je vacsi ako 500
        if moves > 500:
            print("\n\t\t\tUnable to find solution with {} moves executed".format(moves))
            return None, moves
        moves += 1


"""
Funkcia na vypisanie vykonanych krokov
"""


def print_result(closed, moves):
    for close in closed:
        print(close.direction.upper() + "\n")
        for i in close.matrix:
            print(i)
        print()
    print("Made: " + str(moves) + " moves")


"""
Funkcia na zistenie poctu inverzii v pociatocnom stave. Pocet inverzii sa zvacsi v pripade, ze hocikde po lubovolnom znaku
z pola sa nachadza znak s mensou hodnotou
"""


def get_inversions(start):
    inversions = 0
    for i in range(0, len(start)):
        for j in range(i + 1, len(start)):
            if start[j] != "X" and start[i] != "X" and start[i] > start[j]:
                inversions += 1

    return inversions


"""
Kontrola, ci je stav riesitelny
"""


def check_solvable(start):
    new_list = convert_to_list(start)
    if len(new_list) % 2 == 1:
        if get_inversions(new_list) % 2 == 0:
            return 1
    else:
        x, y = find_char(start, "X")
        pos_blank = len(start) - y
        if pos_blank % 2 == 1 and get_inversions(new_list) % 2 == 0 or pos_blank % 2 == 0 and get_inversions(new_list) % 2 == 1:
            return 1
    return 0


"""
Pomocna funkcia na prekonvertovanie list of list na obycajny list
"""


def convert_to_list(start):
    new = []
    for sublist in start:
        for char in sublist:
            new.append(char)
    return new



"""
Funkcia na nacitanie pociatocneho a koncoveho stavu zo suborov do pola
"""


def load_from_file():
    with open("start.txt", "r") as file:
        lines = file.readlines()
        start_matrix = []
        for line in lines:
            line = line.strip()
            row = line.split(' ')
            start_matrix.append(row)
    with open("goal.txt", "r") as file:
        lines = file.readlines()
        goal_matrix = []
        for line in lines:
            line = line.strip()
            row = line.split(' ')
            goal_matrix.append(row)
    return start_matrix, goal_matrix


start_matrix, goal_matrix = load_from_file()

if check_solvable(start_matrix):

    start = time.time()
    print("\t\t\t\tHeuristic number one:\n\t\tHeuristic function = Number of misplaced tiles")
    closed, moves = solve(start_matrix, goal_matrix, 1)
    end = time.time()
    if closed:
        print("\n\t\t\tSolution found in " + str(end-start) + " seconds\n")
        print_result(closed, moves)

    start = time.time()
    print("\n\n\n\t\t\t\tHeuristic number two:\n\t\tHeuristic function = Manhattan distance")
    closed, moves = solve(start_matrix, goal_matrix, 2)
    end = time.time()
    if closed:
        print("\n\t\t\tSolution found in " + str(end - start) + " seconds\n")
        print_result(closed, moves)

    start = time.time()
    print("\n\n\n\t\t\t\tHeuristic number three:\n\t\tHeuristic function = Combination of heuristics 1 and 2")
    closed, moves = solve(start_matrix, goal_matrix, 3)
    end = time.time()
    if closed:
        print("\n\t\t\tSolution found in " + str(end - start) + " seconds\n")
        print_result(closed, moves)

else:
    print("This puzzle is unsolvable")
