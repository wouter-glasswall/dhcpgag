#!/usr/bin/env python
"""
    This file is part of Dhcpgag.

    Dhcpgag is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Dhcpgag is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Foobar.  If not, see <http://www.gnu.org/licenses/>.
"""
from multiprocessing import Process
from time import sleep
import argparse
import sys
sys.path.append("/usr/lib")
from pktgen import *
sys.path.pop()

def sendfunc(p, num, tx):
    sleep(SNIFF_WAIT)
    
    first = True

    for x in xrange(num):
        if first:
            first = False
        else:
            sleep(tx)
        sendp(p, iface=args.interface, verbose=False)

########################################################################

parser = argparse.ArgumentParser(description='Get layer 2 & 3 adresses of running DHCP servers')
parser.add_argument("interface", type=str, help="The interface where to search for DHCP servers.")
parser.add_argument("--timeout", type=float, help="The time to wait for dhcp reply's. (default: 2.0)")
parser.add_argument("--numpackets", type=int, help="The number of discover packets to send (Default: 3)")
parser.add_argument("--discover-tx", type=float, help="The time to wait in between discover packets (Default: 0.33)")

args = parser.parse_args()


timeout = 3.0
if args.timeout: timeout = args.timeout

numpackets = 3
if args.numpackets: numpackets = args.numpackets

discover_tx = 0.33
if args.discover_tx: discover_tx = args.discover_tx

p = mkpktDhcpDiscover("FF:FF:FF:FF:FF:FF")
Process(target=sendfunc, args=(p,numpackets,discover_tx)).start()
packets = sniff(filter="udp and dst port 68 and src port 67", iface=args.interface, timeout=timeout + SNIFF_WAIT + numpackets*discover_tx)

########################################################################

dhcp_bootreply_packets = filter(lambda x: hasattr(x, "op") and (x.op == 2), packets)
print "%d/%d dhcp offers / dhcp packets " % (len(dhcp_bootreply_packets), len(packets))

boot_pkts = map(lambda pkt: (pkt.src, pkt["IP"].src), dhcp_bootreply_packets)

for pkt in set( boot_pkts ):
    print "%s\t%s" % pkt
