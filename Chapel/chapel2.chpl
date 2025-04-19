use Time, Random, IO;

config const num_trials = 2; // number of benchmark trials
config const n = 4096;       // matrix size

var times: [1..num_trials] real; // array to store timings

// iinitialize matrices
var A, B, C: [1..n, 1..n] real;
A = 1.0; B = 2.0; // iinitialize

for trial in 1..num_trials {
    var timer: stopwatch; // create timer
    timer.start(); // start timing

    // optimized matrix multiplication kernel (loop reeordered 4 cache locality)
    for i in 1..n do
        for k in 1..n do {
            const aik = A[i, k]; // cache value - avoid repeated indexing
            for j in 1..n do
                C[i, j] += aik * B[k, j];
        }

    timer.stop(); // stop timing
    times[trial] = timer.elapsed(); 
    timer.clear(); // reset timer

    C = 0.0; // reset result matrix for next trial
}

// calculate statistics
var meantime = (+ reduce times) / num_trials;
var mintime = min reduce times;
var maxtime = max reduce times;

// print  results
writeln("language,implementation,matrixsize,meantime(s),mintime(s),maxtime(s),numtrials");
writeln("chapel,optimized(forall),", n, ",", meantime, ",", mintime, ",", maxtime, ",", num_trials);
stdout.flush();
