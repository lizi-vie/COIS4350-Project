#include <Eigen/Dense>
#include <iostream>
#include <chrono>
#include <fstream>
#ifdef _OPENMP
#include <omp.h>
#endif
#include <vector>
#include <algorithm>
using namespace Eigen;
using namespace std;
using namespace std::chrono;

int main()
{
    // set the size of the matrices
    int n = 4096;
    MatrixXd a = MatrixXd::Random(n, n);
    MatrixXd b = MatrixXd::Random(n, n);
    MatrixXd c(n, n);

    int num_trials = 5;   // num of trials
    vector<double> times; // to store execution times

    // run the benchmark multiple times
    for (int trial = 0; trial < num_trials; trial++)
    {
        auto start = high_resolution_clock::now();
// parallelize the outer loop using OpenMP
#pragma omp parallel for schedule(dynamic)
        for (int i = 0; i < n; i++)
        {
            c.row(i) = a.row(i) * b;
        }
        auto end = high_resolution_clock::now();
        double totaltime = duration<double>(end - start).count();
        times.push_back(totaltime); // store the time for this trial
    }

    // calculate statistics: mean, min & max
    double meantime = 0.0;
    for (double time : times)
        meantime += time;
    meantime /= num_trials;

    // // find min and max times
    double mintime = *min_element(times.begin(), times.end());
    double maxtime = *max_element(times.begin(), times.end());

    // write results to CSV
    ofstream outfile("cpp3_results.csv");
    outfile << "language,implementation,matrixsize,meantime(s),mintime(s),maxtime(s),numtrials\n";
    outfile << "c/c++,advanced(openmp_eigen)," << n << "," << meantime << "," << mintime << "," << maxtime << "," << num_trials << "\n";
    outfile.close();

    cout << "Results written to cpp3_results.csv" << endl;
    return 0;
}