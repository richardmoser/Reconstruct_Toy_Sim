from random import randrange
from Antenna import Transmitter, Receiver
import DReco

import matplotlib
# matplotlib.use('TkAgg',force=True)
print("")
import matplotlib.pyplot as plt
import numpy as np
import math

#TODO: rewrite all functions to just use an RX array
#TODO: retool code to use delta_t instead of time from 0

# TX1 = Transmitter(0, 0, 10, '1')
TX2 = Transmitter(-70, 50, 10, '2')

RX1 = Receiver(0, 30, 10, '1')
RX2 = Receiver((15 * (math.sqrt(3))), -15, 10, '2')
RX3 = Receiver(-(15 * math.sqrt(3)), -15, 10, '3')

RXs = [RX1, RX2, RX3]

c =  c = 299792

if __name__ == '__main__':
    # start_time = randrange(0, 100)
    start_time = 0
    error1 = randrange(-100, 100) / 10000000
    error2 = randrange(-100, 100) / 10000000
    error3 = randrange(-100, 100) / 10000000
    print(f"Error values: {error1}, {error2}, {error3}")
    # error = 0

    # time from transmission to reception
    RX1.time_received = TX2.transmit(RX1, c) + start_time + error1
    RX2.time_received = TX2.transmit(RX2, c) + start_time + error2
    RX3.time_received = TX2.transmit(RX3, c) + start_time + error3

    # Begin Reconstruction code stuff
    print(f"RX1 receipt time: {RX1.time_received} seconds")
    print(f"RX2 receipt time: {RX2.time_received} seconds")
    print(f"RX3 receipt time: {RX3.time_received} seconds")

    fig = plt.figure(figsize=(8, 8))

    # ax = fig.add_subplot(111, projection='3d')
    ax = fig.add_subplot(111)
    # set axes to be 200m x 200m
    ax.set_xlim(-150, 150)
    ax.set_ylim(-150, 150)

    ax.text(.4, 1, "Event Geometry", transform=ax.transAxes)
    ax.scatter(TX2.x, TX2.y, c='r', marker='D')
    ax.scatter(RX1.x, RX1.y, c='b', marker='o')
    ax.scatter(RX2.x, RX2.y, c='g', marker='o')
    ax.scatter(RX3.x, RX3.y, c='r', marker='o')

    # draw the array circle
    x, y, z = DReco.circle_plotter_radius(30, 500, 0, 0, 0)
    ax.plot(x, y, c='b')

    # draw the event circles using the radius function
    x1, y1, z1 = DReco.circle_plotter_radius(c * RX1.time_received, 100, RX1.x, RX1.y, RX1.z)
    x2, y2, z2 = DReco.circle_plotter_radius(c * RX2.time_received, 100, RX2.x, RX2.y, RX2.z)
    x3, y3, z3 = DReco.circle_plotter_radius(c * RX3.time_received, 100, RX3.x, RX3.y, RX3.z)
    ax.plot(x1, y1, c='b')
    ax.plot(x2, y2, c='g')
    ax.plot(x3, y3, c='r')

    intersect = DReco.best_intersection(RX1, RX2, RX3, c, ax)
    ax.scatter(intersect[0][0], intersect[0][1], c='g', marker='X')
    ax.scatter(intersect[1][0], intersect[1][1], c='g', marker='X')
    ax.scatter(intersect[2][0], intersect[2][1], c='g', marker='X')

    ax.set_xlabel('x\n(meters)')
    ax.set_ylabel('y\n(meters)')
    # ax.set_zlabel('depth\n(meters)')

    # draw a line from the transmitter to the receivers
    # ax.plot([TX2.x, RX1.x], [TX2.y, RX1.y], [TX2.z, RX1.z], c='g')
    # ax.plot([TX2.x, RX2.x], [TX2.y, RX2.y], [TX2.z, RX2.z], c='g')
    # ax.plot([TX2.x, RX3.x], [TX2.y, RX3.y], [TX2.z, RX3.z], c='g')

    ax.text(RX1.x, RX1.y, f"{RX1.type}1")
    ax.text(RX2.x, RX2.y, f"{RX2.type}2")
    ax.text(RX3.x, RX3.y, f"{RX3.type}3")

    plt.show()
