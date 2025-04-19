import random, time, csv, sys, statistics
# n is the size of the matrix
n = int(sys.argv[1]) if len(sys.argv) > 1 else 4096

# generate matrices
a = [[random.random() for _ in range(n)] for _ in range(n)]
b = [[random.random() for _ in range(n)] for _ in range(n)]

# naive matrix multiplication
def naivemul(a, b):
    m = len(a)
    n = len(a[0])
    p = len(b[0])
    c = [[0.0 for _ in range(p)] for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                c[i][j] += a[i][k] * b[k][j]
    return c


# run multiple trials to get stable stats
times = []
num_trials = 3

# for each trial, measure the time taken to multiply the matrices
for _ in range(num_trials):
    start = time.perf_counter()
    c = naivemul(a, b)
    end = time.perf_counter()
    times.append(end - start)
# get mean, min, max
meantime = statistics.mean(times)
mintime = min(times)
maxtime = max(times)

# save result
with open("python1_results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["language", "implementation", "matrixsize", "meantime(s)", "mintime(s)", "maxtime(s)", "numtrials"])
    writer.writerow(["python", "naive(purepython)", n, f"{meantime:.6f}", f"{mintime:.6f}", f"{maxtime:.6f}", num_trials])

print(f"results written to python1_results.csv for n = {n}")