import rupho
import numpy as np
import time
from esa.model import reflectance_photometry_HG2

incidence=[67.67580797096775, 67.67580797096775, 67.67580797096775, 67.67580797096775, 67.67580797096775]
emergence=[79.95437032843954, 75.10576202491056, 72.33048461670337, 75.16566414433859, 79.94872913957556]
phase=[114.47247884029174, 126.62719932417313, 138.96759762739993, 137.68807864875149, 129.5867270508553]
azimuth=[121.8389923034837, 140.9486229612637, 170.6234383544679, -159.34550996693042, -140.5697020250803]
#reflectance=[0.04530722468469045, 0.0184783905976342, NaN, NaN, NaN]
params=[0.3, 0.3, 0.5, 30, 0.5, 1]
scene_geometry = (incidence, emergence, azimuth, phase)

# Time the Rust function
print(incidence, emergence)
print(rupho.reflectance(*params, *scene_geometry))
print(reflectance_photometry_HG2(*params, incidence, emergence, azimuth))