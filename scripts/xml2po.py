#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import os

from xml.sax import make_parser, saxutils
from xml.sax.handler import ContentHandler, property_lexical_handler
try:
	from _xmlplus.sax.saxlib import LexicalHandler
	no_comments = False
except ImportError:
	class LexicalHandler:
		pass
	no_comments = True

class parseXML(ContentHandler, LexicalHandler):
	def __init__(self, attrlist, filename):
		self.isPointsElement, self.isReboundsElement = 0, 0
		self.currentFile = filename
		self.attrlist = attrlist
		self.last_comment = None
		self.data = ""

	def comment(self, comment):
		if comment.find("TRANSLATORS:") != -1:
			self.last_comment = comment

	def isSkinFile(self, filename):
		return filename.endswith("skin.xml") or (filename.find("skin_default") >= 0 and filename.endswith(".xml"))

	def startElement(self, name, attrs):
		if name == "color":
			return
		self.last_comment = None
		self.data = ""
		translateable = ["text", "title", "value", "caption", "description"]
		if self.isSkinFile(self.currentFile):
			translateable = ["text", "title"]
		for x in translateable:
			if x not in attrs:
				continue
			try:
				attrlist.add((attrs[x], self.last_comment,self.currentFile))
				self.last_comment = None
			except KeyError:
				pass

	def endElement(self, name):
		#print "endElement", name
		if name in ("shortdescription", "description"):
			attrlist.add((self.data.strip(), self.last_comment,self.currentFile))
		self.data = ""

	def characters(self, data):
		self.data += data.strip()


parser = make_parser()

attrlist = set()

for arg in sys.argv[1:]:
	parse_path = ""
	if os.path.isdir(arg):
		for filename in os.listdir(arg):
			if (filename.endswith(".xml")):
				contentHandler = parseXML(attrlist,filename)
				parser.setContentHandler(contentHandler)
				if not no_comments:
					parser.setProperty(property_lexical_handler, contentHandler)
				parser.parse(os.path.join(arg, filename))
	else:
		contentHandler = parseXML(attrlist, arg)
		parser.setContentHandler(contentHandler)
		if not no_comments:
			parser.setProperty(property_lexical_handler, contentHandler)
		parser.parse(arg)

	attrlist = list(attrlist)
	attrlist.sort(key=lambda a: a[2])

	for (k,c,f) in attrlist:
		if c:
			for l in c.split("\n"):
				print("#. ", l)
		if arg == f:
			print("#: %s" % (arg))
		else:
			print("#: %s" % (arg + f))
		msgid = saxutils.escape(k, {'"': '&quot;'}).encode("utf-8")
		msgid = msgid.decode("utf-8")
		msgid.replace("\\n", "\"\n\"")
		msgstr = ""
		if msgid.strip() != "":
			if msgid.find("\&quot;") != -1:
				print("msgid \"%s\"" % (msgid.replace('\&quot;', '\\"')))
			else:
				print("msgid \"%s\"" % (msgid))
			print("msgstr \"%s\"\n" % (msgstr))

	attrlist = set()
