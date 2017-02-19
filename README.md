Qubes-InterVMFS
==============

A filesystem for interchanging files between virtual machines under qubes.
Current situation is that you just can copy or move a single file from one VM
to another.  If you need access to a whole bunch of files you are lost (or
create a tgz first). Sometimes you don't even want to copy the content. I was
always missing a solution to export a directory tree read only to another VM.
This project solves exactly that.

This is a proof on concept and not considered as stable, final, mature, secure
or whatever as a tool for qubes is expected and should be! Try it on your own
risk.

Installation
------------

The following files are required in the given places:

dom0:

	etc/qubes-rpc/qubes.QubesInterVMFS

srcvm:

	usr/bin/QubesInterVMFS

	dependency: python3, python3-llfuser 1.2+dfsg-1

destvm:

	usr/lib/qubes-intervmfs/QubesInterVMFSd.py
	etc/qubes-rpc/qubes.QubesInterVMFS

	dependency: python3

The Makefile is able to create a tgz and contains a brute force method to
compile a debian package for easier installation and deinstallation.

Running
-------

Create a directory.

Run usr/bin/QubesInterVMFS in the srcvm with the destvm as first and that
directory name as second argument.

The home directory of the destvm should be readonly accessible in the given
directory in the srcvm.

Debugging
---------

The two parts are communicating via qrexec-client-vm (see
https://www.qubes-os.org/doc/qrexec2/) but can run standalone (directly using
stdin/out) for debugging purpose. if you add a non-zero second parameter it
will switch on debugging and run locally.

Todos
-----

- Configurable shared directory

- Anonymise the inodes (currently the original inodes are seen in the client)

- Source code review

- Native server in destvm

