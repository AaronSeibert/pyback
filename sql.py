#!/usr/bin/python

import config


def processSql(filename):
	# First, let's make sure we're actually using the sql database source flag in config
	if config.sqlBackup == True:
	# Then process each database
		for source in config.sqlServers:
			sql = createSqlConn(source[0], source[1], source[2], source[3])
			dbFileName = config.tmpDir + "/" + source[0] + "_" + filename + ".sql"
			processBackup(sql, dbFileName)

def createSqlConn(backend, db_user, db_pass, db_host):
	if backend == "mysql":
		import backup_sources.databases.mysql
		sql =  backup_sources.databases.mysql.sql(db_user, db_pass, db_host)
		return sql
	else:
		raise Exception("No valid SQL providers match the source given.")

def processBackup(sql, dbFileName):
	sql.obtainBackup(dbFileName)

def buildBackupPath(dbFileName):
	return config.tmpDir + "/" + dbFileName

if __name__ == "__main__":
    processSql("temp")
