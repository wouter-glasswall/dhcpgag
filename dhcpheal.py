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
import time
import argparse
import sys
sys.path.append("/usr/lib")
from pktgen import *
sys.path.pop()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Revoke all ips from the heal file and thus ending the dhcp server dos.")
    parser.add_argument("interface", type=str, help="The interface where to heal the DHCP server.")

    parser.add_argument("dhcpmac", type=str, help="The mac address of the dhcp server to attack.")

    parser.add_argument("healfile", type=str, help="The healing file created by dhcpdrain.")

    parser.add_argument("--dt", type=float, help="The time between packets of the arp scanner (Default: 0.01)")
    args = parser.parse_args()

    dt = 0.01
    if args.dt: dt = args.dt

    with open(args.healfile) as f:
        for line in f:
            mac, ip = line.strip().split("\t")
            print "Healing revoke of [%s](%s)" % (mac,ip)
            sendp(mkpktDhcpRevoke(mac, ip, args.dhcpmac), iface=args.interface, verbose=False)
            time.sleep(dt)

