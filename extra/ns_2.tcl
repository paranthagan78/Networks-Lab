# Create a network topology
set ns [new Simulator]

# Enable trace file generation
set tracefile [open "congestion_control.tr" w]
$ns trace-all $tracefile

# Create nodes
set node(0) [$ns node]
set node(1) [$ns node]

# Create links
$ns duplex-link $node(0) $node(1) 10Mb 10ms DropTail

# Set up traffic sources
set tcp [new Agent/TCP]
$tcp set class_ 2
$ns attach-agent $node(0) $tcp

set sink [new Agent/TCPSink]
$ns attach-agent $node(1) $sink

$ns connect $tcp $sink

set ftp [new Application/FTP]
$ftp attach-agent $tcp
$ns at 0.1 "$ftp start" 

# Implement congestion control algorithm
$tcp set cong_algorithm NewReno

# Set simulation parameters
$ns duplex-link-op $node(0) $node(1) orient right-down
$ns color 1 Blue
$ns color 2 Red
$ns at 10.0 "$ns finish"

# Run the simulation
$ns run

# Close the trace file
$ns flush-trace 
close $tracefile

# Launch Nam for visualization
set namfile "congestion_control.nam"
set nam [open $namfile w]
$ns namtrace-all $nam
$ns nam-end-wireless $nam

# Exit NS2
$ns halt
$ns delete
