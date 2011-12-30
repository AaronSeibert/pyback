#!/usr/bin/python
import cloudfiles
import sys
import time
import tarfile
import os

from datetime import date, datetime

# Modify the variables below to match your environment

# Desired log location
logFile = "/var/log/backup"

# Rackspace Cloud Files settings
rackspaceUser = ""
rackspaceAPI = ""

# Database Settings
dbUser = "" # Database User name
dbPass = "" # Database Password
dbHost = "" # Database Host

# Filesystem backup settings
tmpPath = "/tmp"
backupSrc = [
	"/home",
	"/etc"
	]
backupExclude = [
	"/etc/dropbox"
	]

# Number of backup files to keep

maxFiles = {
	'Daily':7,
	'Weekly':4,
	'Monthly':6
	}
	
# DO NOT MODIFY BELOW THIS LINE

backupName = date.today();

# Set the backup type
backupType = sys.argv[1]

# Initiate the connection to RSCloudFiles
conn = cloudfiles.get_connection(rackspaceUser, rackspaceAPI)

def currentTime():
	time = datetime.now()
	return str(time)

def logWrite(string):
	log = open(logFile,"aw")
	log.write(currentTime() + ": " + string + "\n")
	log.close()
	return	

# Checks to verify the backup container exists.  If it does not, creates it.
# Note - This is tailored to RS Cloud.  Could easily be tailored to a mounted FS as well
def checkContainer(container):
	try:
		cont = conn.get_container(container)
		logWrite("Using " + cont.name)
		return cont
	except:
		logWrite(container + " does not exist.  Creating...")
		cont = conn.create_container(container)
		logWrite(container + " created.")
		return cont

# Python's tarfile exclusion function
def tarExclude(filename):
	for item in backupExclude:
		return filename == item

# Deletes opbjects in the RS Cloud container
def delFiles(filename,cont):
	logWrite("Deleting " + filename)
	cont.delete_object(filename)
	return

# Stores the backup file
def pushBackup(backupName,backupFile):
	try:	
		# Push file to RS Cloud
		logWrite("Creating RS Cloud object.")
		rsFile = cont.create_object(backupName)
		logWrite("Uploading backup file.")
		rsFile.load_from_filename(backupFile)
		return "Ok"
	except:
		logWrite("There was an error pushing the backup.")
		return


logWrite("********** START OF LOG **********")
logWrite("Backup process started.")

# Sets the container to use for the backup
cont = checkContainer(backupType)

# Set the SQL Backup path, and dump the backup
dbBackupFile = tmpPath + "/" + str(backupName) + ".sql"
logWrite("Creating database backup...")
os.popen("mysqldump -h " + dbHost + " --user=\"" + dbUser + "\" --password=\"" + dbPass + "\" --all-databases > " + dbBackupFile)

# Add the sql backup to the backup source
backupSrc.append(dbBackupFile)

# Set the name and path for the temporary backup archive
backupName = str(backupName) + ".tar.gz"
backupFile = tmpPath + "/" + backupName

# Create the tardump
tar = tarfile.open(backupFile, "w:gz")

logWrite("Archiving backup...")

# Loops through the backup source array, and excludes any directories matching the exclude array
for item in backupSrc:
	tar.add(item,exclude=tarExclude)
tar.close()

# Push file to backup destination
status = pushBackup(backupName,backupFile)


# Check for old backups and rotate as necessary
if status == "Ok":
	logWrite("Checking for old backups.")

	files = cont.list_objects()
	numFiles = len(files)

	if numFiles <= maxFiles[backupType]:
		logWrite("Number of backups (" + numFiles + ")has not reached threshold of " + maxFiles[backupType] + ".  Will not remove previous backups.")
	else:
		while numFiles > maxFiles[backupType]:
			files = cont.list_objects()
			filename = files[0]
			delFiles(filename,cont)
			numFiles -= 1

	# delete backup files
	logWrite("Deleting temporary backup file.")
	os.remove(backupFile)
else:
	logWrite("There was a problem pushing the backup.")
	logWrite("Backup file located at " + backupFile)
	logWrite("Please move manually.")


# Delete the DB Backup file.  Since this is added to the archive, no need to keep it if the archive
# copy fails.
logWrite("Deleting temporary database backup.")
os.remove(dbBackupFile)

logWrite("Backup process complete.")
logWrite("********** END OF LOG **********\n\n")
