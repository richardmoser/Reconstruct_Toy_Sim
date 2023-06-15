from random import randrange

from Antenna import Transmitter, Receiver

import matplotlib.pyplot as plt
import numpy as np
import math


# TX1 = Transmitter(0, 0, 10, '1')
TX2 = Transmitter(100, 100, 10, '2')

RX1 = Receiver(0, 30, 10, '1')
RX2 = Receiver((15 * (math.sqrt(3))), -15, 10, '2')
RX3 = Receiver(-(15 * math.sqrt(3)), -15, 10, '3')
# RX4 = Receiver(0, 0, '4')

c = 3e8


if __name__ == '__main__':

    # TX1.timetest(RX1, 3e8)

    # TX1toRX1 = TX2.transmit(RX2, c)
    # TX1toRX2 = TX1.transmit(RX2, c)
    # TX1toRX3 = TX1.transmit(RX3, c)

    TX2toRX1 = TX2.transmit(RX1, c)
    TX2toRX2 = TX2.transmit(RX2, c)
    TX2toRX3 = TX2.transmit(RX3, c)
    # TX2toRX4 = TX2.transmit(RX4, c)

    # Begin Reconstruction code stuff


    myVertexer = Vertexer(
        np.array([ [RX1.x, RX1.y,], [RX2.x, RX2.y], [RX3.x, RX3.y]]), c)

    times = np.array([TX2toRX1, TX2toRX2, TX2toRX3])

    print(f"TX2toRX1: {TX2toRX1}, TX2toRX2: {TX2toRX2}, TX2toRX3: {TX2toRX3}")
    solution = myVertexer.reconstruct(times)
    print(f"Solution: {solution}")

    fig = plt.figure(figsize=(12, 7))

    ax = fig.add_subplot(111, projection='3d')
    ax.text2D(.4, 1, "Event Geometry", transform=ax.transAxes)
    # ax.scatter(TX1.x, TX1.y, TX1.z, c='r', marker='o')
    ax.scatter(TX2.x, TX2.y, TX2.z, c='r', marker='o')
    ax.scatter(RX1.x, RX1.y, RX1.z, c='b', marker='o')
    ax.scatter(RX2.x, RX2.y, RX2.z, c='b', marker='o')
    ax.scatter(RX3.x, RX3.y, RX3.z, c='b', marker='o')
    # ax.scatter(RX4.x, RX4.y, RX4.z, c='b', marker='o')

    # Draw a circle in the XY plane at the specified depth using a wireframe
    radius = 30
    depth = -10
    resolution = 100
    theta = np.linspace(0, 2 * np.pi, resolution)
    x = radius * np.cos(theta)
    y = radius * np.sin(theta)
    z = np.full(resolution, depth)
    ax.plot(x, y, 10, c='g')
    ax.set_xlabel('meters')
    ax.set_ylabel('meters')
    ax.set_zlabel('depth meters')

    # draw a line from the transmitter to the receivers
    ax.plot([TX2.x, RX1.x], [TX2.y, RX1.y], [TX2.z, RX1.z], c='g')
    ax.plot([TX2.x, RX2.x], [TX2.y, RX2.y], [TX2.z, RX2.z], c='g')
    ax.plot([TX2.x, RX3.x], [TX2.y, RX3.y], [TX2.z, RX3.z], c='g')
    # ax.plot([TX2.x, RX4.x], [TX2.y, RX4.y], [TX2.z, RX4.z], c='g')
    # label the lines with the time it took to transmit
    # ax.text((TX2.x + RX1.x) / 2, (TX2.y + RX1.y) / 2, (TX2.z + RX1.z) / 2, f"{TX2.time_to_reach[1]} seconds")
    # ax.text((TX2.x + RX2.x) / 2, (TX2.y + RX2.y) / 2, (TX2.z + RX2.z) / 2, f"{TX2.time_to_reach[2]} seconds")
    # ax.text((TX2.x + RX3.x) / 2, (TX2.y + RX3.y) / 2, (TX2.z + RX3.z) / 2, f"{TX2.time_to_reach[3]} seconds")
    # ax.text((TX2.x + RX4.x) / 2, (TX2.y + RX4.y) / 2, (TX2.z + RX4.z) / 2, f"{TX2.time_to_reach[4]} seconds")

    ax.text(TX2.x, TX2.y, TX2.z, f"{TX2.type}1")
    ax.text(RX1.x, RX1.y, RX1.z, f"{RX1.type}1")
    ax.text(RX2.x, RX2.y, RX2.z, f"{RX2.type}2")
    ax.text(RX3.x, RX3.y, RX3.z, f"{RX3.type}3")
    # ax.text(RX4.x, RX4.y, RX4.z, f"{RX4.type}4")

    fig.canvas.manager.window.wm_geometry("+2600+0")

    plt.show()

    #plot the solution and receivers in a separate window
    fig2 = plt.figure(figsize=(12, 7))
    ax2 = fig2.add_subplot(111, projection='3d')
    ax2.scatter(TX2.x, TX2.y, TX2.z, c='r', marker='o')
    ax2.scatter(RX1.x, RX1.y, RX1.z, c='b', marker='o')
    ax2.scatter(RX2.x, RX2.y, RX2.z, c='b', marker='o')
    ax2.scatter(RX3.x, RX3.y, RX3.z, c='b', marker='o')
    ax2.scatter(solution[0], solution[1], 10, c='g', marker='x')

    ax2.text(TX2.x, TX2.y, TX2.z, f"{TX2.type}1")
    ax2.text(RX1.x, RX1.y, RX1.z, f"{RX1.type}1")
    ax2.text(RX2.x, RX2.y, RX2.z, f"{RX2.type}2")
    ax2.text(RX3.x, RX3.y, RX3.z, f"{RX3.type}3")
    # ax2.text(RX4.x, RX4.y, RX4.z, f"{RX4.type}4")
    # ax2.text(solution[0], solution[1], RX1.z, f"Solution")

    ax2.plot(x, y, 10, c='g')
    ax2.set_xlabel('meters')
    ax2.set_ylabel('meters')
    ax2.set_zlabel('depth meters')
    # fig2.canvas.manager.window.wm_geometry("+2600+0")
    plt.show()



    x_1 = randrange(10);
    y_1 = randrange(10);  # //z_1 = randrange(10)
    x_2 = randrange(10);
    y_2 = randrange(10);  # //z_2 = randrange(10)
    x_3 = randrange(10);
    y_3 = randrange(10);  # //z_3 = randrange(10)
    # x_4 = randrange(10); y_4 = randrange(10); //z_4 = randrange(10)

    # Pick source to be at random location
    x = randrange(1000);
    y = randrange(1000);  # //z = randrange(1000)

    # Set velocity
    c = 299792  # km/ns

    # Generate simulated source
    t_1 = math.sqrt((x - x_1) ** 2 + (y - y_1) ** 2) / c
    t_2 = math.sqrt((x - x_2) ** 2 + (y - y_2) ** 2) / c
    t_3 = math.sqrt((x - x_3) ** 2 + (y - y_3) ** 2) / c
    # t_4 = math.sqrt( (x - x_4)**2 + (y - y_4)**2 ) / c

    print('Actual:', x, y)
    myVertexer = Vertexer(np.array([[x_1, y_1], [x_2, y_2], [x_3, y_3]]), c)
    print(myVertexer.reconstruct(np.array([t_1, t_2, t_3])))