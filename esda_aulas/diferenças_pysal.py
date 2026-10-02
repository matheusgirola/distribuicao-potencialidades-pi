import numpy as np
import libpysal
from esda.moran import Moran_BV, Moran_Local_BV

# 1. Generate random reproducible spatial data
np.random.seed(42)
n_side = 10
n = n_side * n_side  # 100 observations

x = np.random.randn(n)
y = np.random.randn(n)

# 2. Create a row-standardized spatial weights matrix (10x10 Grid)
w = libpysal.weights.lat2W(n_side, n_side)
w.transform = 'R'  # Row-standardized

# 3. Compute Global Bivariate Moran's I
global_bv = Moran_BV(y, x, w)

# 4. Compute Local Bivariate Moran's I
local_bv = Moran_Local_BV(y, x, w)

# 5. Extract values to test the mathematical identity
I_global = global_bv.I
sum_I_local = np.sum(local_bv.Is)
derived_global = sum_I_local / (n - 1)

# Output results
print(f"Number of observations (n): {n}")
print(f"Global Moran BV attribute (.I): {I_global:.6f}")
print(f"Sum of Local Moran BV (.Is):     {sum_I_local:.6f}")
print(f"Sum of Local Is / (n - 1):       {derived_global:.6f}")
print(f"Identity holds true?             {np.isclose(I_global, derived_global)}")
