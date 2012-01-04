#!/usr/bin/python
import tarfile

class gzip:
    
    def __init__(self, include_dir, exclude_dir, backupName, tmpPath):
        self.log = "Initiating gzip backup.\n"
        self.include_dir = include_dir
        self.exclude_dir = exclude_dir
        
    def setPaths(self, backupName, tmpPath):
        self.log += "Setting backup temporary destination\n"
        # First, we set the paths for the backup file location
        self.backupName = backupName + ".tar.gz"
        self.backupFile = tmpPath + "/" + backupName
                
    def processBackup(self):
        # Python's tarfile exclusion function
        def tarExclude(filename):
            for item in self.exclude_dir:
                return filename == item    
                
        # Create the tardump
        tar = tarfile.open(self.backupFile, "w:gz")
        
        self.log += "Archiving backup...\n"
        
        # Loops through the backup source array, and excludes any directories matching the exclude array
        for item in self.include_dir:
            tar.add(item,exclude=tarExclude)
        tar.close()
        
        self.log += "Archive complete.\n"
        
        return self.log