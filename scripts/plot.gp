set datafile separator ","
set autoscale
set xtic auto
set ytic auto

set size square

set output "performance.pdf"
set terminal pdf
set title "Performance Under VPM Oversubscription\n".workload
set xlabel "Available PMEM Size (GB)"
set ylabel "Throughput (kops/s)"
set key off

# Convert MB to GB
plot "results.csv" using ($1/1024):2 with linespoints

set output "normalized_performance.pdf"
set terminal pdf
set title "Normalized Performance Under VPM Oversubscription for\n".workload
set xlabel "Available PMEM Size (GB)"
set ylabel "Normalized throughput (%)"
set yrange [0:*]
set format y "%.0f%%"
set key off

# Draw a baseline at 100%
set arrow from graph 0,first 100 to graph 1,first 100 nohead lc rgb 'red' dt 2

# Convert MB to GB
plot "results.csv" using ($1/1024):($3*100) with linespoints

