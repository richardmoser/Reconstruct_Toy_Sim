from random import randrange

import KReco3D
from Antenna import Transmitter, Receiver
from KReco3D import Vertexer
import matplotlib.pyplot as plt
import numpy as np
import math
import os


# TX1 = Transmitter(0, 0, 10, '1')
TX2 = Transmitter(100, 100, 50, '2')

RX1 = Receiver(0, 30, 10, '1')
RX2 = Receiver((15 * (math.sqrt(3))), -15, 10, '2')
RX3 = Receiver(-(15 * math.sqrt(3)), -15, 10, '3')
RX4 = Receiver(0, 0, 10, '4')

c = 299792

if __name__ == '__main__':

    infile = "asdfasdf"
    loops = 30

    if not os.path.exists("data/"):
        os.makedirs("data/")

    bob = f"data/{infile}.txt"
    infile = KReco3D.file_name_increment(bob)

    TX = [0 for i in range(loops)]
    solution = [0 for i in range(loops)]
    error_dist = [0 for i in range(loops)]
    error_phi = [0 for i in range(loops)]
    error_theta = [0 for i in range(loops)]

    for i in range(loops):
        # KReco3D.send_it(RX1, RX2, RX3, RX4, c, infile, printout=False)
        TX[i], solution[i], error_dist[i], error_phi[i], error_theta[i] = KReco3D.send_it(RX1, RX2, RX3, RX4, c, infile)
        # return 1 is the event as a Transmitter object
        # return 2 is the reconstructed event location as a list of (x, y, z, t) coordinates
        # return 3 is the total distance of the error in the reconstructed event in meters
        # return 4 is the error in phi (azimuthal angle) in degrees
        # return 5 is the error in theta (polar angle) in degrees
        # print(f"Loop {i} complete")

    print(f"Done! {loops} loops complete")

    #make three plots on one figure. One for phi error, one for theta error, and one for the distance error
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True)
    fig.suptitle(f"Error values for {infile[:9]}")
    fig.set_size_inches(1920 / 96, 1080 / 96)

    ax1.hist(error_phi, bins=loops, histtype='stepfilled', rwidth=0.8)
    ax1.set_ylabel("Occurrences")
    ax1.set_xlabel("Error (degrees)")

    ax2.hist(error_theta, bins=loops, histtype='stepfilled', rwidth=0.8)
    ax2.set_ylabel("Occurrences")
    ax2.set_xlabel("Error (degrees)")

    ax3.hist(error_dist, bins=loops, histtype='stepfilled', rwidth=0.8)
    ax3.set_ylabel("Occurrences")
    ax3.set_xlabel("Event number")

    pwd = os.getcwd()
    print(f"infile: {infile}")
    print(f"Saving data to\t{pwd}/{infile}")


    plt.savefig(f"{infile[:-4]}.png")
    print(f"Plot saved to\t{pwd}/{infile[:-4]}.png")
    # plt.show()
