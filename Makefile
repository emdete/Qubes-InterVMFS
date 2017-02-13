#!/usr/bin/env make -f
#
# see file:///usr/share/doc/python-llfuse-doc/html/index.html
# see https://www.qubes-os.org/doc/qrexec2/
#
all:

run:
	mkdir -p mnt
	python3 -u usr/bin/QubesInterVMFS.py targetvm "`pwd`/mnt" 1
	fusermount -u mnt

dbg:
	python3 -u usr/bin/QubesInterVMFSd.py "/tmp"

tgz:
	tar cvzf qubes-intervmfs_0.0_all.tgz etc usr

