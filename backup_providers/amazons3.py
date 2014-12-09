#!/usr/bin/python

import boto

class AmazonS3:
	def __init__(self, keyid, key):
		# Create the connection
		self.conn = boto.connect_s3(keyid, key)
		self.log = "Using Amazon S3\n"
		
	def checkLocation(self, base_dir, backup_type):
		self.base_dir = base_dir
		self.backup_type = backup_type

		# get the bucket.  This API creates the bucket if it doesn't exist, and returns the bucket object if it does.
		self.bucket = self.conn.create_bucket(base_dir + "-pyback")
	

	def pushBackup(self, backup_name, backup_file):
		backup_file += "/" + backup_name
		try:
			# Create the backup name to work with the RS Cloud pseudo-directory
			self.backup_name = self.backup_type + "/" + backup_name
		
			self.log += "Creating object for backup file\n"
			key = self.bucket.new_key(self.backup_name)
		
			# Upload the backup file to remote storage
			key.set_contents_from_filename(backup_file)
			key.set_acl=('private')
			return "Ok"
<<<<<<< HEAD
		except Exception, e:
			self.log += "There was an error creating the remote backup:\n\n"
			self.log += e
=======
		except:
			self.log += "There was an error creating the remote backup.\n"
>>>>>>> 5b29aac12466425617c53ee7ce11f67e132c3a6c
			self.log += "Backup file is located at " + backup_file + "\n"
			self.log += "Please move the backup manually\n"
			return "Error"
	
	def rotateBackup (self, maxFiles):
		# Get the current number of objects for this bckup type
		self.log += "Checking for old backups\n"
		priorBackups = self.bucket.list(prefix=self.backup_type)

		archives = []
		for backup in priorBackups:
			archives.append(backup.name)
		currentBackups = len(archives)

		if currentBackups <= maxFiles:
			self.log += "Number of backups (" + str(currentBackups) + ") has not reached the maximum threshold (" + str(maxFiles) + "). Will not remove previous backups.\n"
		else:
			while currentBackups > maxFiles:
				
				# Set the filename to be the first file returned.  Since we're using date-formatted filenames, this works.  Other naming schemes will require adjustment here.
				filename =archives[0]
				filename = str(filename)
				self.log += "Deleting " + filename + "\n"
				
				# Delete the object
				self.bucket.get_key(filename).delete()
				
				currentBackups -= 1