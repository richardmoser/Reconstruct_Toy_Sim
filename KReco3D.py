"""
Author: Keith Madison
Modifications: Richard Moser
Purpose: learn something, reconstruct transmitter location from time differences
"""
from Antenna import Transmitter
from dataclasses import dataclass
from random import randrange
import os
from re import compile, findall, Pattern
from typing import List
from os.path import exists, join, dirname, basename
import numpy as np


"""Pre - fix code below, requires 4 transmitters in 3d space"""

M = np.diag([1, 1, 1, -1])

def seconds_to_nanoseconds(seconds):
    return seconds * 1e9


def points_to_phi_theta(point):
    # calculates phi and theta from points relative to the origin
    #Make sure that the array center is (0,0,0)!
    phi = np.arctan2(point[1], point[0])
    theta = np.arctan2(point[2], np.sqrt(point[0]**2 + point[1]**2))
    return phi, theta



def send_it(RX1, RX2, RX3, RX4, c, infile, printout=False):
    #generate a random transmitter location for TX2
    TX = Transmitter(randrange(-1000, 1000), randrange(-1000, 1000), randrange(-1000, 1000), 1)
    # TX = Transmitter(100, 100, 50, '2')

    t_start = randrange(0, 1000) / 1000000000  # t_start is between 0 and 1000 nanoseconds

    # set errors 1-4 to a gaussian distribution with mean 0 and std dev 1 and multiply them by 10^-9
    # scale = 1e-9 # +/- 1 nanosecond
    scale = 1e-8 # +/- 10 nanoseconds
    error1 = np.random.normal(0, 1) * scale
    error2 = np.random.normal(0, 1) * scale
    error3 = np.random.normal(0, 1) * scale
    error4 = np.random.normal(0, 1) * scale

    t_start_sec = seconds_to_nanoseconds(t_start)
    error1_sec = seconds_to_nanoseconds(error1)
    error2_sec = seconds_to_nanoseconds(error2)
    error3_sec = seconds_to_nanoseconds(error3)
    error4_sec = seconds_to_nanoseconds(error4)

    TX2toRX1_actual = TX.transmit3D(RX1, c) + t_start
    TX2toRX2_actual = TX.transmit3D(RX2, c) + t_start
    TX2toRX3_actual = TX.transmit3D(RX3, c) + t_start
    TX2toRX4_actual = TX.transmit3D(RX4, c) + t_start

    TX2toRX1_actual_sec = seconds_to_nanoseconds(TX2toRX1_actual)
    TX2toRX2_actual_sec = seconds_to_nanoseconds(TX2toRX2_actual)
    TX2toRX3_actual_sec = seconds_to_nanoseconds(TX2toRX3_actual)
    TX2toRX4_actual_sec = seconds_to_nanoseconds(TX2toRX4_actual)

    TX2toRX1 = TX2toRX1_actual + error1
    TX2toRX2 = TX2toRX2_actual + error2
    TX2toRX3 = TX2toRX3_actual + error3
    TX2toRX4 = TX2toRX4_actual + error4

    myVertexer = Vertexer(
        np.array([[RX1.x, RX1.y, RX1.z], [RX2.x, RX2.y, RX2.z], [RX3.x, RX3.y, RX3.z], [RX4.x, RX4.y, RX4.z]]), c)

    times = np.array([TX2toRX1, TX2toRX2, TX2toRX3, TX2toRX4])

    solution, alt_solution = myVertexer.reconstruct(times)
    if printout: print(f"Solution:\t({solution[0]:10.3f}, {solution[1]:10.3f}, {solution[2]:10.3f}   )")

    solution_error = np.array([solution[0] - float(TX.x), solution[1] - float(TX.y), solution[2] - float(TX.z)])
    alt_solution_error = np.array([alt_solution[0] - float(TX.x), alt_solution[1] - float(TX.y), alt_solution[2] - float(TX.z)])

    if np.linalg.norm(solution_error) > 10:
        if printout: print(f"\t\tError distance: {np.linalg.norm(solution_error)} meters") # distance between actual and reconstructed point in meters
        if printout: print(f"\t\tError distance for alternate solution: {np.linalg.norm(alt_solution - np.array([float(TX.x), float(TX.y), float(TX.z)]))} meters")
        if np.linalg.norm(alt_solution_error) < np.linalg.norm(solution_error):
            solution = alt_solution
            solution_error = alt_solution_error
            if printout: print("\t\tUsing alternate solution")

    sol_phi, sol_theta = points_to_phi_theta(solution)  # returns phi and theta in radians
    #this is relative to the origin! Make sure that the array center is (0,0,0)
    sol_phi_deg = np.degrees(sol_phi)  # convert to degrees. This is the azimuthal angle
    sol_theta_deg = np.degrees(sol_theta)  # convert to degrees. This is the polar angle

    act_phi, act_theta = points_to_phi_theta(np.array([float(TX.x), float(TX.y), float(TX.z)]))  # returns phi and theta in radians
    act_phi_deg = np.degrees(act_phi)  # convert to degrees
    act_theta_deg = np.degrees(act_theta)  # convert to degrees

    err_phi, err_theta = np.absolute(sol_phi - act_phi), np.absolute(sol_theta - act_theta)  # returns phi and theta error in radians
    err_phi_deg, err_theta_deg = np.degrees(err_phi), np.degrees(err_theta)  # convert to degrees

    #if the file exists, then append the data to the file, if not, create it and write the data
    if os.path.isfile(infile):
        with open(infile, 'a') as f:
            f.write(
                f"t_start: {t_start_sec}ns\nerror1: {error1_sec}ns\nerror2: "
                f"{error2_sec}ns\nerror3: {error3_sec}ns\nerror4: {error4_sec}ns\n"
                f"TX2toRX1_actual: {TX2toRX1_actual_sec - t_start_sec}ns\n"
                f"TX2toRX2_actual: {TX2toRX2_actual_sec - t_start_sec}ns\n"
                f"TX2toRX3_actual: {TX2toRX3_actual_sec - t_start_sec}ns\n"
                f"TX2toRX4_actual: {TX2toRX4_actual_sec - t_start_sec}ns\n"
                f"Solution:\t({solution[0]:10.3f}, {solution[1]:10.3f}, {solution[2]:10.3f}    )\n"
                f"Actual:\t\t({float(TX.x):10.3f}, {float(TX.y):10.3f}, {float(TX.z):10.3f}    )\n"
                f"Error:\t\t({solution_error[0]:10.3f}, {solution_error[1]:10.3f}, {solution_error[2]:10.3f}    )\n"
                f"Error distance: {np.linalg.norm(solution_error)} meters\n"
                f"Solution Phi, Theta:\t\t({sol_phi:10.3f}, {sol_theta:10.3f}     )\n"
                f"Actual Phi, Theta:\t\t({act_phi:10.3f}, {act_theta:10.3f}     )\n"
                f"Solution Phi, Theta (deg):\t({sol_phi_deg:10.3f}, {sol_theta_deg:10.3f}     )\n"
                f"Actual Phi, Theta (deg):\t({act_phi_deg:10.3f}, {act_theta_deg:10.3f}     )\n"
                f"Error Phi, Theta:\t\t({err_phi:10.3f}, {err_theta:10.3f}     )\n"
                f"Error Phi, Theta (deg):\t\t({err_phi_deg:10.3f}, {err_theta_deg:10.3f}     )\n"
                f"\n--------------------------------------------------\n\n")
            f.close()
    else:
        with open(infile, 'w') as f:
            f.write(
                f"t_start: {t_start_sec}ns\nerror1: {error1_sec}ns\nerror2: "
                f"{error2_sec}ns\nerror3: {error3_sec}ns\nerror4: {error4_sec}ns\n"
                f"TX2toRX1_actual: {TX2toRX1_actual_sec - t_start_sec}ns\n"
                f"TX2toRX2_actual: {TX2toRX2_actual_sec - t_start_sec}ns\n"
                f"TX2toRX3_actual: {TX2toRX3_actual_sec - t_start_sec}ns\n"
                f"TX2toRX4_actual: {TX2toRX4_actual_sec - t_start_sec}ns\n"
                f"Solution:\t({solution[0]:10.3f}, {solution[1]:10.3f}, {solution[2]:10.3f}    )\n"
                f"Actual:\t\t({float(TX.x):10.3f}, {float(TX.y):10.3f}, {float(TX.z):10.3f}    )\n"
                f"Error:\t\t({solution_error[0]:10.3f}, {solution_error[1]:10.3f}, {solution_error[2]:10.3f}    )\n"
                f"Error distance: {np.linalg.norm(solution_error)} meters\n"
                f"Solution Phi, Theta:\t\t({sol_phi:10.3f}, {sol_theta:10.3f}     )\n"
                f"Actual Phi, Theta:\t\t({act_phi:10.3f}, {act_theta:10.3f}     )\n"
                f"Solution Phi, Theta (deg):\t({sol_phi_deg:10.3f}, {sol_theta_deg:10.3f}     )\n"
                f"Actual Phi, Theta (deg):\t({act_phi_deg:10.3f}, {act_theta_deg:10.3f}     )\n"
                f"Error Phi, Theta:\t\t({err_phi:10.3f}, {err_theta:10.3f}     )\n"
                f"Error Phi, Theta (deg):\t\t({err_phi_deg:10.3f}, {err_theta_deg:10.3f}     )\n"
                f"\n--------------------------------------------------\n\n")
            f.close()

    return TX, solution, solution_error, err_phi_deg, err_theta_deg
    # return 1 is the event as a Transmitter object
    # return 2 is the reconstructed event location as a list of (x, y, z, t) coordinates
    # return 3 is the total distance of the error in the reconstructed event in meters
    # return 4 is the error in phi (azimuthal angle) in degrees
    # return 5 is the error in theta (polar angle) in degrees


