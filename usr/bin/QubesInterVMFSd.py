#!/usr/bin/env python3
from sys import stdin, stderr, stdout
from json import dumps as encode_json, loads as decode_json
from os import listdir, stat, O_RDWR, O_WRONLY, access, R_OK
from random import randint
from base64 import encodestring as encode_base64
from logging import getLogger, StreamHandler, Formatter, DEBUG, INFO
from errno import EPERM, EBADMSG
from faulthandler import enable as enablefaulthandler
from os.path import join as pathjoin, expanduser

enablefaulthandler()
log = getLogger(__name__)

class OpenFile(object):
	def __init__(self, inode, stat):
		self.inode = inode
		self.stat = stat
		self.file = open(stat.name, 'rb')

class OpenDir(object):
	def __init__(self, inode, stat):
		self.inode = inode
		self.name = stat.name
		self.listdir = listdir(stat.name)

class INode(object):
	def __init__(self, name, stat):
		self.name = name
		self.stat = stat

class VmReadFSd(object):
	def __init__(self, root):
		super(VmReadFSd, self).__init__()
		self.root = root
		self.openfiles = dict()
		self.opendirs = dict()
		self.inodes = dict()

	def _getattr(self, name):
		e = stat(name)
		s = dict(
			#st_atime=e.st_atime,
			st_atime_ns=e.st_atime_ns,
			#st_ctime=e.st_ctime,
			st_ctime_ns=e.st_ctime_ns,
			#st_dev=e.st_dev,
			st_gid=e.st_gid,
			st_ino=e.st_ino,
			st_mode=e.st_mode,
			#st_mtime=e.st_mtime,
			st_mtime_ns=e.st_mtime_ns,
			st_nlink=e.st_nlink,
			st_size=e.st_size,
			st_uid=e.st_uid,
			)
		self.inodes[e.st_ino] = INode(name, s)
		return s

	def _readable(self, dirname, name):
		return name[0] != '.' and access(pathjoin(dirname, name), R_OK)

	def getattr(self, inode, ctx):
		if ctx['isroot'] and inode not in self.inodes:
			self._getattr(self.root)
			self.inodes[inode] = INode(self.root, self._getattr(self.root))
		return self.inodes[inode].stat

	def lookup(self, parent_inode, name, ctx):
		if ctx['isroot']:
			name = pathjoin(self.root, name)
		else:
			name = pathjoin(self.inodes[parent_inode].name, name)
		return self._getattr(name)

	def opendir(self, inode, ctx):
		if ctx['isroot'] and inode not in self.inodes:
			self._getattr(self.root)
			self.inodes[inode] = INode(self.root, self._getattr(self.root))
		fh = randint(3,0x7fffffff)
		while fh in self.opendirs:
			fh = randint(3,0x7fffffff)
		self.opendirs[fh] = OpenDir(inode, self.inodes[inode])
		return fh

	def readdir(self, fh, off):
		d = self.opendirs[fh]
		return [(name, self._getattr(pathjoin(d.name, name)), off+index+1)
			for index, name, in enumerate(d.listdir[off:])
			if self._readable(d.name, name)
			]

	def releasedir(self, fh):
		del self.opendirs[fh]
		return

	def open(self, inode, flags, ctx):
		if flags & O_RDWR or flags & O_WRONLY or ctx['isroot']:
			raise OSError(EPERM, 'permission denied')
		fh = randint(3,0x7fffffff)
		while fh in self.openfiles:
			fh = randint(3,0x7fffffff)
		self.openfiles[fh] = OpenFile(inode, self.inodes[inode])
		return fh

	def read(self, fh, off, size):
		f = self.openfiles[fh].file
		f.seek(off)
		return str(encode_base64(f.read(size)).strip(), 'ascii')

	def flush(self, fh):
		return

	def release(self, fh):
		return


def init_logging(debug):
	handler = StreamHandler(stderr)
	handler.setFormatter(Formatter('%(asctime)s.%(msecs)03d %(threadName)s: [%(name)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))
	root_logger = getLogger()
	if debug:
		handler.setLevel(DEBUG)
		root_logger.setLevel(DEBUG)
	else:
		handler.setLevel(INFO)
		root_logger.setLevel(INFO)
	root_logger.addHandler(handler)

def main(mountpoint='~', debug=True):
	mountpoint = expanduser(mountpoint)
	init_logging(debug)
	daemon = VmReadFSd(mountpoint)
	line = stdin.readline()
	while line:
		log.debug("in %s", line)
		try:
			line = decode_json(line)
			for method, parameters in line.items():
				if method in set(('flush', 'getattr', 'open', 'opendir', 'readdir', 'release', 'releasedir', 'read', 'lookup', )):
					method = getattr(daemon, method)
					line = method(*parameters)
					line = encode_json(dict(result=line))
					print(line)
					stdout.flush()
				else:
					raise Exception('unsupported method "{}"'.format(method))
		except OSError as e:
			log.exception(str(e))
			line = encode_json(dict(error=(e.errno, )))
			print(line)
			stdout.flush()
		except Exception as e:
			log.exception(str(e))
			line = encode_json(dict(error=(EBADMSG, )))
			print(line)
			stdout.flush()
		log.debug("out %s", line)
		line = stdin.readline()

if __name__ == '__main__':
	from sys import argv
	main(*argv[1:])
# vim:tw=0:nowrap
