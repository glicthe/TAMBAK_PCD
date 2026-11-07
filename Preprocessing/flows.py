from denoise import median, gaussian, bilateral
from contrast import clahe, hist_eq
from sharpen import unsharp, laplacian

DENOISERS = {"median": median, "gaussian": gaussian, "bilateral": bilateral}


def make_flows(denoise="median"):
    """Build the flow table using the chosen denoise filter."""
    d = DENOISERS[denoise]
    return {
        "A": lambda x: x,
        "B": d,
        "C": lambda x: clahe(d(x)),
        "D": lambda x: unsharp(clahe(d(x))),
        # Extras so HE and Laplacian are actually compared. Drop them if you cut those techniques.
        "E": lambda x: hist_eq(d(x)),
        "F": lambda x: laplacian(clahe(d(x))),
    }


FLOWS = make_flows("median")