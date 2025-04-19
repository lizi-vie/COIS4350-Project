import numpy as np, time, csv
from numba import njit, prange
import statistics

# matrix size
n = 4096

# generate random matrices
a = np.random.rand(n, n).astype(np.float64)
b = np.random.rand(n, n).astype(np.float64)

# numba-optimized matrix multiplication, using parallelization
@njit(parallel=True)
def numbamul(a, b):
    n = a.shape[0]
    c = np.zeros((n, n), dtype=a.dtype)
    for i in prange(n):
        for j in range(n):
            for k in range(n):
                c[i, j] += a[i, k] * b[k, j]
    return c

# run multiple trials to gather statistics
times = []
num_trials = 3  

# for each tria  measure the time taken to multiply the matrices
for _ in range(num_trials):
    start = time.perf_counter()
    c = numbamul(a, b)
    end = time.perf_counter()
    times.append(end - start)

# calculate timing statistics
meantime = statistics.mean(times)
mintime = min(times)
maxtime = max(times)

# save results CSV file
with open("python3_results.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["language", "implementation", "matrixsize", "meantime(s)", "mintime(s)", "maxtime(s)", "numtrials"])
    writer.writerow(["python", "advanced(numba)", n, f"{meantime:.6f}", f"{mintime:.6f}", f"{maxtime:.6f}", num_trials])

print(f"Results written to python3_results.csv for n = {n}")