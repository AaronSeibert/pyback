#!/usr/bin/python

import config

# Check for backup provider, and then process the backup
def checkProviders():
	if config.bpRackspace == True:
		import backup_providers.rackspace
		Provider = backup_providers.rackspace.Rackspace(config.bpRackspaceUser, config.bpRackspaceAPI)
		processBackup(Provider)

def processBackup(Provider):
	import platform
	hostname = platform.node()
	Provider.checkLocation(hostname)
	print Provider.log

if __name__ == "__main__":
    checkProviders()
