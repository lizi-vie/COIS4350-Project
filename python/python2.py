import numpy as np, time, csv, statistics

# matrix size
n = 4096

# generate random matrices
a = np.random.rand(n, n)
b = np.random.rand(n, n)

# run multiple trials to gather more statistics
times = []
num_trials = 3  

for _ in range(num_trials):
    start = time.perf_counter()
    c = np.dot(a, b)
    end = time.perf_counter()
    times.append(end - start)

# calculate timing statistics
meantime = statistics.mean(times)
mintime = min(times)
maxtime = max(times)

# save results  CSV file
with open("python2_results.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["language", "implementation", "matrixsize", "meantime(s)", "mintime(s)", "maxtime(s)", "numtrials"])
    writer.writerow(["python", "optimized(numpy)", n, f"{meantime:.6f}", f"{mintime:.6f}", f"{maxtime:.6f}", num_trials])

print(f"Results written to python2_results.csv for n = {n}")