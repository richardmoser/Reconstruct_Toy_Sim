import numpy as np
import matplotlib.pyplot as plt
import math


def reconstruct(times):
    # Normalize times
    # times -= times.min()
    times -= min(times)

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
    z = z
    print(f"radius: {radius}")
    return x, y, z


def circle_intersection(RX1, RX2, RX3, c):
    # Calculate distances
    speeds_of_light = c  # Speed of light in meters per second
    distances = np.array([RX1.time_received, RX2.time_received, RX3.time_received]) * speeds_of_light

    # Extract antenna positions
    x1, y1, z1 = RX1.x, RX1.y, RX1.z
    x2, y2, z2 = RX2.x, RX2.y, RX2.z
    x3, y3, z3 = RX3.x, RX3.y, RX3.z

    # Calculate position differences
    dx1 = x2 - x1
    dy1 = y2 - y1
    dz1 = z2 - z1
    dx2 = x3 - x1
    dy2 = y3 - y1
    dz2 = z3 - z1

    # Calculate trilateration
    delta = dx2 * dy1 - dx1 * dy2
    d1 = (distances[0] ** 2 - distances[1] ** 2 + dx1 ** 2 + dy1 ** 2 + dz1 ** 2) / 2
    d2 = (distances[0] ** 2 - distances[2] ** 2 + dx2 ** 2 + dy2 ** 2 + dz2 ** 2) / 2

    # Calculate coordinates of the intersection point(s)
    x = (d1 * dy2 - d2 * dy1) / delta
    y = (d2 * dx1 - d1 * dx2) / delta
    z = z1 + (d1 * dz2 - d2 * dz1) / delta

    return x, y, z


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


def distance(x1, y1, x2, y2):
    # Calculate the Euclidean distance between two points
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def best_intersection(RX1, RX2, RX3, c, ax):
    x1 = RX1.x
    y1 = RX1.y
    r1 = RX1.time_received * c

    x2 = RX2.x
    y2 = RX2.y
    r2 = RX2.time_received * c

    x3 = RX3.x
    y3 = RX3.y
    r3 = RX3.time_received * c

    # finds the intersection of the first two circles
    intersect_12a, intersect_12b = helper_intersections(x1, y1, r1, x2, y2, r2)
    # finds the intersection of the second two circles
    intersect_23a, intersect_23b = helper_intersections(x2, y2, r2, x3, y3, r3)
    # finds the intersection of the first and third circles
    intersect_13a, intersect_13b = helper_intersections(x1, y1, r1, x3, y3, r3)

    array = [[x1, y1, r1], [x2, y2, r2], [x3, y3, r3]]
    intersects = [intersect_12a, intersect_12b, intersect_13a, intersect_13b, intersect_23a, intersect_23b]
    tempdist = intersect_distance(RX1, RX2, RX3, intersect_12a)


    intersect_12 = best_intersect_distance(RX1, RX2, RX3, intersect_12a, intersect_12b)
    intersect_23 = best_intersect_distance(RX1, RX2, RX3, intersect_23a, intersect_23b)
    intersect_13 = best_intersect_distance(RX1, RX2, RX3, intersect_13a, intersect_13b)

    return intersect_12, intersect_23, intersect_13


"""Do not use this function, it calculates the distance from the points to the RXs, not the middle of the intersection
# def best_intersect_distance(RX1, RX2, RX3, pointa, pointb):
#     if intersect_distance(RX1, RX2, RX3, pointa) > intersect_distance(RX1, RX2, RX3, pointb):
#         return pointb
#     else:
#         return pointa
# 
# def intersect_distance(RX1, RX2, RX3, intersection):
#     #returns the total distance between the xy pair and each RX position
#     x1 = RX1.x
#     y1 = RX1.y
# 
#     x2 = RX2.x
#     y2 = RX2.y
# 
#     x3 = RX3.x
#     y3 = RX3.y
# 
#     #dist 1 is the distance from x1,y1 to the x,y pair
#     dist1 = distance(x1, y1, intersection[0], intersection[1])
#     #dist 2 is the distance from x2,y2 to the x,y pair
#     dist2 = distance(x2, y2, intersection[0], intersection[1])
#     #dist 3 is the distance from x3,y3 to the x,y pair
#     dist3 = distance(x3, y3, intersection[0], intersection[1])
# 
#     total_distance = dist1 + dist2 + dist3
#     return total_distance


def function_intersection(RX1, RX2, RX3, c, ax):
    #TODO: make this work or delete. currently working on best_intersection() 6/20/23

    x1 = RX1.x
    y1 = RX1.y
    t1 = RX1.time_received * c

    x2 = RX2.x
    y2 = RX2.y
    t2 = RX2.time_received * c

    x3 = RX3.x
    y3 = RX3.y
    t3 = RX3.time_received * c

    #finds the intersection of the first two circles
    intersect_12 = helper_intersections(x1, y1, t1, x2, y2, t2)
    print(intersect_12)
    #finds the intersection of the second and third circles
    intersect_23 = helper_intersections(x2, y2, t2, x3, y3, t3)
    print(intersect_23)
    #finds the intersection of the first and third circles
    intersect_13 = helper_intersections(x1, y1, t1, x3, y3, t3)
    print(intersect_13)

    #TODO: fix the filter_intersection function because it is still selecting the 6/16/23
    # intersection behind the array.

    # TODO: remove unnecessary/unused/non functional functions above 6/16/23
    # (most of the helper functions are probably bad)

    #plots the lines of intersection
    # ax.plot(intersect_123)
    ax.scatter(intersect_12[0][0], intersect_12[0][1], c='grey', marker='x')
    ax.scatter(intersect_12[1][0], intersect_12[1][1], c='grey', marker='x' )
    ax.scatter(intersect_23[0][0], intersect_23[0][1], c='grey', marker='x')
    ax.scatter(intersect_23[1][0], intersect_23[1][1], c='grey', marker='x')
    ax.scatter(intersect_13[0][0], intersect_13[0][1], c='grey', marker='x')
    ax.scatter(intersect_13[1][0], intersect_13[1][1], c='grey', marker='x')

    #filter the intersection points
    intersetcionlist = [intersect_12[0], intersect_12[1], intersect_23[0], intersect_23[1], intersect_13[0], intersect_13[1]]


    #TODO: put the best intersection function here



    # print(f"Best intersections: {intersection}")
    # ax.scatter(intersection[0][0], intersection[0][1], c='black', marker='x')
    # ax.scatter(intersection[1][0], intersection[1][1], c='black', marker='x')
    # ax.scatter(intersection[2][0], intersection[2][1], c='black', marker='x')


    plt.show()
    #returns the intersection point
    return
"""


