"""
Author: Keith Madison
Modifications: Richard Moser
Purpose: learn something, reconstruct transmitter location from time differences
"""

from dataclasses import dataclass
import numpy as np

M = np.diag([1, 1, -1])


@dataclass
class Vertexer:
    nodes: np.ndarray
    c: float

    def reconstruct(self, times):
        A = np.append(self.nodes, np.reshape(times, (-1, 1)) * self.c, axis=1) # append time to nodes array

        def ssr_error(point):
            # Return SSR error
            #    print('Error: ', np.sum(((np.linalg.norm(self.nodes - point, axis=1) / self.c)
            #                                   - times)**2))
            return np.sum(((np.linalg.norm(self.nodes - point, axis=1) / self.c)
                           - times) ** 2)  # sum of squared residuals

        def lorentz(a, b):
            # Return Lorentzian Inner-Product
            return np.sum(a * (b @ M), axis=-1)  # lorentzian inner product

        b = lorentz(A, A) * 0.5  # b = 1/2 * lorentzian inner product of A with itself
        C = np.linalg.solve(A, np.ones(3))  # solve for C in AC = 1
        D = np.linalg.solve(A, b)  # solve for D in AD = b

        roots = np.roots([lorentz(C, C),
                          (lorentz(C, D) - 1) * 2,
                          lorentz(D, D)])  # solve for roots of polynomial

        solutions = []  # list of solutions
        for root in roots:  # for each root
            X, Y, T = M @ np.linalg.solve(A, root + b)  # solve for X, Y, T
            solutions.append(np.array([X, Y]))  # append solution to list of solutions
            # print(X,Y)

        solution = min(solutions, key=ssr_error)  # find solution with minimum error

        # print(ssr_error(solution))
        return solution, ssr_error(solution)  # return solution and error
