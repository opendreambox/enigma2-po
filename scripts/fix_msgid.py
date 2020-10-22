#!/usr/bin/python

import os
import fileinput
import sys

replaces = [
	("Please configure at least one valid Nameserver (DNS).", "Please configure at least one valid name server (DNS)."),
	]

files = []

for child in os.listdir('po'):
	if child.endswith(".po") or child.endswith(".pot"):
		files.append("po/%s" %(child,))

for line in fileinput.input(files, inplace=1):
	if not line or line.startswith("#") or line.startswith("msgstr"):
		isMsgId = False
	elif line.startswith("msgid"):
		isMsgId = True
	if isMsgId:
		for r in replaces:
			line = line.replace(*r)
	sys.stdout.write(line)
