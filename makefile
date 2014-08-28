#This file is part of Dhcpgag.
#
#Dhcpgag is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#Dhcpgag is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with Foobar.  If not, see <http://www.gnu.org/licenses/>.

all: dhcpgag.deb

clean:
	rm -rf dhcpgag
	rm dhcpgag.deb

dhcpgag.deb: dhcpgag/DEBIAN/control dhcpgag/usr/bin/dhcpheal dhcpgag/usr/bin/dhcpdrain dhcpgag/usr/bin/dhcprevoker dhcpgag/usr/bin/dhcpshow dhcpgag/usr/lib/pktgen.py
	fakeroot "dpkg-deb --build dhcpgag"

dhcpgag/DEBIAN/control: dhcpgag/DEBIAN
	cp control dhcpgag/DEBIAN/

dhcpgag/usr/bin/dhcpheal: dhcpgag/usr/bin/dhcpheal.py
	cd dhcpgag/usr/bin/; \
    ln -s dhcpheal.py dhcpheal; \
	cd -

dhcpgag/usr/bin/dhcpdrain: dhcpgag/usr/bin/dhcpdrain.py
	cd dhcpgag/usr/bin/; \
    ln -s dhcpdrain.py dhcpdrain; \
	cd -

dhcpgag/usr/bin/dhcprevoker: dhcpgag/usr/bin/dhcprevoker.py
	cd dhcpgag/usr/bin/; \
    ln -s dhcprevoker.py dhcprevoker; \
	cd -

dhcpgag/usr/bin/dhcpshow: dhcpgag/usr/bin/dhcpshow.py
	cd dhcpgag/usr/bin/; \
    ln -s dhcpshow.py dhcpshow; \
	cd -

dhcpgag/usr/bin/dhcpheal.py: dhcpgag/usr/bin
	cp dhcpheal.py dhcpgag/usr/bin/; \
	chmod +x dhcpgag/usr/bin/dhcpheal.py

dhcpgag/usr/bin/dhcpdrain.py: dhcpgag/usr/bin
	cp dhcpdrain.py dhcpgag/usr/bin/; \
	chmod +x dhcpgag/usr/bin/dhcpdrain.py

dhcpgag/usr/bin/dhcprevoker.py: dhcpgag/usr/bin
	cp dhcprevoker.py dhcpgag/usr/bin/; \
	chmod +x dhcpgag/usr/bin/dhcprevoker.py

dhcpgag/usr/bin/dhcpshow.py: dhcpgag/usr/bin
	cp dhcpshow.py dhcpgag/usr/bin/; \
	chmod +x dhcpgag/usr/bin/dhcpshow.py

dhcpgag/usr/lib/pktgen.py: dhcpgag/usr/lib
	cp pktgen.py dhcpgag/usr/lib/

dhcpgag:
	mkdir dhcpgag

dhcpgag/DEBIAN: dhcpgag
	mkdir dhcpgag/DEBIAN

dhcpgag/usr: dhcpgag
	mkdir dhcpgag/usr

dhcpgag/usr/lib: dhcpgag/usr
	mkdir dhcpgag/usr/lib

dhcpgag/usr/bin: dhcpgag/usr
	mkdir dhcpgag/usr/bin
