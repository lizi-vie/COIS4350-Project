#include <iostream>
#include <vector>
#include <chrono>
#include <fstream>
#include <cstdlib>
#include <algorithm>
using namespace std;
using namespace std::chrono;

typedef vector<vector<double>> matrix;

// function to multiply two matrices using naive triple nested loops
matrix naivemul(const matrix &a, const matrix &b)
{
    int m = a.size();
    int n = a[0].size();
    int p = b[0].size();
    matrix c(m, vector<double>(p, 0.0));
    for (int i = 0; i < m; i++)
        for (int j = 0; j < p; j++)
            for (int k = 0; k < n; k++)
                c[i][j] += a[i][k] * b[k][j];
    return c;
}

// main
int main()
{
    int n = 4096;
    // set the size of the matrices
    matrix a(n, vector<double>(n)), b(n, vector<double>(n));

    // initialize matrices with random values
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++)
        {
            a[i][j] = rand() / double(RAND_MAX);
            b[i][j] = rand() / double(RAND_MAX);
        }

    int num_trials = 5;   // num of trials
    vector<double> times; // to store execution times

    // run the benchmark multiple times
    for (int trial = 0; trial < num_trials; trial++)
    {
        auto start = high_resolution_clock::now();
        matrix c = naivemul(a, b);
        auto end = high_resolution_clock::now();
        double totaltime = duration<double>(end - start).count();
        times.push_back(totaltime); // store the time taken for this trial
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
    ofstream outfile("cpp1_results.csv");
    outfile << "language,implementation,matrixsize,meantime(s),mintime(s),maxtime(s),numtrials\n";
    outfile << "c/c++,naive(triplenested)," << n << "," << meantime << "," << mintime << "," << maxtime << "," << num_trials << "\n";
    outfile.close();

    cout << "Results written to cpp1_results.csv" << endl;
    return 0;
}