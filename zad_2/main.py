

def move(start, goal):
    x, y = find_char(start, "X")
    moves = [[x - 1, y], [x, y + 1], [x, y - 1], [x + 1, y]]
    #moves = [[x, y - 1], [x, y + 1], [x - 1, y], [x + 1, y]]
    moves_words = [["up"], ["down"], ["left"], ["right"]]
    nodes = []
    for move in moves:
        temp = []
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


def manhattan_distance(x1, x2, y1, y2):
    return abs(x2 - x1) + abs((y2 - y1))


def get_distances(node, goal):
    distance = 0
    for n in node:
        for char in n:
            #if char != "X":
            x_start, y_start = find_char(node, char)
            x_goal, y_goal = find_char(goal, char)
            distance += manhattan_distance(x_start, x_goal, y_start, y_goal)
    return distance


def solve(start, goal):
    opened = []
    closed = []
    moves = []
    nodes = []
    temp = []
    opened.append(start)
    while True:
        current = opened[0]
        if get_distances(current, goal) == 0 and get_distances(current, start) != 0:
            closed.append(current)
            print("Solution found")
            break
        nodes = move(current, goal)
        for node in nodes:
            opened.append(node)
        closed.append(current)
        opened = opened[1:]

        opened = sorted(opened, key=lambda x: get_distances(x, goal))

    for close in closed:
        for i in close:
            print(i)
        print()





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
dimensions = [len(start_matrix[0]), len(start_matrix)]
print(start_matrix)
print(goal_matrix)
print(dimensions)
move(start_matrix, goal_matrix)
solve(start_matrix, goal_matrix)
