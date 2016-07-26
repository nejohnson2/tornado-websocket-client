#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tornado.ioloop import IOLoop, PeriodicCallback
from tornado import gen
from tornado.websocket import websocket_connect
import json
import couchdb

class Client(object):
	def __init__(self, url):
		self.url = url
		# connect to local couchdb
		self.couch = couchdb.Server('http://127.0.0.1:5984/')
		self.db = self.couch['test']
		self.ioloop = IOLoop.instance()
		self.ws = None
		self.connect()
		PeriodicCallback(self.keep_alive, 10000, io_loop=self.ioloop).start()
		self.ioloop.start()

	@gen.coroutine
	def connect(self):
	'''Connect to server'''
		print "trying to connect"
		try:
			self.ws = yield websocket_connect(self.url)
		except Exception, e:
			print "connection error"
		else:
			print "connected"
			self.run()

	@gen.coroutine
	def run(self):
	'''Read any messages from server websocket
		while True:
			msg = yield self.ws.read_message()
			
			# write to couchdb
			self.db.save(json.loads(msg))
			
			print 'Document saved to db'
			if msg is None:
				print "connection closed"
				self.ws = None
				break

	def keep_alive(self):
		if self.ws is None:
			self.connect()
		else:
			self.ws.write_message('keep alive')

if __name__ == "__main__":
	client = Client("ws://<server>/ws")
