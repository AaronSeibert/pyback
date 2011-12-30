#!/usr/bin/python

#Set the log file directory
logFile = "/var/log/backup"

# Set the number of backup files to keep for each backup type as an associative array
maxFiles = {
	'Daily':7,
	'Weekly':4,
	'Monthly':6
	}

#########################################################################################
#
# The following sections allow you to configure the individual backup sources
# Currently we have filesystem backups and MySQL backups
#
#########################################################################################

# fsBackup - choose to enable (True) or disable (False) the filesystem backup
# fsBackupTmpPath - path to temporary storage of the backups
# fsBackupSrc - array of directories to back up
# fsBackupExclude = array of directories to exclude from backup
fsBackup = True
fsBackupTmpPath = "/tmp"
fsBackupSrc = [
	"/home",
	"/etc"
	]
fsBackupExclude = [
	"/etc/dropbox"
	]

# dbMysql - choose to enable (True) or disable (False) the MySQL backup
# dbMysqlUser - the MySQL user account that has access to the databases you wish to backup
# dbMysqlPass - dbMysqlUser's password
# dbMysqlHost - host of the MySQL server.
dbMysql = True
dbMysqlUser = ""
dbMysqlPass = ""
dbMysqlHost = ""

#########################################################################################
#
# The following sections allow you to configure the individual ackup destinations
# Currently we have Rackspace CloadFiles
#
#########################################################################################

# Configure the Rackspace backup destination
bpRackspace = True
bpRackspaceUser = ""
bpRackspaceAPI = ""
