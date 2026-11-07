"""All preprocessing parameters live here. Lock these before any counting (Tahap 7)."""

CFG = {
    # denoise
    "median_k": 5,          # odd; use 3 if thin pematang start to vanish
    "gauss_k": 5,           # odd kernel size
    "gauss_sigma": 0,       # 0 = derived from kernel size
    "bil_d": 9,
    "bil_sigma_color": 75,
    "bil_sigma_space": 75,
    # contrast
    "clip": 2.0,
    "tile": 8,
    # sharpen
    "us_sigma": 1.0,
    "us_amount": 1.0,
    "lap_amount": 0.5,
}
