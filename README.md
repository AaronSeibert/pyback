# PyBack - A Python backup tool

This backup script, at the moment, only backs up to Rackspace Cloud.


## Usage
First, modify config.py to match your environment and backup demands.
Then, check the Documentation folder for requirements pertaining to each of the providers you choose to use (ie, rackspace.txt, mysql.txt, etc.)

Then, simply call backup.py with the type of backup to perform:

```bash
backup.py Daily
backup.py Weekly
backup.py Monthly
```

## Adding backup providers
New backup destination providers can be added by creating an appropriately named class in the "backup_providers" folder.  Classes *must* contain the following methods, other than the standard __init__:

checkLocation - this method should first check to ensure the target location exists, and create it if it doesn't.  It should accept an argument of the base backup directory - it should then check to ensure that directory exists, and then subsequently check for each of the Daily/Weekly/Monthly folders, and create any directories that do not exist.

A <provider>.txt file should also be created in the Documentation folder, that outlines requirements for that provider
