set datafile separator ","
set autoscale
set xtic auto
set ytic auto

set output "performance.pdf"
set terminal pdf
set title "Performance Under VPM Oversubscription"
set xlabel "Available PMEM Size (MB)"
set ylabel "Throughput (kops/s)"
set xrange [*:*] reverse
set key off
plot "results.csv" using 1:2 with linespoints

set output "normalized_performance.pdf"
set terminal pdf
set title "Normalized Performance Under VPM Oversubscription"
set xlabel "Available PMEM Size (MB)"
set ylabel "Normalized throughput (%)"
set xrange [*:*] reverse
set yrange [0:100]
set format y "%.0f%%"
set key off
plot "results.csv" using 1:($3*100) with linespoints

