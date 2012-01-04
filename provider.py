#!/usr/bin/python

import config

# Check for backup provider, and then process the backup
def processProviders(backup_type, backup_name, backup_path):
	log = "Processing backup destination providers\n"
	if config.bpRackspace == True:
		import backup_providers.rackspace
		Provider = backup_providers.rackspace.Rackspace(config.bpRackspaceUser, config.bpRackspaceAPI)
		log += processBackup(Provider, backup_type, backup_name, backup_path)
	else:
		# If there are no valid backup destinations, raise exception
		raise Exception("No valid backup destination providers.")
	return log

def processBackup(Provider, backup_type, backup_name, backup_path):
	import platform
	hostname = platform.node()
	Provider.checkLocation(hostname, backup_type)
	Provider.pushBackup(backup_name, backup_path)
	Provider.rotateBackup(config.maxFiles[backup_type])
	return Provider.log

if __name__ == "__main__":
    processProviders("Weekly", "temp.tgz", "")
