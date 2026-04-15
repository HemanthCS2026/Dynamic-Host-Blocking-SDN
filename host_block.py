from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()
blocked_ip = "10.0.0.2"

mac_to_port = {}

def _handle_PacketIn(event):
    packet = event.parsed
    dpid = event.connection.dpid

    mac_to_port.setdefault(dpid, {})
    mac_to_port[dpid][packet.src] = event.port

    ip = packet.find('ipv4')

    # BLOCK suspicious host
    if ip and str(ip.srcip) == blocked_ip:
        log.info("Blocking host %s", ip.srcip)

        msg = of.ofp_flow_mod()
        msg.match.dl_type = 0x800
        msg.match.nw_src = ip.srcip
        msg.actions = []  # drop
        event.connection.send(msg)
        return

    # NORMAL forwarding (learning switch)
    if packet.dst in mac_to_port[dpid]:
        out_port = mac_to_port[dpid][packet.dst]
    else:
        out_port = of.OFPP_FLOOD

    msg = of.ofp_packet_out()
    msg.data = event.ofp
    msg.actions.append(of.ofp_action_output(port=out_port))
    event.connection.send(msg)


def launch():
    core.openflow.addListenerByName("PacketIn", _handle_PacketIn)
