use Time, Random, IO;

config const num_trials = 2; // number of benchmark trials
config const n = 4096;  // matrix size

var times: [1..num_trials] real;  // array to store timings

var A, B, C: [1..n, 1..n] real;

// random number generator
var rng = new randomStream(real, seed=12345); // fixed seed for reproducibility

// fill matrices with random values
rng.fill(A);
rng.fill(B);

for trial in 1..num_trials {
  var timer: stopwatch;
  timer.start();

  // parallel matrix multiplication
  forall (i, j) in C.domain {
    var sum: real = 0.0;
    for k in 1..n {
      sum += A[i, k] * B[k, j];
    }
    C[i, j] = sum;
  }

  timer.stop();
  times[trial] = timer.elapsed();
  timer.clear();

  C = 0.0;
}


//statistics
var meantime = (+ reduce times) / num_trials;
var mintime = min reduce times;
var maxtime = max reduce times;

//results
writeln("language,implementation,matrixsize,meantime(s),mintime(s),maxtime(s),numtrials");
writeln("chapel,parallel(forall),", n, ",", meantime, ",", mintime, ",", maxtime, ",", num_trials);
stdout.flush();
