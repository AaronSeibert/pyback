#!/usr/bin/python
import sys
import time
import tarfile
import os
import config

from datetime import date, datetime

backupName = date.today();

# Set the backup type
backupType = sys.argv[1]

def currentTime():
	time = datetime.now()
	return str(time)

def logWrite(string):
	log = open(logFile,"aw")
	log.write(currentTime() + ": " + string + "\n")
	log.close()
	return	

# Python's tarfile exclusion function
def tarExclude(filename):
	for item in backupExclude:
		return filename == item

logWrite("********** START OF LOG **********")
logWrite("Backup process started.")

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
	# delete backup files
	logWrite("Deleting temporary backup file.")
	os.remove(backupFile)

# Delete the DB Backup file.  Since this is added to the archive, no need to keep it if the archive
# copy fails.
logWrite("Deleting temporary database backup.")
os.remove(dbBackupFile)

logWrite("Backup process complete.")
logWrite("********** END OF LOG **********\n\n")
