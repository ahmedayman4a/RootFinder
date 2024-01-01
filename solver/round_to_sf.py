import numpy as np


def round_to_sf(x,sf):
    if x == 0:
        return 0
    return round(x, -int(np.floor(np.log10(abs(x)))) + (sf - 1))
    
