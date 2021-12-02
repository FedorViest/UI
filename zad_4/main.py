import random
import math
import sys
import time
from copy import deepcopy

import matplotlib.pyplot as plt


"""
Funkcia na nacitanie bodov zo suboru do listu
"""


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


"""
Funkcia na vykreslenie bodov do grafu
"""


def plot_points(points, neighbour_count=0):
    x = []
    y = []
    colors = []
    for point in points:    # Priradenie x a y suradnic a farieb do jednotlivych poli
        x.append(point[0])
        y.append(point[1])
        colors.append(point[2])

    if len(points) <= 1000:
        plt.scatter(x, y, c=colors, s=50)
    else:
        plt.scatter(x, y, c=colors, s=2)
    if neighbour_count == 0:
        plt.title("Initial state")
    else:
        plt.title(f"Neighbour amount {neighbour_count}")
    plt.show()


"""
Funkcia na vygenerovanie nahodnych bodov a priradenie do pola, ktore funkcia vracia
"""


def generate_points(amount):
    generated = []
    color = ''
    percentage = int((amount/4) * 0.99)  # Vypocitanie kolko z kazdeho bodu je potrebne vygenerovat
    for i in range(percentage * 4):
        x, y = 0, 0
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
        generated.append([x, y, color])     # Priradenie suradnic a farby do pola
    other = amount - (percentage * 4)
    for i in range(other):      # Vygenerovanie zvysneho 1% bodov
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
        generated.append([x, y, color])     # Priradenie suradnic a farby do pola

    return generated


"""
Funkcia na klasifikaciu bodov podla suradnic, kazdemu novemu bodu priradi farbu podla KNN algoritmu
"""


def classify(all_pt, generated_pts, neighbour_count):
    counter = 0
    correct_classify = 0
    for generated_pt in generated_pts:      # Prechadzanie vygenerovanych bodov
        distances = []
        x = generated_pt[0]         # Ulozenie x suradnice do premennej
        y = generated_pt[1]         # Ulozenie y suradnice do premennej
        for point in all_pt:        # Prechadzanie uz urcenych bodov
            x1 = point[0]           # Ulozenie x suradnice do premennej
            y1 = point[1]           # Ulozenie y suradnice do premennej
            # Vypocitanie vzdialenosti generovaneho bodu od vsetkych urcenych bodov
            distance = math.dist((x, y), (x1, y1))
            distances.append([distance, point[2]])      # Priradenie vzdialenosti spolu s farbou do pola
        distances = sorted(distances, key=lambda dist: dist[0])     # Zoradenie vzdialenosti od najmensej po najvacsiu
        distances = distances[:neighbour_count]     # Vybratie prvych K prvkov y utriedeneho pola
        values = []
        red, green, blue, purple = 0, 0, 0, 0
        # Cyklus na poratanie jednotlivych farieb v poli so vzdialenostami
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

        # Zoradenie poctov farieb od najvacsej po najmensiu
        values = sorted(values, key=lambda count: count[0], reverse=True)

        # Ratanie uspesnosti klasifikatora
        if values[0][1] == generated_pt[2]:
            correct_classify += 1

        all_pt.append([x, y, values[0][1]])     # Priradenie bodu do pola vsetkych uz zaradenych bodov
        counter += 1
        sys.stdout.write(f"\rFinished {counter} points")
    return all_pt, correct_classify


"""
Funkcia na inicializaciu bodov a vykonanie testov
"""


def knn_start(amount_gen):
    initial_points = load_coords()
    plot_points(initial_points)
    generated = generate_points(amount_gen)
    neighbours = [1, 3, 7, 15]
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


point_amount = int(input("Points to generate: "))
knn_start(point_amount)
