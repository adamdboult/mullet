# gnuplot script file for plotting bandwidth over time
#!/usr/bin/gnuplot
reset
set terminal png

set xdata time
set timefmt "%d/%m/%Y"
set format x "%m %y"	
set xtics rotate

set key autotitle columnheader below

set grid

set datafile separator ","

set output outputpath
plot filename using 1:2 with lines title columnhead
