using LinearAlgebra, BenchmarkTools, CSV, DataFrames

# set the number of threads to use
BLAS.set_num_threads(Sys.CPU_THREADS)

# initialize
n = 4096
a = rand(Float64, n, n)
b = rand(Float64, n, n)

# run the benchmark
GC.enable(false)
benchresult = @benchmark a * b
GC.enable(true)
# get benchmark results
meantime = median(benchresult).time / 1e9
mintime = minimum(benchresult).time / 1e9
maxtime = maximum(benchresult).time / 1e9
numtrials = length(benchresult.times)

# print the results
df = DataFrame(language = "julia", implementation = "optimized+threads", matrixsize = n,
               meantime = meantime, mintime = mintime, maxtime = maxtime,
               numtrials = numtrials)
CSV.write("julia2_results_optimized.csv", df)
println("results written to julia2_results_optimized.csv")