def circle_overlap(rx1, rx2, rx3, c):
    center1 = np.array([rx1.x, rx1.y, rx1.z])
    center2 = np.array([rx2.x, rx2.y, rx2.z])
    center3 = np.array([rx3.x, rx3.y, rx3.z])
    radius1 = rx1.time_received * c
    radius2 = rx2.time_received * c
    radius3 = rx3.time_received * c
    # Calculate the distances between the centers of the circles
    d12 = np.linalg.norm(center1 - center2)
    d13 = np.linalg.norm(center1 - center3)
    d23 = np.linalg.norm(center2 - center3)

    # Check if any circle is completely inside another circle
    if d12 + radius2 <= radius1 or d13 + radius3 <= radius1:
        return 0
    if d12 + radius1 <= radius2 or d23 + radius3 <= radius2:
        return 0
    if d13 + radius1 <= radius3 or d23 + radius2 <= radius3:
        return 0

    # Calculate the intersection area
    A1 = radius1**2 * np.arccos((d12**2 + radius1**2 - radius2**2) / (2 * d12 * radius1))
    A2 = radius2**2 * np.arccos((d12**2 + radius2**2 - radius1**2) / (2 * d12 * radius2))
    A3 = radius3**2 * np.arccos((d23**2 + radius3**2 - radius2**2) / (2 * d23 * radius3))
    A4 = radius2**2 * np.arccos((d23**2 + radius2**2 - radius3**2) / (2 * d23 * radius2))
    A5 = radius3**2 * np.arccos((d13**2 + radius3**2 - radius1**2) / (2 * d13 * radius3))
    A6 = radius1**2 * np.arccos((d13**2 + radius1**2 - radius3**2) / (2 * d13 * radius1))

    intersection_area = A1 + A2 + A3 + A4 + A5 + A6 - 0.5 * np.sqrt((-d12 + radius1 + radius2) * (d12 + radius1 - radius2) *
                                                                   (d12 - radius1 + radius2) * (d12 + radius1 + radius2) +
                                                                   (-d13 + radius1 + radius3) * (d13 + radius1 - radius3) *
                                                                   (d13 - radius1 + radius3) * (d13 + radius1 + radius3) +
                                                                   (-d23 + radius2 + radius3) * (d23 + radius2 - radius3) *
                                                                   (d23 - radius2 + radius3) * (d23 + radius2 + radius3))
    print(f"intersection area: {intersection_area}")
    return intersection_area

def plot_circles(rx1, rx2, rx3, c):
    center1 = np.array([rx1.x, rx1.y, rx1.z])
    center2 = np.array([rx2.x, rx2.y, rx2.z])
    center3 = np.array([rx3.x, rx3.y, rx3.z])
    radius1 = rx1.time_received * c
    radius2 = rx2.time_received * c
    radius3 = rx3.time_received * c

    fig, ax = plt.subplots()

    # Plot the circles
    circle1 = plt.Circle(center1, radius1, fill=False)
    circle2 = plt.Circle(center2, radius2, fill=False)
    circle3 = plt.Circle(center3, radius3, fill=False)
    ax.add_patch(circle1)
    ax.add_patch(circle2)
    ax.add_patch(circle3)

    # Set the aspect ratio to equal
    ax.set_aspect('equal', adjustable='box')

    # Set the limits based on the circles
    min_x = min(center1[0] - radius1, center2[0] - radius2, center3[0] - radius3)
    max_x = max(center1[0] + radius1, center2[0] + radius2, center3[0] + radius3)
    min_y = min(center1[1] - radius1, center2[1] - radius2, center3[1] - radius3)
    max_y = max(center1[1] + radius1, center2[1] + radius2, center3[1] + radius3)
    ax.set_xlim(min_x, max_x)
    ax.set_ylim(min_y, max_y)

    # Add gridlines
    ax.grid(True)

    # Show the plot
    plt.show()