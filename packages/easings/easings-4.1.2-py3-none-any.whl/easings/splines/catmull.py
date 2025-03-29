import numpy as np


class Catmull():
    def __init__(self, points: np.ndarray, tension = 1.0):
        self.points = points
        self.tension = tension


    def point(self, progress: float):
        local_prog = progress - int(progress)
        
        poly_mat = np.array([1, local_prog, local_prog**2, local_prog**3])
        
        basis_mat = np.array([
            [0, 1, 0, 0],
            [-self.tension, 0, self.tension, 0],
            [2 * self.tension, self.tension - 3, 3 - 2 * self.tension, -self.tension],
            [-self.tension, 2 - self.tension, self.tension - 2, self.tension]
        ])
        
        return poly_mat @ basis_mat @ self.points[int(progress) - 1 : int(progress) - 1 + 3 + 1]