# Dynamic Host Blocking System using SDN

## 1. Problem Statement

In modern networks, malicious or suspicious hosts can disrupt communication by generating unwanted traffic. Traditional networks lack dynamic control to handle such threats.
This project aims to **detect and block suspicious hosts dynamically using Software Defined Networking (SDN)** by installing flow rules in real time.

---

## 2. Objective

* To implement an SDN-based network using Mininet
* To monitor network traffic using a controller
* To identify suspicious host behavior
* To dynamically block malicious hosts
* To allow normal traffic without interruption

---

## 3. Tools & Technologies Used

* **Mininet** – Network emulator for creating virtual topology
* **POX Controller** – SDN controller for implementing logic
* **OpenFlow Protocol** – Communication between switch and controller
* **Ubuntu Linux** – Development environment

---

## 4. Network Topology

* 3 Hosts: h1, h2, h3
* 1 Switch: s1
* 1 Controller (POX)

```
h1 ----\
        s1 ---- Controller
h2 ----/
h3 ----/
```

---

## 5. Working Principle

1. When a packet arrives at the switch without a matching rule, it sends a **PacketIn** message to the controller
2. The controller analyzes the packet
3. If the source IP is **10.0.0.2**, it is marked as suspicious
4. The controller installs a **flow rule with DROP action** in the switch
5. The switch blocks all future packets from that host
6. Other hosts continue normal communication

---

## 6. Controller Logic (Implementation)

* Uses `_handle_PacketIn()` event handler
* Implements **match-action flow rule**

  * Match: Source IP address
  * Action: Drop packets
* Uses learning switch logic for normal traffic forwarding

---

## 7. Steps to Run the Project

### Step 1: Start POX Controller

```bash
cd ~/pox
python3 pox.py host_block
```

---

### Step 2: Start Mininet

```bash
sudo mn --topo single,3 --controller remote
```

---

### Step 3: Test Network Behavior

#### Allowed Traffic

```bash
h1 ping -c 3 h3
```

**Expected Output:**

```
0% packet loss
```

---

#### Blocked Traffic

```bash
h2 ping -c 3 h1
```

**Expected Output:**

```
100% packet loss
```

---

## 8. Flow Table Verification

To verify installed flow rules:

```bash
sudo ovs-ofctl dump-flows s1
```

**Observation:**

* Flow entry exists for source IP `10.0.0.2`
* Action: `DROP`
* Confirms that blocking rule is installed in switch

---

## 9. Performance Observation

* Allowed hosts show low latency (~1–3 ms)
* Blocked host shows **100% packet loss**
* Demonstrates efficient filtering using SDN
* No impact on normal traffic

---

## 10. Results

* Normal traffic successfully forwarded
* Suspicious host dynamically blocked
* Controller enforces security policies in real time
* Network behavior changes dynamically based on rules

---

## 11. Proof of Execution

The following screenshots are included:

* Controller running
* Mininet topology
* Allowed traffic output
* Blocked traffic output
* Controller log (blocking message)
* Flow table output

---

## 12. Conclusion

This project demonstrates how SDN enables centralized and dynamic control of network behavior.
By using a controller, we can detect malicious activity and enforce security policies by installing flow rules directly in the network switch.

---

## 13. References

* Mininet Official Documentation
* POX Controller Documentation
* OpenFlow Specification
