#!/usr/bin/env python3
import hashlib
import os
import sys

if len(sys.argv) < 2:
	sys.exit('Usage: %s filename' % sys.argv[0])


if not os.path.exists(sys.argv[1]):
	sys.exit('ERROR: File "%s" was not found!' % sys.argv[1])

with open(sys.argv[1], 'rb') as f:
	contents = f.read()
	print("SHA1: %s" % hashlib.sha1(contents).hexdigest())
