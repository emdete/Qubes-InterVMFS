QubesInterVMFS
==============

A filesystem for interchanging files between virtual machines under qubes.

This is a proof on concept and not considered as stable, final, mature, secure
or whatever as a tool for qubes is expected! Try it on your own risk.

Installation
------------

dom0:

	etc/qubes-rpc/qubes.QubesInterVMFS

targetvm:

	usr/bin/QubesInterVMFSd.py
	etc/qubes-rpc/qubes.QubesInterVMFS

	dependency: python3

sourcevm:

	usr/bin/QubesInterVMFS.py

	dependency: python3, python3-llfuser

Running
-------

Create a directory.

Run usr/bin/QubesInterVMFS.py with that directory name as first argument.

The home directory of the target vm should be visible in the directory.

Debugging
---------

The two parts are communicating via qrexec-client-vm (see
https://www.qubes-os.org/doc/qrexec2/) but can run standalone (directly using
stdin/out) for debugging purpose. if you add a non-zero second parameter it
will switch on debugging.

On qubes you should see logging in /var/log/qubes/targetvm..., the daemon part
is logging all requests on stderr, the client part is quiet.

