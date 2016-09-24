# gnuplot script file for plotting bandwidth over time
#!/usr/bin/gnuplot
reset
set terminal png

set xdata time
set timefmt "%d/%m/%Y"
set format x "%d/%m/%Y"

set xlabel "Date"
set ylabel filename

set key below
set grid

set datafile separator ","

set output outputpath
plot filename using 1:2 with lines title columnhead
