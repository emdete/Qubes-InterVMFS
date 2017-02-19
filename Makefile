#!/usr/bin/env make -f
#
# see file:///usr/share/doc/python-llfuse-doc/html/index.html
# see https://www.qubes-os.org/doc/qrexec2/
#
.PHONY: all run dbg tgz debian clean

all:
	mkdir -p mnt
	python3 -u usr/bin/QubesInterVMFS debian-9 "`pwd`/mnt"

run:
	mkdir -p mnt
	python3 -u usr/bin/QubesInterVMFS targetvm "`pwd`/mnt" 1
	fusermount -u mnt

dbg:
	qvm-copy-to-vm personal qubes-intervmfs_0.0_all.deb

tgz:
	tar cvzf qubes-intervmfs_0.0_all.tgz etc usr

debian:
	git checkout debian
	git rebase master
	make -f debian/Makefile
	git checkout master

clean:
	rm -rf control control.tar.gz data.tar.gz debian-binary postinst postrm preinst prerm qubes-intervmfs_0.0_all.deb qubes-intervmfs_0.0_all.tgz

