#!/bin/bash

# Mean of elapsed time in seconds for 5 runs
for i in `seq 1 5`; do { /usr/bin/time --format "real %e" ./call_s_cos  2>&1; }; done | awk '/real/ { num_values++;sum_values += $2}; END { print sum_values/num_values }'
