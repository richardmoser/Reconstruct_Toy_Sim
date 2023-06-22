from random import randrange
from Antenna import Transmitter, Receiver
from KReco2D import Vertexer
import matplotlib.pyplot as plt
import numpy as np
import math


# TX1 = Transmitter(0, 0, 10, '1')
TX2 = Transmitter(100, 100, 10, '2')

RX1 = Receiver(0, 30, 10, '1')
RX2 = Receiver((15 * (math.sqrt(3))), -15, 10, '2')
RX3 = Receiver(-(15 * math.sqrt(3)), -15, 10, '3')

c = 299792


if __name__ == '__main__':
    # t_start = randrange(0, 200)  / 100
    t_start = 0

    TX2toRX1 = TX2.transmit(RX1, c) + t_start
    TX2toRX2 = TX2.transmit(RX2, c) + t_start
    TX2toRX3 = TX2.transmit(RX3, c) + t_start

    # Begin Reconstruction code stuff
    myVertexer = Vertexer(
        np.array([[RX1.x, RX1.y], [RX2.x, RX2.y], [RX3.x, RX3.y]]), c)

    times = np.array([TX2toRX1, TX2toRX2, TX2toRX3])

    print(f"TX2toRX1: {TX2toRX1}, TX2toRX2: {TX2toRX2}, TX2toRX3: {TX2toRX3}")
    solution = myVertexer.reconstruct(times)
    print(f"Solution: {solution}")
    print(f"manual code: {solution[0][0]}, {solution[0][1]}")

    fig = plt.figure(figsize=(12, 7))

    ax = fig.add_subplot(111, projection='3d')
    ax.text2D(.4, 1, "Event Geometry", transform=ax.transAxes)
    ax.scatter(TX2.x, TX2.y, TX2.z, c='r', marker='o')
    ax.scatter(RX1.x, RX1.y, RX1.z, c='b', marker='o')
    ax.scatter(RX2.x, RX2.y, RX2.z, c='b', marker='o')
    ax.scatter(RX3.x, RX3.y, RX3.z, c='b', marker='o')

    # Draw a circle in the XY plane at the specified depth using a wireframe
    radius = 30
    depth = -10
    resolution = 100
    theta = np.linspace(0, 2 * np.pi, resolution)
    x = radius * np.cos(theta)
    y = radius * np.sin(theta)
    z = np.full(resolution, depth)
    ax.plot(x, y, 10, c='g')
    ax.set_xlabel('x meters')
    ax.set_ylabel('y meters')
    ax.set_zlabel('depth meters')

    # draw a line from the transmitter to the receivers
    ax.plot([TX2.x, RX1.x], [TX2.y, RX1.y], [TX2.z, RX1.z], c='g')
    ax.plot([TX2.x, RX2.x], [TX2.y, RX2.y], [TX2.z, RX2.z], c='g')
    ax.plot([TX2.x, RX3.x], [TX2.y, RX3.y], [TX2.z, RX3.z], c='g')

    # fig.canvas.manager.window.wm_geometry("+2600+0")

    ax.scatter(solution[0][0], solution[0][1], 10, c='g', marker='x')

    ax.text(TX2.x, TX2.y, TX2.z, f"{TX2.type}1")
    ax.text(RX1.x, RX1.y, RX1.z, f"{RX1.type}1")
    ax.text(RX2.x, RX2.y, RX2.z, f"{RX2.type}2")
    ax.text(RX3.x, RX3.y, RX3.z, f"{RX3.type}3")
    ax.text(solution[0][0], solution[0][1], RX1.z, f"Solution")

    ax.plot(x, y, 10, c='g')
    ax.set_xlabel('meters')
    ax.set_ylabel('meters')
    ax.set_zlabel('depth meters')

    x_1 = randrange(10)
    y_1 = randrange(10)
    # //z_1 = randrange(10)
    x_2 = randrange(10)
    y_2 = randrange(10)
    # //z_2 = randrange(10)
    x_3 = randrange(10)
    y_3 = randrange(10)
    # //z_3 = randrange(10)

    # Pick source to be at random location
    x = randrange(1000)
    y = randrange(1000)  # //z = randrange(1000)

    # Generate simulated source
    t_1 = math.sqrt((x - x_1) ** 2 + (y - y_1) ** 2) / c
    t_2 = math.sqrt((x - x_2) ** 2 + (y - y_2) ** 2) / c
    t_3 = math.sqrt((x - x_3) ** 2 + (y - y_3) ** 2) / c

    print('Actual:', x, y)
    myVertexer = Vertexer(np.array([[x_1, y_1], [x_2, y_2], [x_3, y_3]]), c)
    print(myVertexer.reconstruct(np.array([t_1, t_2, t_3])))

    plt.show()
