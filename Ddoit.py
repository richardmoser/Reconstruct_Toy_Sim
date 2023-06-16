from random import randrange

from Antenna import Transmitter, Receiver
import DReco
import matplotlib.pyplot as plt
import numpy as np
import math

#TODO: rewrite this and the reconstruction code to use the new DReco.py
# based off of overlapping circles of radius c * t

# TX1 = Transmitter(0, 0, 10, '1')
TX2 = Transmitter(100, 100, 10, '2')

RX1 = Receiver(0, 30, 10, '1')
RX2 = Receiver((15 * (math.sqrt(3))), -15, 10, '2')
RX3 = Receiver(-(15 * math.sqrt(3)), -15, 10, '3')

RXs = [RX1, RX2, RX3]

c =  c = 299792


if __name__ == '__main__':

    # TX1.timetest(RX1, 3e8)

    # TX1toRX1 = TX2.transmit(RX2, c)
    # TX1toRX2 = TX1.transmit(RX2, c)
    # TX1toRX3 = TX1.transmit(RX3, c)

    start_time = randrange(0, 100)

    # RX1.time_received = TX2.transmit(RX1, c) + start_time
    # RX2.time_received = TX2.transmit(RX2, c) + start_time
    # RX3.time_received = TX2.transmit(RX3, c) + start_time
    RX1.time_received = TX2.transmit(RX1, c)
    RX2.time_received = TX2.transmit(RX2, c)
    RX3.time_received = TX2.transmit(RX3, c)

    # Begin Reconstruction code stuff


    array = np.array([ [RX1.x, RX1.y,], [RX2.x, RX2.y], [RX3.x, RX3.y]])

    times = np.array([RX1.time_received, RX2.time_received, RX3.time_received])

    print(f"RX1: {RX1.time_received}, RX2: {RX2.time_received}, RX3: {RX3.time_received}")


    fig = plt.figure(figsize=(12, 7))

    # ax = fig.add_subplot(111, projection='3d')
    ax = fig.add_subplot(111)
    ax.text(.4, 1, "Event Geometry", transform=ax.transAxes)
    # ax.scatter(TX1.x, TX1.y, TX1.z, c='r', marker='o')
    ax.scatter(TX2.x, TX2.y, c='r', marker='o')
    ax.scatter(RX1.x, RX1.y, c='b', marker='o')
    ax.scatter(RX2.x, RX2.y, c='b', marker='o')
    ax.scatter(RX3.x, RX3.y, c='b', marker='o')

    # calculate the intersection of the circles
    solution = [0, 0, 0]
    solution[0], solution[1], solution[2] = DReco.circle_intersection(RX1, RX2, RX3, c)
    print(solution)
    ax.scatter(solution[0], solution[1], solution[2], c='g', marker='o')


    # ax.plot(x, y, z, c='g')
    ax.set_xlabel('x\n(meters)')
    ax.set_ylabel('y\n(meters)')
    # ax.set_zlabel('depth\n(meters)')

    # draw a line from the transmitter to the receivers
    ax.plot([TX2.x, RX1.x], [TX2.y, RX1.y], [TX2.z, RX1.z], c='g')
    ax.plot([TX2.x, RX2.x], [TX2.y, RX2.y], [TX2.z, RX2.z], c='g')
    ax.plot([TX2.x, RX3.x], [TX2.y, RX3.y], [TX2.z, RX3.z], c='g')

    # draw a line from the reconstructed point to the receivers
    ax.plot([solution[0], RX1.x], [solution[1], RX1.y], [solution[2], RX1.z], c='r')
    ax.plot([solution[0], RX2.x], [solution[1], RX2.y], [solution[2], RX2.z], c='r')
    ax.plot([solution[0], RX3.x], [solution[1], RX3.y], [solution[2], RX3.z], c='r')

    # ax.text(TX2.x, TX2.y, TX2.z, f"{TX2.type}1")
    ax.text(RX1.x, RX1.y, f"{RX1.type}1")
    ax.text(RX2.x, RX2.y, f"{RX2.type}2")
    ax.text(RX3.x, RX3.y, f"{RX3.type}3")

    # label the reconstructed point and transission point
    ax.text(solution[0], solution[1], f"Reconstructed Point \n {solution[0]:.2f}, {solution[1]:.2f}, {solution[2]:.2f}")
    ax.text(TX2.x, TX2.y, f"True Point \n {TX2.x}, {TX2.y}, {TX2.z}")
    # fig.canvas.manager.window.wm_geometry("+2600+0")

    plt.show()
    ################################################################






    #plot the solution and receivers in a separate window
    # fig2 = plt.figure(figsize=(12, 7))
    # ax2 = fig2.add_subplot(111, projection='3d')
    # ax2.scatter(TX2.x, TX2.y, TX2.z, c='r', marker='o')
    # ax2.scatter(RX1.x, RX1.y, RX1.z, c='b', marker='o')
    # ax2.scatter(RX2.x, RX2.y, RX2.z, c='b', marker='o')
    # ax2.scatter(RX3.x, RX3.y, RX3.z, c='b', marker='o')
    #
    # ax2.text(TX2.x, TX2.y, TX2.z, f"{TX2.type}1")
    # ax2.text(RX1.x, RX1.y, RX1.z, f"{RX1.type}1")
    # ax2.text(RX2.x, RX2.y, RX2.z, f"{RX2.type}2")
    # ax2.text(RX3.x, RX3.y, RX3.z, f"{RX3.type}3")
    # # ax2.text(RX4.x, RX4.y, RX4.z, f"{RX4.type}4")
    # # ax2.text(solution[0], solution[1], RX1.z, f"Solution")
    #
    # # ax2.plot(x, y, 10, c='g')
    # ax2.set_xlabel('meters')
    # ax2.set_ylabel('meters')
    # ax2.set_zlabel('depth meters')
    # fig2.canvas.manager.window.wm_geometry("+2600+0")
    # plt.show()
