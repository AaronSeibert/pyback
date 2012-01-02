#!/usr/bin/python

import config


def processSql():
	# First, let's make sure we're actually using the sql database source flag in config
	if config.sqlBackup == True:
	# Then process each database
		for source in config.sqlServers:
			sql = createSqlConn(source[0], source[1], source[2], source[3])
			processBackup(sql, config.tmpDir, "test.sql")

def createSqlConn(backend, db_user, db_pass, db_host):
	if backend == "mysql":
		import backup_sources.databases.mysql
		sql =  backup_sources.databases.mysql.sql(db_user, db_pass, db_host)
		return sql
	else:
		raise Exception("No valid SQL providers match the source given.")

def processBackup(sql, tmpDir, dbFileName):
	sql.obtainBackup(tmpDir, dbFileName)

if __name__ == "__main__":
    processSql()
