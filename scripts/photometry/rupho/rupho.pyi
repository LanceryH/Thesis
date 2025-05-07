import numpy as np

class MicroStructure:
    """
    Define the microstructure of the surface studied
    """
    
    def __init__(self, w: float, b: float, c: float, z: float, o: float, h: float) -> None:
        self.w: float
        self.b: float
        self.c: float
        self.z: float
        self.o: float
        self.h: float

    def some_method(self) -> float: ...
    
def reflectance(
    w: float,
    b: float,
    c: float,
    dzeta: float,
    b0: float,
    h: float,
    incidence: np.ndarray,
    emergence: np.ndarray,
    azimuth: np.ndarray,
    phase: np.ndarray
) -> np.ndarray:
    ...