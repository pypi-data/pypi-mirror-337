import math
import numpy as np

from ..curves.bezier import *


class BezierSpline():
    def __init__(self, curves : list[Bezier]):
        self.curves = curves

    
    def point(self, prog : float):
        return self.curves[int(prog // 1)].point(prog % 1)