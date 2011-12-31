#!/usr/bin/python

import config

# Check for backup provider, and then process the backup
def checkProviders():
	if config.bpRackspace == True:
		import backup_providers.rackspace
		Provider = backup_providers.rackspace.Rackspace(config.bpRackspaceUser, config.bpRackspaceAPI)
		processBackup(Provider, "Daily")

def processBackup(Provider, backup_type):
	import platform
	hostname = platform.node()
	Provider.checkLocation(hostname, backup_type)
	print Provider.log

if __name__ == "__main__":
    checkProviders()