@dataclass  # a class for data
class Vertexer:
    nodes: np.ndarray
    c: float

    def reconstruct(self, times):
        # Normalize times
        # times -= times.min()
        times -= min(times)

        A = np.append(self.nodes, np.reshape(times, (-1, 1)) * self.c, axis=1)
        # print(f"A: \n{A}")

        def ssr_error(point):
            # Return SSR error
            return np.sum(((np.linalg.norm(self.nodes - point, axis=1) / self.c) - times) ** 2)

        def lorentz(a, b):
            # Return Lorentzian Inner-Product
            return np.sum(a * (b @ M), axis=-1)

        b = lorentz(A, A) * 0.5
        C = np.linalg.solve(A, np.ones(4))
        D = np.linalg.solve(A, b)

        roots = np.roots([lorentz(C, C),
                          (lorentz(C, D) - 1) * 2,
                          lorentz(D, D)])

        solutions = []
        for root in roots:
            X, Y, Z, T = M @ np.linalg.solve(A, root + b)
            solutions.append(np.array([X, Y, Z]))

        return min(solutions, key=ssr_error), max(solutions, key=ssr_error)


def file_name_increment(file_path: str, start_idx: int = 1, prepend_str: str = "-", append_str: str = "", sep: str = ".") -> str:
    if exists(file_path):
        dir_path: str = dirname(file_path)
        file_name_ext: str = basename(file_path)
        file_parts: List[str] = file_name_ext.split(sep)
        file_ext: str = file_parts[-1]
        # just in case file contains multiple sep characters
        file_name: str = sep.join(file_parts[:-1])
        rgx: Pattern = compile(f"(.*{prepend_str})(\d+)({append_str})$")
        if s := findall(rgx, file_name):
            increment = int(s[0][1]) + 1
            new_file_name: str = f"{s[0][0]}{increment}{s[0][2]}"
            new_file_path: str = join(dir_path, f"{new_file_name}{sep}{file_ext}")
        else:
            # if the pattern is not found then the incrementing string is to be appended to the file_name (excl ext)
            new_file_path: str = join(dir_path, f"{file_name}{prepend_str}{start_idx}{append_str}{sep}{file_ext}")
            increment = start_idx + 1
        return file_name_increment(new_file_path, increment, prepend_str, append_str, sep)
    return file_path

# compile()