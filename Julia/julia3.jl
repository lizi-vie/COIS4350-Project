using LinearAlgebra, BenchmarkTools, CSV, DataFrames, Dates

# set matrix size
n = 4096

# generate random matrices
a = rand(Float64, n, n)
b = rand(Float64, n, n)

# initialize timing variables
local meantime, mintime, maxtime, numtrials
meantime = 0.0
mintime = 0.0
maxtime = 0.0
numtrials = 0
# run the benchmark
try
    println("running benchmark...")
    GC.gc()
    benchresult = @benchmark $a * $b setup=(GC.gc()) samples=10 seconds=10
    meantime = median(benchresult).time / 1e9  # Convert ns to seconds
    mintime = minimum(benchresult).time / 1e9
    maxtime = maximum(benchresult).time / 1e9
    numtrials = length(benchresult.times)
catch e
    println("benchmarking failed or took too long. Falling back to manual timing.")
    start = time()
    c = a * b
    elapsed = time() - start
    meantime = mintime = maxtime = elapsed
    numtrials = 1
end

# create a DataFrame and write to CSV
df = DataFrame(
    language = "julia",
    implementation = "optimized",
    matrixsize = n,
    meantime = meantime,
    mintime = mintime,
    maxtime = maxtime,
    numtrials = numtrials,
    timestamp = now()
)
# write the DataFrame to a CSV file
CSV.write("julia1_results.csv", df)
println("Results written to julia1_results.csv")
