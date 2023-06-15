"""
Author: Keith Madison
Modifications: Richard Moser
Purpose: learn something, reconstruct transmitter location from time differences
"""

from dataclasses import dataclass
from random import randrange
import math
import numpy as np

M = np.diag([1, 1, -1])


@dataclass
class Vertexer:
    nodes: np.ndarray
    c: float

    def reconstruct(self, times):
        A = np.append(self.nodes, np.reshape(times, (-1, 1)) * self.c, axis=1)

        def ssr_error(point):
            # Return SSR error
            #    print('Error: ', np.sum(((np.linalg.norm(self.nodes - point, axis=1) / self.c)
            #                                   - times)**2))
            return np.sum(((np.linalg.norm(self.nodes - point, axis=1) / self.c)
                           - times) ** 2)

        def lorentz(a, b):
            # Return Lorentzian Inner-Product
            return np.sum(a * (b @ M), axis=-1)

        b = lorentz(A, A) * 0.5
        C = np.linalg.solve(A, np.ones(3))
        D = np.linalg.solve(A, b)

        roots = np.roots([lorentz(C, C),
                          (lorentz(C, D) - 1) * 2,
                          lorentz(D, D)])

        solutions = []
        for root in roots:
            X, Y, T = M @ np.linalg.solve(A, root + b)
            solutions.append(np.array([X, Y]))
            # print(X,Y)

        solution = max(solutions, key=ssr_error)
        # print(ssr_error(solution))
        return (solution, ssr_error(solution))



"""Pre - fix code below, requires 4 transmitters in 3d space"""

# M = np.diag([1, 1, 1, -1])
#
#
# @dataclass  # a class for data
# class Vertexer:
#     nodes: np.ndarray
#     c: float
#
#     def reconstruct(self, times):
#         # Normalize times
#         # times -= times.min()
#         times -= min(times)
#
#         A = np.append(self.nodes, np.reshape(times, (-1, 1)) * self.c, axis=1)
#
#         def ssr_error(point):
#             # Return SSR error
#             return np.sum(((np.linalg.norm(self.nodes - point, axis=1) / self.c) - times) ** 2)
#
#         def lorentz(a, b):
#             # Return Lorentzian Inner-Product
#             return np.sum(a * (b @ M), axis=-1)
#
#         b = lorentz(A, A) * 0.5
#         C = np.linalg.solve(A, np.ones(4))
#         D = np.linalg.solve(A, b)
#
#         roots = np.roots([lorentz(C, C),
#                           (lorentz(C, D) - 1) * 2,
#                           lorentz(D, D)])
#
#         solutions = []
#         for root in roots:
#             X, Y, Z, T = M @ np.linalg.solve(A, root + b)
#             solutions.append(np.array([X, Y, Z]))
#
#         return max(solutions, key=ssr_error)
#

