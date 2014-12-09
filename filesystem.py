#!/usr/bin/python

import config

def processFS(sqlBackup, sqlStatus, backupName, tmpPath):
    log = "Processing filesystem backup sources.\n"
    # First, check to see if the fs flag is on in the config
    if config.fsBackup == True:
        
        # If we have a sql backup, be sure to append it to the backup source
        if sqlStatus == True:
                include_dir = config.fsBackupSrc
                include_dir.append(sqlBackup)
        else:
            include_dir = config.fsBackupSrc
                
        # Check to see which method we're using for the filesystem backup
        if config.fsType == "gzip":
            backupName += ".tar.gz"
            import backup_sources.filesystem.gzip
            fs = backup_sources.filesystem.gzip.gzip(include_dir, config.fsBackupExclude, backupName, tmpPath)
            log += processBackup(fs, backupName, tmpPath)

    else:
        log += "No filesystem backup sources defined.\n"
    
    return {
        'log':log,
        'file':backupName
    }

def processBackup(fs, backupName, tmpPath):
    fs.setPaths(backupName, tmpPath)
    return fs.processBackup()