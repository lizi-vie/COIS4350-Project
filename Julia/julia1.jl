using LinearAlgebra, BenchmarkTools, CSV, DataFrames, Dates

n = 4069
a = rand(Float64, n, n)
b = rand(Float64, n, n)
# initialize
meantime = mintime = maxtime = 0.0
numtrials = 0

try
    # run the benchmark
    println("running benchmark")
    GC.gc()
    benchresult = @benchmark $a * $b setup=(GC.gc()) seconds=10

    println("Raw benchmark result:")
    display(benchresult)

    times_ns = benchresult.times  
    if !isempty(times_ns)
        meantime = median(times_ns) / 1e9
        mintime = minimum(times_ns) / 1e9
        maxtime = maximum(times_ns) / 1e9
        numtrials = length(times_ns)
    else
        error("No benchmark samples recorded.")
    end
catch e
    println("benchmarking failed or took too long. Falling back to manual timing.")
    start = time()
    c = a * b
    elapsed = time() - start
    meantime = mintime = maxtime = elapsed
    numtrials = 1
end
# print the results
println(" results before writing:")
println("Meantime: $meantime, Min: $mintime, Max: $maxtime, Trials: $numtrials")
# create a DataFrame
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
