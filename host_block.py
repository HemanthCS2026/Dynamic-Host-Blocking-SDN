from pox.core import core
import pox.openflow.libopenflow_01 as of

# Initialize logger
log = core.getLogger()

# IP address of the host to be blocked
blocked_ip = "10.0.0.2"

# Dictionary to store MAC-to-port mapping (for learning switch)
mac_to_port = {}


def _handle_PacketIn(event):
    """
    This function handles incoming packets from the switch.
    It implements:
    1. Host blocking (firewall behavior)
    2. Normal learning switch forwarding
    """

    packet = event.parsed
    dpid = event.connection.dpid

    # Initialize dictionary for this switch
    mac_to_port.setdefault(dpid, {})

    # Learn source MAC address → port mapping
    mac_to_port[dpid][packet.src] = event.port

    # Extract IPv4 packet (if present)
    ip = packet.find('ipv4')

    # -------------------------------
    # BLOCK LOGIC (FIREWALL)
    # -------------------------------
    if ip and str(ip.srcip) == blocked_ip:
        log.info("Blocking host %s", ip.srcip)

        # Create flow rule to DROP packets from blocked IP
        msg = of.ofp_flow_mod()
        msg.match.dl_type = 0x800  # Match IPv4 packets
        msg.match.nw_src = ip.srcip  # Match source IP
        msg.actions = []  # No action = DROP

        # Send rule to switch
        event.connection.send(msg)
        return

    # -------------------------------
    # NORMAL LEARNING SWITCH LOGIC
    # -------------------------------
    if packet.dst in mac_to_port[dpid]:
        # Known destination → forward to correct port
        out_port = mac_to_port[dpid][packet.dst]
    else:
        # Unknown destination → flood
        out_port = of.OFPP_FLOOD

    # Create packet out message
    msg = of.ofp_packet_out()
    msg.data = event.ofp
    msg.actions.append(of.ofp_action_output(port=out_port))

    # Send packet to switch
    event.connection.send(msg)


def launch():
    """
    Entry point of the POX controller module.
    Registers PacketIn event handler.
    """
    core.openflow.addListenerByName("PacketIn", _handle_PacketIn)
