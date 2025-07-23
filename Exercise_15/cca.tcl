# Create a new simulator object
set ns [new Simulator]

# Open trace files
set tracefile [open "congestion.tr" w]
set namfile [open "congestion.nam" w]

# Enable tracing
$ns trace-all $tracefile
$ns namtrace-all $namfile

# Define colors for flows
foreach color {Red Blue White Green} {
    $ns color [expr {[lsearch {Red Blue White Green} $color] + 1}] $color
}

# Create nodes
for {set i 0} {$i < 6} {incr i} {
    set n($i) [$ns node]
}

# Create links
set bw {2Mb 2Mb 0.3Mb 0.5Mb 0.5Mb}
set delay {10ms 10ms 200ms 40ms 30ms}
foreach {from to} {0 2 1 2 2 3 3 4 3 5} {
    $ns duplex-link $n($from) $n($to) [lindex $bw $from] [lindex $delay $from] DropTail
}

# Create TCP agents and attach to nodes
for {set i 0} {$i < 4} {incr i} {
    set tcp($i) [new Agent/TCP/Reno]
    $ns attach-agent $n($i) $tcp($i)
    set sink($i) [new Agent/TCPSink]
    $ns attach-agent $n(4+$i) $sink($i)
    $ns connect $tcp($i) $sink($i)
    $tcp($i) set fid_ [expr $i + 1]
}

# Setup FTP applications
for {set i 0} {$i < 4} {incr i} {
    set ftp($i) [new Application/FTP]
    $ftp($i) attach-agent $tcp($i)
    $ns at [expr 0.5 + $i * 0.1] "$ftp($i) start"
    $ns at [expr 70.0 + $i * 0.1] "$ftp($i) stop"
}

# Setup Ping agents
set p0 [new Agent/Ping]
$ns attach-agent $n(0) $p0
set p1 [new Agent/Ping]
$ns attach-agent $n(4) $p1
$ns connect $p0 $p1

# Define receive procedure for Ping agents
Agent/Ping instproc recv {from rtt} {
    puts "node [$self node] received ping answer from $from with round-trip-time $rtt ms."
}

# Schedule Ping events
$ns at 0.3 "$p0 send"
$ns at 70.1 "$p0 send"
$ns at 70.2 "$p1 send"

# Procedure to plot congestion window
proc plotWindow {tcpSource outfile} {
    global ns
    set now [$ns now]
    set cwnd [$tcpSource set cwnd_]
    puts $outfile "$now $cwnd"
    $ns at [expr $now + 0.1] "plotWindow $tcpSource $outfile"
}

# Open output file for congestion window data
set outfile [open "congestion.xg" w]
$ns at 0.0 "plotWindow $tcp(0) $outfile"

# Set simulation end time and finish procedure
$ns at 80.0 "finish"
proc finish {} {
    global ns tracefile namfile outfile
    $ns flush-trace
    close $tracefile
    close $namfile
    close $outfile
    exec nam congestion.nam &
    exec xgraph congestion.xg -geometry 300x300 &
    exit 0
}

# Run simulation
$ns run
