from denoise import median
from contrast import clahe, hist_eq
from sharpen import unsharp, laplacian

# Main flows from the roadmap
FLOWS = {
    "A": lambda x: x,
    "B": median,
    "C": lambda x: clahe(median(x)),
    "D": lambda x: unsharp(clahe(median(x))),
    # Extras so HE and Laplacian are actually compared. Drop them if you cut those techniques.
    "E": lambda x: hist_eq(median(x)),
    "F": lambda x: laplacian(clahe(median(x))),
}
