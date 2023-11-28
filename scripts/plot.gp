set datafile separator ","
set autoscale
set xtic auto
set ytic auto


set output "performance_".workload.".pdf"
set terminal pdfcairo enhanced color font "Sans,16" size 3in,2.5in
#set title "Performance Under VPM Oversubscription\n".workload
set xlabel "Available PMEM Size (GB)"
set ylabel "Throughput (Mops/s)" offset 1,0
set key off
set arrow from 48, graph 0 to 48, graph 1 nohead linecolor rgb "red" linewidth 2

# Convert MB to GB
plot "results.csv" using ($1/1024):($2/1024) with linespoints

set output "normalized_performance_".workload.".pdf"
#set terminal pdf
unset title
# set title "Normalized Performance Under VPM Oversubscription for\n".workload
set xlabel "Available PMEM Size (GB)"
set ylabel "Normalized throughput (%)"
set yrange [0:105]
set format y "%.0f%%"
set key off

# Draw a baseline at 100%
# set arrow from graph 0,first 100 to graph 1,first 100 nohead lc rgb 'red' dt 2

# Convert MB to GB
plot "results.csv" using ($1/1024):($3*100) with linespoints

