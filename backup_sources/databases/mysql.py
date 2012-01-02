#!/usr/bin/python

import os

class sql:
	def __init__(self, db_user, db_pass, db_host):
		self.db_user = db_user
		self.db_pass = db_pass
		self.db_host = db_host

	def obtainBackup(self, tmp_path, file_name):
		dbBackupFile = tmp_path + "/" + file_name + ".sql"
		os.popen("mysqldump -h " + self.db_host + " --user=\"" + self.db_user + "\" --password=\"" + self.db_pass + "\" --all-databases > " + dbBackupFile)
