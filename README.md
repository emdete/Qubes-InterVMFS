QubesInterVMFS
==============

A filesystem for interchanging files between virtual machines under qubes.

This is a proof on concept and not considered as stable, final, mature, secure
or whatever as a tool for qubes is expected! Try it on your own risk.

Installation
------------

dom0:

	etc/qubes-rpc/qubes.QubesInterVMFS

destvm:

	usr/bin/QubesInterVMFSd.py
	etc/qubes-rpc/qubes.QubesInterVMFS

	dependency: python3

srcvm:

	usr/bin/QubesInterVMFS.py

	dependency: python3, python3-llfuser

Running
-------

Create a directory.

Run usr/bin/QubesInterVMFS.py with the targetvm as first and that directory
name as second argument.

The home directory of the target vm should be readonly accessible in the
directory.

Debugging
---------

The two parts are communicating via qrexec-client-vm (see
https://www.qubes-os.org/doc/qrexec2/) but can run standalone (directly using
stdin/out) for debugging purpose. if you add a non-zero second parameter it
will switch on debugging.

On qubes you should see logging in /var/log/qubes/targetvm..., the daemon part
is logging all requests on stderr, the client part is quiet.

Todos
-----

- configurable shared directory

- anonymise the inodes (currently the original inodes are seen in the client)

- hide files that can't be read anyway

- source code review

- native server

