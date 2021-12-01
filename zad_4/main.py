import random
import math
import sys
import time
from copy import deepcopy

import matplotlib.pyplot as plt


def load_coords():
    all_pts = []
    with open("coords.txt", "r") as file:
        lines = file.read().splitlines()
        for line in lines:
            line = line.split(", ")
            x = int(line[1])
            y = int(line[2])
            if line[0] == "R":
                color = 'red'
            elif line[0] == "G":
                color = 'green'
            elif line[0] == "B":
                color = 'blue'
            elif line[0] == "P":
                color = 'purple'

            all_pts.append([x, y, color])

    return all_pts


def print_points(sur):
    for s in sur:
        print(s)


def plot_points(points, neighbour_count=0):
    x = []
    y = []
    colors = []
    for point in points:
        x.append(point[0])
        y.append(point[1])
        colors.append(point[2])

    plt.scatter(x, y, c=colors, s=2)
    if neighbour_count == 0:
        plt.title("Initial state")
    else:
        plt.title(f"Neighbour amount {neighbour_count}")
    plt.show()


def generate_points(amount):
    generated = []
    color = ''
    percentage = int((amount/4) * 0.99)
    for i in range(percentage * 4):
        if i % 4 == 0:
            x = random.randrange(-5000, 500)
            y = random.randrange(-5000, 500)
            color = 'red'
        elif i % 4 == 1:
            x = random.randrange(-501, 5001)
            y = random.randrange(-5000, 500)
            color = 'green'
        elif i % 4 == 2:
            x = random.randrange(-5000, 500)
            y = random.randrange(-501, 5001)
            color = 'blue'
        elif i % 4 == 3:
            x = random.randrange(-501, 5001)
            y = random.randrange(-501, 5001)
            color = 'purple'
        generated.append([x, y, color])
    other = amount - (percentage * 4)
    for i in range(other):
        x = random.randrange(-5000, 5001)
        y = random.randrange(-5000, 5001)
        if i % 4 == 0:
            color = 'red'
        elif i % 4 == 1:
            color = 'green'
        elif i % 4 == 2:
            color = 'blue'
        elif i % 4 == 3:
            color = 'purple'
        generated.append([x, y, color])

    return generated


def classify(all_pt, generated_pts, neighbour_count):
    counter = 0
    correct_classify = 0
    for generated_pt in generated_pts:
        distances = []
        x = generated_pt[0]
        y = generated_pt[1]
        for point in all_pt:
            x1 = point[0]
            y1 = point[1]
            distance = math.dist((x, y), (x1, y1))
            distances.append([distance, point[2]])
        distances = sorted(distances, key=lambda dist: dist[0])
        distances = distances[:neighbour_count]
        values = []
        red, green, blue, purple = 0, 0, 0, 0
        for distance in distances:
            if distance[1] == 'red':
                red += 1
            elif distance[1] == 'green':
                green += 1
            elif distance[1] == 'blue':
                blue += 1
            elif distance[1] == 'purple':
                purple += 1
        values.extend(([red, "red"], [green, "green"], [blue, "blue"], [purple, "purple"]))

        values = sorted(values, key=lambda count: count[0], reverse=True)

        if values[0][1] == generated_pt[2]:
            correct_classify += 1

        all_pt.append([x, y, values[0][1]])
        counter += 1
        sys.stdout.write(f"\rFinished {counter} points")
    return all_pt, correct_classify


initial_points = load_coords()
plot_points(initial_points)
amount_gen = 20000
generated = generate_points(amount_gen)
neighbours = [31]
for neighbour in neighbours:
    test_pts = deepcopy(initial_points)
    start = time.time()
    classified_pts, correct = classify(test_pts, generated, neighbour)
    plot_points(classified_pts, neighbour)
    end = time.time()
    percentage = (correct / amount_gen) * 100
    percentage = float("{:.2f}".format(percentage))
    print(f"\nClassification with {neighbour} neighbours"
          f"\nTook {int(end - start)} seconds"
          f"\nCorrectly classified points according to classifier: {percentage}%")
    print()
    print()
