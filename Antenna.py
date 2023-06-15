"""
Author: Richard Moser
Purpose: simulate the transmission of a signal from a transmitter to a receiver
with a given speed of light in the medium and a resulting time delay
"""
import string
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


