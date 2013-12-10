#!/usr/bin/python
import sys
import os
import config #for development.  Production should just use config
import shutil
import argparse

from datetime import date, datetime
from provider import processProviders as provider
from sql import processSql as sql
from filesystem import processFS as fs

backupName = str(date.today());
sqlTmpDir = config.tmpDir + "/sql"

# argument parser

parser = argparse.ArgumentParser(description='Create rotating backups')
parser.add_argument('backupType', metavar='TYPE', type=str,
                   help='The type of backup to perform - Daily, Weekly, or Monthly')
parser.add_argument('-c', '--client', 
				   help='Optional.  Name of the client to process an individual backup for.')
parser.add_argument('-p', '--path', 
				   help='Optional.  Filesystem path for a single folder backup')
# parser.add_argument('-d', '--database', help='Optional.  Database name for a single database backup')



args = parser.parse_args()

# Set the backup type
backupType = args.backupType

email = ""

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
		try:
			shutil.rmtree(sqlTmpDir)
		except:
			logWrite("No tmp sql dir to remove")
		logWrite("There was an issue pushing the local backup.\n  Backup is located in " + config.tmpDir)

	logWrite("Backup process complete.")
	logWrite("********** END OF LOG **********\n\n")
	sendEmail(backupType)
	
def currentTime():
	time = datetime.now()
	return str(time)

def logWrite(string):
	global email
	log = open(config.logFile,"aw")
	log.write(currentTime() + ": " + string + "\n")
	email += currentTime() + ":" + string + "\n"
	log.close()
	return	

def sendEmail(backupType):
	import smtplib
	import string
	import platform
	
	FROM = config.fromEmail
	TO = config.toEmail
	SUBJECT = "Backup Complete: " + platform.node() + " " + backupType
	BODY= string.join((
					"From: %s" % FROM,
					"To: %s" % TO,
					"Subject: %s" %SUBJECT,
					"",
					email
					), "\r\n")

	s = smtplib.SMTP('localhost')
	s.sendmail(FROM, TO, BODY)
	s.quit()

def checkDir(d):
	if not os.path.exists(d):
		os.makedirs(d)

if __name__ == "__main__":
	main()
