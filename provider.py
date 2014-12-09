#!/usr/bin/python

<<<<<<< HEAD
import config
       
=======
import  config
>>>>>>> 5b29aac12466425617c53ee7ce11f67e132c3a6c
import traceback

# Check for backup provider, and then process the backup
def processProviders(backup_type, backup_name, backup_path):
	log = "Processing backup destination providers\n"
	if config.bpRackspace == True:
		import backup_providers.rackspace
		Provider = backup_providers.rackspace.Rackspace(config.bpRackspaceUser, config.bpRackspaceAPI)
		status = processBackup(Provider, backup_type, backup_name, backup_path, log)
	elif config.bpAmazonS3 == True:
		import backup_providers.amazons3
		Provider = backup_providers.amazons3.AmazonS3(config.bpAWSKeyID, config.bpAWSKey)
		status = processBackup(Provider, backup_type, backup_name, backup_path, log)
	else:
		# If there are no valid backup destinations, raise exception
		raise Exception("No valid backup destination providers.")
	return status

def processBackup(Provider, backup_type, backup_name, backup_path, log):
	import platform
	hostname = platform.node()
        hostname = hostname.replace('.','_')
	try:
		
		# First we check to make sure the remote location exists.
		Provider.checkLocation(hostname, backup_type)
		
		# Then push the backup to the remote location
		Provider.pushBackup(backup_name, backup_path)
		
		# Then rotate
		Provider.rotateBackup(config.maxFiles[backup_type])
		
		# Obtain the provider log file
		log = Provider.log
		
		return {
			'log':log,
			'status':True
		}
<<<<<<< HEAD
	except Exception, e:
	        print e
		return {
			'log': e,
=======
	except:
		return {
			'log':log,
>>>>>>> 5b29aac12466425617c53ee7ce11f67e132c3a6c
			'status':False
			}

if __name__ == "__main__":
    processProviders("Weekly", "temp.tgz", "")
