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
			self.log += "Folder " + self.backup_type + " does not exist.\n"
			self.createSubFolder(self.backup_type)

	def pushBackup(self, backup_name, backup_file):
		backup_file += "/" + backup_name
		try:
			# Create the backup name to work with the RS Cloud pseudo-directory
			self.backup_name = self.backup_type + "/" + backup_name
		
			self.log += "Creating object for backup file\n"
			rsFile = self.cont.create_object(self.backup_name)
		
			# Upload the backup file to remote storage
			rsFile.load_from_filename(backup_file)
			return "Ok"
		except:
			self.log += "There was an error creating the remote backup.\n"
			self.log += "Backup file is located at " + backup_file + "\n"
			self.log += "Please move the backup manually\n"
			return "Error"
	
	def rotateBackup (self, maxFiles):
		# Get the current number of objects for this bckup type
		self.log += "Checking for old backups\n"
		priorBackups = self.cont.get_objects(path=self.backup_type)
		currentBackups = len(priorBackups)

		if currentBackups <= maxFiles:
			self.log += "Number of backups (" + str(currentBackups) + ") has not reached the maximume threshold (" + str(maxFiles) + "). Will not remove previous backups.\n"
		else:
			while currentBackups > maxFiles:
				# Obtain the list of files and store as an array
				files = self.cont.get_objects(path=self.backup_type)
				
				# Set the filename to be the first file returned.  Since we're using date-formatted filenames, this works.  Other naming schemes will require adjustment here.
				filename = files[0]
				filename = str(filename)
				self.log += "Deleting " + filename + "\n"
				
				# Delete the object
				self.cont.delete_object(filename)
				currentBackups -= 1
	
