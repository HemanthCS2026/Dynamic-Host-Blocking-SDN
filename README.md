# Dynamic Host Blocking System using SDN

## Objective

To dynamically detect and block suspicious hosts using an SDN controller.

## Tools Used

* Mininet
* POX Controller
* OpenFlow

## Topology

3 hosts (h1, h2, h3) connected to 1 switch.

## Working

* Controller monitors PacketIn events
* Detects suspicious host (10.0.0.2)
* Installs drop rule
* Blocks traffic dynamically

## Steps to Run

1. Start controller
   python3 pox.py host_block

2. Start Mininet
   sudo mn --topo single,3 --controller remote

3. Test
   h1 ping h3 → allowed
   h2 ping h1 → blocked

## Output

* Normal hosts communicate successfully
* Suspicious host is blocked

## Conclusion

SDN enables dynamic control of network traffic using centralized controller.
