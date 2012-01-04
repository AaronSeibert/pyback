#!/usr/bin/python
import sys
import os
import config
import shutil

from datetime import date, datetime
from provider import processProviders as provider
from sql import processSql as sql
from filesystem import processFS as fs

backupName = str(date.today());
sqlTmpDir = config.tmpDir + "/sql"

# Set the backup type
backupType = sys.argv[1]

def main():
	
	# Create the tmp backup directories
	checkDir(config.tmpDir)
	
	# Start off our log
	logWrite("********** START OF LOG **********")
	logWrite("Backup process started.")
	
	# Set the SQL Backup path, and dump the backup
	logWrite("Creating database backup...")
	sqlStatus = sql(sqlTmpDir, backupName)
	logWrite(sqlStatus['log'])
	
	# Process the filesystem backups
	logWrite("Creating filesystem backup...")
	fsStatus = fs(sqlTmpDir, sqlStatus['enabled'], backupName, config.tmpDir)
	logWrite(fsStatus['log'])
	
	# Push file to backup destination
	logWrite("Pushing backup to configured provider(s)...")
	pushStatus = provider(backupType, fsStatus['file'], config.tmpDir)
	logWrite(pushStatus['log'])
	
	# If the backup push was successful, delete the tmp backup folder.
	if pushStatus['status'] == True:
		# Delete the DB Backup file.  Since this is added to the archive, no need to keep it if the archive
		# copy fails.
		logWrite("Deleting temporary backup files.")
		shutil.rmtree(config.tmpDir)
	else:
		# remove the sql backup directory, since it's already in the archive, and add the failure to the log
		shutil.rmtree(sqlTmpDir)
		logWrite("There was an issue pushing the local backup.\n  Backup is located in " + config.tmpDir)
	
	logWrite("Backup process complete.")
	logWrite("********** END OF LOG **********\n\n")
	
def currentTime():
	time = datetime.now()
	return str(time)

def logWrite(string):
	log = open(config.logFile,"aw")
	log.write(currentTime() + ": " + string + "\n")
	log.close()
	return	

def checkDir(d):
	if not os.path.exists(d):
		os.makedirs(d)

if __name__ == "__main__":
	main()
