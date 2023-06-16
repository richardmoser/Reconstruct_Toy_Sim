import numpy as np
import matplotlib.pyplot as plt

def reconstruct(times):
    # Normalize times
    # times -= times.min()
    times -= min(times)

def circle_plotter(time, resolution, posit, c):
    radius = time * c
    theta = np.linspace(0, 2 * np.pi, resolution)
    x = radius * np.cos(theta) + posit.x
    y = radius * np.sin(theta) + posit.y
    z = posit.z
    print(f"radius: {radius}")
    return x, y, z

# def circle_intersection(center1, radius1, center2, radius2, center3, radius3):
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
    d1 = (distances[0]**2 - distances[1]**2 + dx1**2 + dy1**2 + dz1**2) / 2
    d2 = (distances[0]**2 - distances[2]**2 + dx2**2 + dy2**2 + dz2**2) / 2

    # Calculate coordinates of the intersection point(s)
    x = (d1 * dy2 - d2 * dy1) / delta
    y = (d2 * dx1 - d1 * dx2) / delta
    z = z1 + (d1 * dz2 - d2 * dz1) / delta

    return x, y, z

