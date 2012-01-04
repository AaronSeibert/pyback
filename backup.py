#!/usr/bin/python
import sys
import os
import tarfile
import config

from datetime import date, datetime
from provider import processProviders as provider
from sql import processSql as sql

backupName = str(date.today());
sqlTmpDir = config.tmpDir + "/sql"

# Set the backup type
backupType = sys.argv[1]

def main():
	
	# Create the tmp backup directories
	checkDir(config.tmpDir)
	checkDir(sqlTmpDir)
	
	
	# Start off our log
	logWrite("********** START OF LOG **********")
	logWrite("Backup process started.")
	
	# Set the SQL Backup path, and dump the backup
	logWrite("Creating database backup...")
	sqlStatus = sql(sqlTmpDir, backupName)
	logWrite(sqlStatus)
	
	# Push file to backup destination
	logWrite("Pushing backup to configured provider(s)...")
	pushStatus = provider(backupType, "temp.tgz", "")
	logWrite(pushStatus)

	# Delete the DB Backup file.  Since this is added to the archive, no need to keep it if the archive
	# copy fails.
	logWrite("Deleting temporary backup files.")
	os.remove(config.tmpDir)
	
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

"""

# Python's tarfile exclusion function
def tarExclude(filename):
	for item in backupExclude:
		return filename == item

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
"""

if __name__ == "__main__":
	main()
