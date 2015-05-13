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
#prevent annoying scappy warnings
import sys
with open("/dev/null", "w") as f:
    out,err = sys.stdout, sys.stderr
    sys.stdout, sys.stderr = f, f
    from scapy.all import *
    sys.stdout, sys.stderr = out,err

#global that is tuned for the delay before sniffing
SNIFF_WAIT = 0.25

#various functions

def randomMac():
    n = [random.randint(0,255),random.randint(0,255),random.randint(0,255),random.randint(0,255),random.randint(0,255),random.randint(0,255)]
    n[0] &= 0b11111100 #make factory mac and not an boardcast mac
    return ":".join( map(lambda x: chr(x).encode("hex"), n) )

def ip2num(ip):
    octets = map(int, ip.split("."))
    packed = struct.pack( *tuple(["!BBBB"] + octets) )
    return struct.unpack("!L", packed)[0]

def num2ip(num):
    packed = struct.pack("!L", num)
    unpacked = struct.unpack("!BBBB", packed)
    return ".".join( map(str, list(unpacked)) )

def ipgen(start,stop):
    startIp = ip2num(start)
    stopIp = ip2num(stop)
    
    for x in xrange(startIp, stopIp+1):
        yield num2ip(x)


# ARP packets

def mkpktArpWhoHas(ip, mac=None):
    p = Ether(dst="FF:FF:FF:FF:FF:FF")/ARP(op="who-has")
    if mac: 
         p.src = mac
         p.hwsrc = mac
    p.pdst = ip
    return p


# DHCP packets

def mkpktDhcpDiscover(dhcpServerMac="FF:FF:FF:FF:FF:FF", mac=None):
    p = Ether(dst=dhcpServerMac)/IP(src="0.0.0.0", dst="255.255.255.255")/UDP(sport=68,dport=67)/BOOTP()/DHCP(options=[("message-type","discover"),"end"])
    if mac: p.src=mac
    p.chaddr = p.src.replace(":","").decode("hex")
    return p

def mkpktDhcpRequest(pkt):
    p = Ether(dst=pkt.src, src=pkt.dst) \
    /IP(src=pkt['IP'].dst, dst=pkt['IP'].src) \
    /UDP(sport=68,dport=67) \
    /BOOTP() \
    /DHCP(options=[("message-type","request"), ("server_id", pkt['IP'].src), ("requested_addr",pkt['IP'].dst), ('lease_time', 3600), "end"])

    p.chaddr = p.src.replace(":","").decode("hex")
    return p

def mkpktDhcpRevoke(mac, ip, dhcpServerMac="FF:FF:FF:FF:FF:FF"):
    p = Ether(src=mac, dst=dhcpServerMac)/IP(src=ip, dst="255.255.255.255")/UDP(sport=68,dport=67)/BOOTP()/DHCP(options=[("message-type","release"),"end"])
    p.chaddr = p.src.replace(":","").decode("hex")
    p.ciaddr = ip
    return p

