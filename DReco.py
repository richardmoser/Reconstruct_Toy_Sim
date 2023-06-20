import numpy as np
import matplotlib.pyplot as plt
import math

def circle_plotter_time(time, resolution, posit, c):
    radius = time * c
    theta = np.linspace(0, 2 * np.pi, resolution)
    x = radius * np.cos(theta) + posit.x
    y = radius * np.sin(theta) + posit.y
    z = posit.z
    print(f"radius: {radius}")
    return x, y, z


def circle_plotter_radius(radius, resolution, x, y, z):
    theta = np.linspace(0, 2 * np.pi, resolution)
    x = radius * np.cos(theta) + x
    y = radius * np.sin(theta) + y
    # z = z
    print(f"radius: {radius}")
    return x, y, z


def distance(x1, y1, x2, y2):
    # Calculate the Euclidean distance between two points
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def best_intersection(RX1, RX2, RX3, c):
    x1 = RX1.x
    y1 = RX1.y
    r1 = RX1.time_received * c

    x2 = RX2.x
    y2 = RX2.y
    r2 = RX2.time_received * c

    x3 = RX3.x
    y3 = RX3.y
    r3 = RX3.time_received * c

    # finds the intersection of the first two circles and splits them into two variables
    intersect_12a, intersect_12b = helper_intersections(x1, y1, r1, x2, y2, r2)
    # finds the intersection of the second two circles
    intersect_23a, intersect_23b = helper_intersections(x2, y2, r2, x3, y3, r3)
    # finds the intersection of the first and third circles
    intersect_13a, intersect_13b = helper_intersections(x1, y1, r1, x3, y3, r3)

    # # finds the intersection of the first two circles and puts them in one variable
    # intersect_12 = helper_intersections(x1, y1, r1, x2, y2, r2) #list of two points
    # intersect_23 = helper_intersections(x2, y2, r2, x3, y3, r3)
    # intersect_13 = helper_intersections(x1, y1, r1, x3, y3, r3)

    # array = [[x1, y1, r1], [x2, y2, r2], [x3, y3, r3]]
    intersects = [intersect_12a, intersect_12b, intersect_13a, intersect_13b, intersect_23a, intersect_23b]
    # intersects = [intersect_12, intersect_13, intersect_23]
    best_dist = 0
    best_12 = [0,0]
    best_13 = [0,0]
    best_23 = [0,0]
    # tempdist = intersect_distance(RX1, RX2, RX3, intersect_12a)


    aaa = averager(intersect_12a[0], intersect_12a[1], intersect_23a[0], intersect_23a[1], intersect_13a[0], intersect_13a[1])
    aab = averager(intersect_12a[0], intersect_12a[1], intersect_23a[0], intersect_23a[1], intersect_13b[0], intersect_13b[1])
    aba = averager(intersect_12a[0], intersect_12a[1], intersect_23b[0], intersect_23b[1], intersect_13a[0], intersect_13a[1])
    abb = averager(intersect_12a[0], intersect_12a[1], intersect_23b[0], intersect_23b[1], intersect_13b[0], intersect_13b[1])
    baa = averager(intersect_12b[0], intersect_12b[1], intersect_23a[0], intersect_23a[1], intersect_13a[0], intersect_13a[1])
    bab = averager(intersect_12b[0], intersect_12b[1], intersect_23a[0], intersect_23a[1], intersect_13b[0], intersect_13b[1])
    bba = averager(intersect_12b[0], intersect_12b[1], intersect_23b[0], intersect_23b[1], intersect_13a[0], intersect_13a[1])
    bbb = averager(intersect_12b[0], intersect_12b[1], intersect_23b[0], intersect_23b[1], intersect_13b[0], intersect_13b[1])

    aaa_dist = triangle_distance(intersect_12a, intersect_23a, intersect_13a, aaa)
    aab_dist = triangle_distance(intersect_12a, intersect_23a, intersect_13b, aab)
    aba_dist = triangle_distance(intersect_12a, intersect_23b, intersect_13a, aba)
    abb_dist = triangle_distance(intersect_12a, intersect_23b, intersect_13b, abb)
    baa_dist = triangle_distance(intersect_12b, intersect_23a, intersect_13a, baa)
    bab_dist = triangle_distance(intersect_12b, intersect_23a, intersect_13b, bab)
    bba_dist = triangle_distance(intersect_12b, intersect_23b, intersect_13a, bba)
    bbb_dist = triangle_distance(intersect_12b, intersect_23b, intersect_13b, bbb)

    best_intersect_dist = min(aaa_dist, aab_dist, aba_dist, abb_dist, baa_dist, bab_dist, bba_dist, bbb_dist)

    if best_intersect_dist == aaa_dist:
        best_intersect = [intersect_12a, intersect_23a, intersect_13a]
    elif best_intersect_dist == aab_dist:
        best_intersect = [intersect_12a, intersect_23a, intersect_13b]
    elif best_intersect_dist == aba_dist:
        best_intersect = [intersect_12a, intersect_23b, intersect_13a]
    elif best_intersect_dist == abb_dist:
        best_intersect = [intersect_12a, intersect_23b, intersect_13b]
    elif best_intersect_dist == baa_dist:
        best_intersect = [intersect_12b, intersect_23a, intersect_13a]
    elif best_intersect_dist == bab_dist:
        best_intersect = [intersect_12b, intersect_23a, intersect_13b]
    elif best_intersect_dist == bba_dist:
        best_intersect = [intersect_12b, intersect_23b, intersect_13a]
    elif best_intersect_dist == bbb_dist:
        best_intersect = [intersect_12b, intersect_23b, intersect_13b]

    # for i in range(len(intersects)):
    #     for j in range(len(intersects)):
    #         for k in range(len(intersects)):
    #             tempdist = intersect_distance(RX1, RX2, RX3, intersects[i])
    #             tempdist += intersect_distance(RX1, RX2, RX3, intersects[j])
    #             tempdist += intersect_distance(RX1, RX2, RX3, intersects[k])
    #             if tempdist > best_dist:
    #                 best_dist = tempdist
    #                 best_12 = intersects[i]
    #                 best_13 = intersects[j]
    #                 best_23 = intersects[k]
    #                 print(best_dist)
    #                 print(best_12)
    #                 print(best_13)
    #                 print(best_23)
    #                 print()


    return best_intersect


