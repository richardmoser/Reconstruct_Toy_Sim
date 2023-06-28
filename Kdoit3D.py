import time
import KReco3D
from Antenna import Transmitter, Receiver
import matplotlib.pyplot as plt
import math
import os
from time import process_time_ns

debug_printout = False
draw_array = False
draw_histograms = False

# TODO: could probably implement something to handle complex numbers in
#  histograms at some point but it seems to work as is

RX1 = Receiver(0, 30, 10, '1')
RX2 = Receiver((15 * (math.sqrt(3))), -15, 10, '2')
RX3 = Receiver(-(15 * math.sqrt(3)), -15, 10, '3')
RX4 = Receiver(0, 0, 10, '4')
c = 299792

infile = "test"
# loops = 1000
loops = 100

# debug_printout = True  # prints additional information to the console for debugging
# draw_array = True  # draws the array of receivers and transmitters to the screen
# draw_histograms = True  # draws the histograms of the error values


if __name__ == '__main__':

    start_of_main = process_time_ns()

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
        if debug_printout:
            print(f"error_dist: {error_dist[i]}")
            print(f"Loop {i} complete")

    print(f"Done! {loops} loops complete")

    end_of_looping = process_time_ns()

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
    if debug_printout: print(f"Phi Error hist")
    axs[0, 0].hist(error_phi, bins=loops, histtype='stepfilled', rwidth=0.8)
    axs[0, 0].set_ylabel("Occurrences")
    axs[0, 0].set_xlabel("Error (degrees)")
    #set x axis to +/- 110% of the maximum value in the array
    # axs[0, 0].set_xlim(-1.1 * max(error_phi), 1.1 * max(error_phi))
    axs[0, 0].set_xlim(-2, 2)
    axs[0, 0].set_title("Phi Error")
    # axs[0, 0].set_xscale('symlog')

    if debug_printout: print(f"Theta Error hist")
    axs[1, 0].hist(error_theta, bins=loops, histtype='stepfilled', rwidth=0.8)
    axs[1, 0].set_ylabel("Occurrences")
    axs[1, 0].set_xlabel("Error (degrees)")
    #set x axis to +/- 110% of the maximum value in the array
    # axs[2, 0].set_xlim(-1.1 * max(error_theta), 1.1 * max(error_theta))
    axs[1, 0].set_xlim(-2, 2)
    axs[1, 0].set_title("Theta Error")

    if debug_printout: print(f"X Distance Error hist")
    # axs[2, 0] is the X distance error stored in the first index of each error_dist array
    axs[2, 0].hist([error_dist[i][0] for i in range(len(error_dist))], bins=loops, histtype='stepfilled', rwidth=0.8)
    axs[2, 0].set_ylabel("Occurrences")
    axs[2, 0].set_xlabel("Error (meters)")
    #set x axis to +/- 110% of the maximum value in the array
    axs[2, 0].set_xlim(-1.1 * max([error_dist[i][0] for i in range(len(error_dist))]), 1.1 * max([error_dist[i][0] for i in range(len(error_dist))]))
    axs[2, 0].set_title("X Distance Error in Meters")

    if debug_printout: print(f"Y Distance Error hist")
    # axs[4, 0] is the Y distance error stored in the second index of each error_dist array
    axs[3, 0].hist([error_dist[i][1] for i in range(len(error_dist))], bins=loops, histtype='stepfilled', rwidth=0.8)
    axs[3, 0].set_ylabel("Occurrences")
    axs[3, 0].set_xlabel("Error (meters)")
    #set x axis to +/- 110% of the maximum value in the array
    axs[3, 0].set_xlim(-1.1 * max([error_dist[i][1] for i in range(len(error_dist))]), 1.1 * max([error_dist[i][1] for i in range(len(error_dist))]))
    axs[3, 0].set_title("Y Distance Error in Meters")

    if debug_printout: print(f"Z Distance Error hist")
    axs[4, 0].hist([error_dist[i][2] for i in range(len(error_dist))], bins=loops, histtype='stepfilled', rwidth=0.8)
    axs[4, 0].set_ylabel("Occurrences")
    axs[4, 0].set_xlabel("Error (meters)")
    #set x axis to +/- 110% of the maximum value in the array
    # axs[5, 0].set_xlim(-1.1 * max([error_dist[i][2] for i in range(len(error_dist))]), 1.1 * max([error_dist[i][2] for i in range(len(error_dist))]))
    axs[4, 0].set_xlim(-50, 50)
    axs[4, 0].set_title("Z Distance Error in Meters")


    # axs[2, 1] is the histogram of the percentage error in the X direction
    # axs[2, 1] = ax3.twinx()
    if debug_printout: print(f"X Distance Error as a Percentage of Total Distance hist")
    axs[2, 1].hist([100 * error_dist[i][0] / TX[i].x for i in range(len(error_dist))], bins=loops,
                   histtype='stepfilled', rwidth=0.8, color='red')
    axs[2, 1].set_xlabel("Error (% of actual distance from origin)")
    axs[2, 1].set_ylabel("Occurrences")
    # axs[2, 1].set_ylim(0, 100)
    # axs[2, 1].set_xlim(-1.1 * max([error_dist[i][0] for i in range(len(error_dist))]),
    #                    1.1 * max([error_dist[i][0] for i in range(len(error_dist))]))
    axs[2, 1].set_xlim(-15, 15)
    axs[2, 1].set_title("X Distance Error as a Percentage of Total Distance")

    if debug_printout: print(f"Y Distance Error as a Percentage of Total Distance hist")
    # axs[3, 1] is the histogram of the percentage error in the Y direction
    # axs[3, 1] = ax4.twinx()
    axs[3, 1].hist([100 * error_dist[i][1] / TX[i].y for i in range(len(error_dist))], bins=loops,
                   histtype='stepfilled', rwidth=0.8, color='red')
    axs[3, 1].set_xlabel("Error (% of actual distance from origin)")
    axs[3, 1].set_ylabel("Occurrences")
    # axs[3, 1].set_ylim(0, 100)
    # axs[3, 1].set_xlim(-1.1 * max([error_dist[i][1] for i in range(len(error_dist))]),
    #                    1.1 * max([error_dist[i][1] for i in range(len(error_dist))]))
    axs[3, 1].set_xlim(-15, 15)
    axs[3, 1].set_title("Y Distance Error as a Percentage of Total Distance")

    if debug_printout: print(f"Z Distance Error as a Percentage of Total Distance hist")
    # axs[4, 1] is the histogram of the percentage error in the Z direction
    # axs[4, 1] = ax5.twinx()
    axs[4, 1].hist([100 * error_dist[i][2] / TX[i].z for i in range(len(error_dist))], bins=loops,
                   histtype='stepfilled', rwidth=0.8, color='red')
    axs[4, 1].set_xlabel("Error (% of actual distance from origin)")
    axs[4, 1].set_ylabel("Occurrences")
    # axs[4, 1].set_ylim(0, 100)
    # axs[4, 1].set_xlim(-1.1 * max([error_dist[i][2] for i in range(len(error_dist))]),
    #                    1.1 * max([error_dist[i][2] for i in range(len(error_dist))]))
    axs[4, 1].set_xlim(-15, 15)
    axs[4, 1].set_title("Z Distance Error as a Percentage of Total Distance")


    plt.tight_layout()
    if draw_histograms: plt.show()

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

    end_of_main = time.process_time_ns()
    print(f"Time taken: {end_of_main - start_of_main} nanoseconds")
    print(f"Time taken: {(end_of_main - start_of_main) / 1000000000} seconds")
