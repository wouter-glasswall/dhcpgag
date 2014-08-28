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

===================================================================

This is the source package of dhcpgag.
The makefile will generate a debain package named "dhcpgag.deb" which you can (un)install at your leisure.

Building package:
make

Purge building residu files
make clean

Manual install withoutout a package:
Install python 2.X (preferably 2.7)
Install scapy (2.2 or higher)

Just copy the following files to the smae directory and give them executable rights:
- dhcpdrain.py
- dhcprevoker.py
- dhcpshow.py
- dhcpheal.py
- pktgen.py

===================================================================
Changelog

0.1
    - Initial release
0.2
    - Added healing options to the toolkit (dhcpdrain, dhcpheal)