def triangle_distance(intersect1, intersect2, intersect3, point):
    # sums the distance from each point in the triangle to the point
    dist1 = distance(intersect1[0], intersect1[1], point[0], point[1])
    dist2 = distance(intersect2[0], intersect2[1], point[0], point[1])
    dist3 = distance(intersect3[0], intersect3[1], point[0], point[1])
    return dist1 ** 2 + dist2 ** 2 + dist3 ** 2

def averager(x1, y1, x2, y2, x3, y3):
    # finds the average of the three points
    x = (x1 + x2 + x3) / 3
    y = (y1 + y2 + y3) / 3
    return x, y


def helper_intersections(x1, y1, r1, x2, y2, r2):
    # Calculate the distance between the centers of the circles
    d = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    # Check if the circles are separate or one is contained within the other
    if d > r1 + r2 or d < abs(r1 - r2):
        # Circles do not intersect or one is contained within the other
        print(f"Circles centered at {x1, y1} and {x2, y2} do not intersect")
        return []

    # Calculate the intersection points
    a = (r1 ** 2 - r2 ** 2 + d ** 2) / (2 * d)
    h = math.sqrt(r1 ** 2 - a ** 2)

    # Calculate the intersection coordinates
    x3 = x1 + a * (x2 - x1) / d
    y3 = y1 + a * (y2 - y1) / d
    x4 = x3 + h * (y2 - y1) / d
    y4 = y3 - h * (x2 - x1) / d
    x5 = x3 - h * (y2 - y1) / d
    y5 = y3 + h * (x2 - x1) / d
    # Return the intersection points as tuples
    return [x4, y4], [x5, y5]