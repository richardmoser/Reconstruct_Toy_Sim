"""
Author: Richard Moser
Purpose: simulate the transmission of a signal from a transmitter to a receiver
with a given speed of light in the medium and a resulting time delay
"""
from dataclasses import dataclass
import numpy as np


@dataclass
class Antenna:
    x: float
    y: float
    z: float
    number: int
    type: str


class Receiver(Antenna):
    def __init__(self, x, y, z, number):
        self.x = x
        self.y = y
        self.z = z
        self.number = number
        self.time_received = 0
        self.event_radius = 0
        self.type = "Receiver"


class Transmitter(Antenna):
    def __init__(self, x, y, z, number):
        self.x = x
        self.y = y
        self.z = z
        self.number = number
        self.type = "Transmitter"
        self.time_to_reach: list = [0]

    def transmit(self, rx, c):  # RUN ME IN SEQUENTIAL ORDER!!!
        distance = np.sqrt((rx.x - self.x) ** 2 + (rx.y - self.y) ** 2)
        time_delay = distance / c
        self.time_to_reach.append(time_delay)
        # print(self.time_to_reach)

        return time_delay

    def transmit3D(self, rx, c):  # RUN ME IN SEQUENTIAL ORDER!!!
        distance = np.sqrt((rx.x - self.x) ** 2 + (rx.y - self.y) ** 2 + (rx.z - self.z) ** 2)
        time_delay = distance / c
        self.time_to_reach.append(time_delay)
        # print(self.time_to_reach)

        return time_delay


import os


def generate_available_filename(infile):
    if infile + ".txt" in os.listdir():
        for i in range(1, 1000):
            if infile + f" ({i}).txt" in os.listdir():
                continue
            else:
                print(f"Files up to {infile} ({i - 1}).txt already exist")
                infile = f"data/{infile} ({i}).txt"
                break
        else:
            print("No available file names found")
            return None
    else:
        infile = f"data/{infile} (1).txt"

    return infile


# Example usage
filename = "infile"

available_filename = generate_available_filename(filename)
if available_filename is not None:
    print("Available file name:", available_filename)

