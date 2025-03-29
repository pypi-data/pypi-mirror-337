import math
import numpy as np


class Bezier():
    def __init__(self, points : np.ndarray):
        self.points = points


    def basis(self):
        n = self.points.shape[0] - 1
        basis_mat = np.zeros((n+1, n+1))
        
        for j in range(n + 1):
            for i in range(n + 1):
                if j >= i:
                    basis_mat[j][i] = math.comb(n, i) * ((-1) ** (j - i)) * math.comb(n - i, j - i)
                else:
                    basis_mat[j][i] = 0

        return basis_mat

    
    def point(self, prog : float):
        poly_mat = np.array([(prog % 1) ** i for i in range(self.points.shape[0])])
        
        return poly_mat @ self.basis() @ self.points[int(prog) : int(prog) + 3 + 1]