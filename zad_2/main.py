import random
import time


class Node:
    def __init__(self, matrix, depth):
        self.matrix = matrix
        self.depth = depth

    def move(self, start):
        x, y = find_char(start, "X")
        # moves = [[x - 1, y], [x, y + 1], [x, y - 1], [x + 1, y]]
        moves = [[x, y - 1], [x, y + 1], [x - 1, y], [x + 1, y]]
        moves_words = [["up"], ["down"], ["left"], ["right"]]
        nodes = []
        for move in moves:
            children = check_move(start, x, y, move[0], move[1])
            if children:
                nodes.append(children)
        return nodes


def check_move(data, x, y, x1, y1):
    if 0 <= x1 < len(data[0]) and 0 <= y1 < len(data):
        new_map = copy(data)
        help = data[y1][x1]
        new_map[y1][x1] = new_map[y][x]
        new_map[y][x] = help
        return new_map
    else:
        return None


def copy(data):
    copy = []
    for node in data:
        temp = []
        for char in node:
            temp.append(char)
        copy.append(temp)
    return copy


def find_char(map, character):
    for y in range(len(map)):
        for x in range(len(map[y])):
            if map[y][x] == character:
                return x, y


def heuristic_one(start, goal):
    number = 0
    for i in range(len(start)):
        for j in range(len(start[i])):
            if start[i][j] != goal[i][j]:
                number += 1
    return number


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


def get_distances(node, goal, heuristics):
    if heuristics == 1:
        return heuristic_one(node, goal)
    elif heuristics == 2:
        return heuristic_two(node, goal)
    elif heuristics == 3:
        return heuristic_one(node, goal) + heuristic_two(node, goal)

def solve(start, goal, heuristic):
    opened = []
    closed = []
    moves = 0
    init = Node(start, 0)
    opened.append(init)
    while True:
        current = opened[0]
        if get_distances(current.matrix, goal, heuristic) == 0 and get_distances(current.matrix, start, heuristic) != 0:
            closed.append(current)
            return closed, moves
        nodes = current.move(current.matrix)
        appended = 0
        for node in nodes:
            if closed:
                flag = 1
                for close in closed:
                    if get_distances(node, close.matrix, heuristic) == 0:
                        flag = 0
                        break
                if flag:
                    new = Node(node, current.depth + 1)
                    opened.append(new)
                    appended += 1
            else:
                new = Node(node, current.depth + 1)
                opened.append(new)
                appended += 1
        if appended == 0:
            max_range = len(nodes) - 1
            index = random.randrange(0, max_range)
            new = Node(nodes[index], current.depth + 1)
            opened.append(new)
        closed.append(current)
        opened = opened[1:]

        opened.sort(key=lambda x: get_distances(x.matrix, goal, heuristic))

        while opened[0].depth <= current.depth:
            opened = opened[1:]
            if not opened:
                break
        if not opened:
            print("\n\t\t\tEmpty opened list")
            return None, 0

        if moves > 1000:
            print("\n\t\t\tUnable to find solution with 1000 moves executed")
            return None, moves
        moves += 1


def print_result(closed, moves):
    for close in closed:
        for i in close.matrix:
            print(i)
        print()
    print("Made: " + str(moves) + " moves")


def get_inversions(start):
    inversions = 0
    for i in range(0, len(start)):
        for j in range(i + 1, len(start)):
            if start[j] != "X" and start[i] != "X" and start[i] > start[j]:
                inversions += 1

    return inversions


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


def convert_to_list(start):
    new = []
    for sublist in start:
        for char in sublist:
            new.append(char)
    return new


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
