#!/usr/bin/python

import cloudfiles

class Rackspace:
	def __init__(self, user, api):
		# Create the Rackspace Cloudfiles connection
		self.conn = cloudfiles.get_connection(user, api)
		self.log = "Using Rackspace Cloudfiles\n"
		
	def createSubFolder(self, folder):
		# Mehod for creating the subfolders
		# API documentation states that best practice is to create a 0 or 1 byte object
		# with content-type of application/directory so the virtual directories can 
		# be enumerated using path=.  So that's what we do here
		rsfolder = self.cont.create_object(folder)
		rsfolder.content_type = "application/directory"
		rsfolder.write("")
	
	def checkLocation(self, location):
		try:	
			# First we try to access the container.  If it exists, we set make the object
			# available to the class
			self.cont = self.conn.get_container(location)
		except cloudfiles.errors.NoSuchContainer:
			# If the container doesn't exist, we create it (and the subfolders)
			self.log += location + " does not exist.  Creating...\n"
			self.cont = self.conn.create_container(location)
			self.log += location + " has been created.\n"
			self.log += "Creating sub-containers...\n"

			#Creates the subfolders
			self.createSubFolder("Daily")
			self.createSubFolder("Weekly")
			self.createSubFolder("Monthly")

			self.log += "Sub-containers created.\n"
		else:
			self.log += "Using " + self.cont.name
