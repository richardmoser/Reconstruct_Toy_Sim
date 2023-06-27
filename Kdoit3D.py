from random import randrange

import KReco3D
from Antenna import Transmitter, Receiver
from KReco3D import Vertexer
import matplotlib.pyplot as plt
import numpy as np
import math
import os

#TODO: set percentage plot y axes to be set relative to the max value in the arrays (so they are all the same)

# TX1 = Transmitter(0, 0, 10, '1')
# TX2 = Transmitter(100, 100, 50, '2')

RX1 = Receiver(0, 30, 10, '1')
RX2 = Receiver((15 * (math.sqrt(3))), -15, 10, '2')
RX3 = Receiver(-(15 * math.sqrt(3)), -15, 10, '3')
RX4 = Receiver(0, 0, 10, '4')
c = 299792

infile = "test"
# loops = 1000
loops = 10
# debug_printout = True
debug_printout = False
draw_array = False

if __name__ == '__main__':


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
        TX[i], solution[i], error_dist[i], error_phi[i], error_theta[i] = KReco3D.send_it(RX1, RX2, RX3, RX4, c, infile, debug_printout)
        # return 1 is the event as a Transmitter object
        # return 2 is the reconstructed event location as a list of (x, y, z, t) coordinates
        # return 3 is the total distance of the error in the reconstructed event in meters
        # return 4 is the error in phi (azimuthal angle) in degrees
        # return 5 is the error in theta (polar angle) in degrees
        print(f"error_dist: {error_dist[i]}")
        print(f"Loop {i} complete")

    print(f"Done! {loops} loops complete")


    print(f"Min, Max error Phi: {min(error_phi)}, {max(error_phi)}")
    print(f"Min, Max error Theta: {min(error_theta)}, {max(error_theta)}")
    print(f"Min, Max error Dist X: {min([error_dist[i][0] for i in range(len(error_dist))])}, {max([error_dist[i][0] for i in range(len(error_dist))])}")
    print(f"Min, Max error Dist Y: {min([error_dist[i][1] for i in range(len(error_dist))])}, {max([error_dist[i][1] for i in range(len(error_dist))])}")
    print(f"Min, Max error Dist Z: {min([error_dist[i][2] for i in range(len(error_dist))])}, {max([error_dist[i][2] for i in range(len(error_dist))])}")

    # fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(5, 1, sharex=False)
    fig, axs = plt.subplots(5, 2, sharex=False, gridspec_kw={'width_ratios': [2, 1]})

    fig.suptitle(f"Error values for {infile}")
    fig.set_size_inches(1920 / 96, 1300 / 96)

    # Remove the unused subplots
    axs[0, 1].remove()
    axs[1, 1].remove()

    # Plotting and customization for ax1, ax2, ax3, ax4, ax5

    axs[0, 0].hist(error_phi, bins=loops, histtype='stepfilled', rwidth=0.8)
    axs[0, 0].set_ylabel("Occurrences")
    axs[0, 0].set_xlabel("Error (degrees)")
    #set x axis to +/- 110% of the maximum value in the array
    # axs[0, 0].set_xlim(-1.1 * max(error_phi), 1.1 * max(error_phi))
    axs[0, 0].set_xlim(-.5, .5)
    axs[0, 0].set_title("Phi Error")
    # axs[0, 0].set_xscale('symlog')

    axs[1, 0].hist(error_theta, bins=loops, histtype='stepfilled', rwidth=0.8)
    axs[1, 0].set_ylabel("Occurrences")
    axs[1, 0].set_xlabel("Error (degrees)")
    #set x axis to +/- 110% of the maximum value in the array
    # axs[2, 0].set_xlim(-1.1 * max(error_theta), 1.1 * max(error_theta))
    axs[1, 0].set_xlim(-1, 1)
    axs[1, 0].set_title("Theta Error")

    # axs[2, 0] is the X distance error stored in the first index of each error_dist array
    axs[2, 0].hist([error_dist[i][0] for i in range(len(error_dist))], bins=loops, histtype='stepfilled', rwidth=0.8)
    axs[2, 0].set_ylabel("Occurrences")
    axs[2, 0].set_xlabel("Error (meters)")
    #set x axis to +/- 110% of the maximum value in the array
    axs[2, 0].set_xlim(-1.1 * max([error_dist[i][0] for i in range(len(error_dist))]), 1.1 * max([error_dist[i][0] for i in range(len(error_dist))]))
    axs[2, 0].set_title("X Distance Error")

    # axs[4, 0] is the Y distance error stored in the second index of each error_dist array
    axs[3, 0].hist([error_dist[i][1] for i in range(len(error_dist))], bins=loops, histtype='stepfilled', rwidth=0.8)
    axs[3, 0].set_ylabel("Occurrences")
    axs[3, 0].set_xlabel("Error (meters)")
    #set x axis to +/- 110% of the maximum value in the array
    axs[3, 0].set_xlim(-1.1 * max([error_dist[i][1] for i in range(len(error_dist))]), 1.1 * max([error_dist[i][1] for i in range(len(error_dist))]))
    axs[3, 0].set_title("Y Distance Error")

    axs[4, 0].hist([error_dist[i][2] for i in range(len(error_dist))], bins=loops, histtype='stepfilled', rwidth=0.8)
    axs[4, 0].set_ylabel("Occurrences")
    axs[4, 0].set_xlabel("Error (meters)")
    #set x axis to +/- 110% of the maximum value in the array
    # axs[5, 0].set_xlim(-1.1 * max([error_dist[i][2] for i in range(len(error_dist))]), 1.1 * max([error_dist[i][2] for i in range(len(error_dist))]))
    axs[4, 0].set_xlim(-50, 50)
    axs[4, 0].set_title("Z Distance Error")

    # axs[2, 1] is the histogram of the percentage error in the X direction
    # axs[2, 1] = ax3.twinx()
    axs[2, 1].hist([100 * error_dist[i][0] / TX[i].x for i in range(len(error_dist))], bins=loops,
                   histtype='stepfilled', rwidth=0.8, color='red')
    axs[2, 1].set_ylabel("Percentage Error")
    # axs[2, 1].set_ylim(0, 100)
    axs[2, 1].set_xlim(-1.1 * max([error_dist[i][0] for i in range(len(error_dist))]),
                       1.1 * max([error_dist[i][0] for i in range(len(error_dist))]))
    axs[2, 1].set_title("X Distance Error")

    # axs[3, 1] is the histogram of the percentage error in the Y direction
    # axs[3, 1] = ax4.twinx()
    axs[3, 1].hist([100 * error_dist[i][1] / TX[i].y for i in range(len(error_dist))], bins=loops,
                   histtype='stepfilled', rwidth=0.8, color='red')
    axs[3, 1].set_ylabel("Percentage Error")
    # axs[3, 1].set_ylim(0, 100)
    axs[3, 1].set_xlim(-1.1 * max([error_dist[i][1] for i in range(len(error_dist))]),
                       1.1 * max([error_dist[i][1] for i in range(len(error_dist))]))
    axs[3, 1].set_title("Y Distance Error")

    # axs[4, 1] is the histogram of the percentage error in the Z direction
    # axs[4, 1] = ax5.twinx()
    axs[4, 1].hist([100 * error_dist[i][2] / TX[i].z for i in range(len(error_dist))], bins=loops,
                   histtype='stepfilled', rwidth=0.8, color='red')
    axs[4, 1].set_ylabel("Percentage Error")
    # axs[4, 1].set_ylim(0, 100)
    axs[4, 1].set_xlim(-1.1 * max([error_dist[i][2] for i in range(len(error_dist))]),
                       1.1 * max([error_dist[i][2] for i in range(len(error_dist))]))
    axs[4, 1].set_title("Z Distance Error")


    plt.tight_layout()
    plt.show()


    pwd = os.getcwd()
    print(f"infile: {infile}")
    print(f"Saving data to\t{pwd}/{infile}")


    plt.savefig(f"{infile[:-4]}.png")
    print(f"Plot saved to\t{pwd}/{infile[:-4]}.png")
    # plt.show()


    if draw_array:
        # plotting the array
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')


        # sets maximum axis value to 1.1 times the maximum value of the array
        # max_axis = 1.1 * max([max([TX[i].x, TX[i].y, TX[i].z]) for i in range(len(TX))]) # for largest in whole array
        max_axis = 1.1 * int(max([TX[0].x, TX[0].y, TX[0].z]))
        ax.set_xlim3d(-max_axis, max_axis)
        ax.set_ylim3d(-max_axis, max_axis)
        ax.set_zlim3d(-max_axis, max_axis)

        #set the plot window to 8x8
        fig.set_size_inches(12,12)

        # plot the transmitters and receivers
        ax.scatter(TX[0].x, TX[0].y, TX[0].z, c='r', marker='o')
        ax.scatter(RX1.x, RX1.y, RX1.z, c='b', marker='o')
        ax.scatter(RX2.x, RX2.y, RX2.z, c='b', marker='o')
        ax.scatter(RX3.x, RX3.y, RX3.z, c='b', marker='o')

        # plot the reconstructed event
        ax.scatter(solution[0][0], solution[0][1], solution[0][2], c='g', marker='o')

        # plot the array circle 30m from 0,0,0
        x, y, z = KReco3D.circle_plotter_radius(30, 500, 0, 0, 0)
        ax.plot(x, y, z, c='k')


