import numpy as np


class BSpline():
    def __init__(self, points : np.ndarray):
        self.points = points


    def point(self, prog : float):
        local_prog = prog - int(prog)

        poly_mat = np.array([1, local_prog, local_prog ** 2, local_prog ** 3])

        basis_mat = 1/6 * np.array([
            [1, 4, 1, 0],
            [-3, 0, 3, 0],
            [3, -6, 3, 0],
            [-1, 3, -3, 1]
        ])

        return poly_mat @ basis_mat @ self.points[int(prog) - 1 : int(prog) - 1 + 3 + 1]