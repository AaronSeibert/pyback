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
		self.log += "Creating folder " + folder + "\n"
		rsfolder = self.cont.create_object(folder)
		rsfolder.content_type = "application/directory"
		rsfolder.write("")
		self.log += folder + " has been created.\n"
	
	def checkLocation(self, base_dir, backup_type):
		self.base_dir = base_dir
		self.backup_type = backup_type

		try:	
			# First we try to access the container.  If it exists, we set make the object
			# available to the class
			self.cont = self.conn.get_container(base_dir)
		except cloudfiles.errors.NoSuchContainer:
			# If the container doesn't exist, we create it (and the subfolders)
			self.log += "Container " + self.base_dir + " does not exist.  Creating...\n"
			self.cont = self.conn.create_container(self.base_dir)
			self.log += "Container " + self.base_dir + " has been created.\n"

			#Creates the subfolders
			self.createSubFolder(self.backup_type)

		self.log += "Using container " + self.cont.name + "\n"

		try:
			# Now we try to access the backup type "folder".
			self.cont.get_object(self.backup_type)
		except cloudfiles.errors.NoSuchObject:
			# If the backup "folder" doesn't exist, create it
			self.log += "Folder " + self.backup_type + " does nto exist.\n"
			self.createSubFolder(self.backup_type)
			
