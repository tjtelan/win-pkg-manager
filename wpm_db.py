########################################################################
#	Group: Windows Package Manager #2
# Name: Joshua Stein
# Group Members: Sebastian Imlay and Timothy James Telan
# Date: October 3, 2011
# Class that takes care of all database queries
########################################################################


import sqlite3, logging, sys

class db:
	# __init__
	# Parameters: dbFileName and logFileName are strings
	# Exception: sqlite3.Error if db error
	# Sets up all the tables for Windows Package Manager
	def __init__(self, dbFileName, logFileName):
		# Initialize Logger
		logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%a, %d %b %Y %H:%M:%S', filename=logFileName, filemode='a')

		# Connect/Create Database
		self.conn = sqlite3.connect(dbFileName)
		self.cursor = self.conn.cursor()
		
		# Check existance of each table and create if necessary
		tableCheck = "SELECT name FROM sqlite_master WHERE name=? AND type='table'"
		
		# Tuples with name names and strings of sql queries for table construction
		tableNames = [("Statistics",),("Application",),("RegExpr",),("Scripts",),("Dependencies",),("Files",),("OldFiles",)]

		tableConstruct = ["CREATE TABLE Statistics(ID INTEGER PRIMARY KEY, NumUpdatesNeeded INTEGER, NumSuccUpdates INTEGER, Date TEXT)",
		"CREATE TABLE Application(ID INTEGER PRIMARY KEY, ApplicationName TEXT, CurrentVersionNum TEXT, DownloadURL TEXT, MainURL TEXT, Uninstall BOOLEAN, NumOldVersionsToKeep INTEGER)",
		"CREATE TABLE RegExpr(ApplicationID INTEGER REFERENCES Application(ID), Expression TEXT)",
		"CREATE TABLE Scripts(ID INTEGER PRIMARY KEY, ApplicationID INTEGER REFERENCES Application(ID), Script TEXT)",
		"CREATE TABLE Dependencies(ID INTEGER PRIMARY KEY, ApplicationID INTEGER REFERENCES Application(ID), Dependency INTEGER REFERENCES Application(ID))",
		"CREATE TABLE Files(ID INTEGER PRIMARY KEY, ApplicationID INTEGER REFERENCES Application(ID), CurrEXEFileName TEXT, LocalEXELocation TEXT, EXEType TEXT)",
		"CREATE TABLE OldFiles(ID INTEGER PRIMARY KEY, ApplicationID INTEGER REFERENCES Application(ID), OldEXEFileName TEXT, OldVersionNum TEXT, OldCount INTEGER)"]

		# Add every table defined above to the database
		numTables = len(tableNames)
		for ix in range(numTables):
			self.cursor.execute(tableCheck, tableNames[ix])
			if self.cursor.fetchone() == None:
				try:
					self.cursor.execute(tableConstruct[ix])
				except sqlite3.Error, e:
					logging.exception("Database error: " + str(e.args[0]))
					raise
				except:
					logging.exception("Unexpected error: " + str(sys.exc_info()[0]))
					raise
				self.conn.commit()
				logging.info("Table Created: " + tableNames[ix][0])


	# __del__
	# Parameters: None
	# Close database connection and save any changes made to the database
	def __del__(self):
		self.close()


	# close
	# Parameters: None
	# Close database connection and save any changes made to the database
	def close(self):
		self.conn.commit()
		self.cursor.close()
		self.conn.close()
		logging.info("Database: Changes saved and connection closed")


	# retrieve
	# Parameters: num is an integer, none indicates fetchall
	# Returns: A list of query results
	# Exception: TypeError if num is not an integer, sqlite3.Error if db error
	# Retrieves data from from the database after a query
	def retrieve(self, num=None):
		if num == None:
			data = self.cursor.fetchall()
			logging.info("Database: Fetched all data from query")
			return data
		else:
			try:
				data = self.cursor.fetchmany(num)
				logging.info("Database: Fetched " + str(num) + " entries from query")
				return data
			except sqlite3.Error, e:
					logging.exception("Database error: " + str(e.args[0]))
					raise
			except TypeError:
				logging.exception("db Class: TypeError in retrieve")
				return None


	# query
	# Parameters: tableName and appName are strings
	#							selectField is a list (or tuple) of table column names
	# Returns: True on success, exception otherwise
	# Exception: sqlite3.Error if db error
	# Performs a database query
	def query(self, tableName=None, appName=None, selectField=('*',)):
		
		# Table and application must be defined
		if tableName == None or appName == None:
			return False

		# Build sql queries
		sF_Len = len(selectField) - 1
		qField = ["SELECT ", selectField[0]]
		for ix in range(sF_Len):
			qField.append(", ")
			qField.append(selectField[ix + 1])


		if tableName == "Application":
			qField.append(" FROM Application WHERE ApplicationName=?")
		else:	
			qField.append(" FROM ")
			qField.append(tableName)
			qField.append(" WHERE ApplicationID IN (SELECT ApplicationID FROM Application WHERE ApplicationName=?)")
		qField = "".join(qField)

		# Execute sql queries
		try:
			self.cursor.execute(qField, (appName,))
			logging.info("Database Query: Application: " + appName + " -- Table: " + tableName + " -- Fields: " + str(selectField))
			return True
		except sqlite3.Error, e:
			logging.exception("Database error: " + str(e.args[0]))
			raise
		except:
			logging.exception("Unexpected error: " + str(sys.exc_info()[0]))
			raise


	# insert
	# Parameters: tableName and appName are strings
	# 						fields is a list (or tuple) of column names
	#							data is a list (or tupe) of data values in proper order w.r.t. fields
	# Exception: sqlite3.Error if db error
	# Insert data into a table
	def insert(self, tableName=None, fields=None, data=None, appName=None):

		# All fields must be defined
		if tableName == None or (tableName != "Application" and appName == None) or fields == None or data == None:
			return False

		f_len = len(fields) - 1
		d_len = len(data) - 1
		
		# Build query
		qField = ["INSERT INTO ", tableName, "(", fields[0]]
		for ix in range(f_len):
			qField.append(", ")
			qField.append(fields[ix + 1])
		qField.append(") VALUES(?")
		for ix in range(d_len):
			qField.append(", ?")
		qField.append(")")
		qField = "".join(qField)

		# Execute the query
		if tableName == 'Application':
			try:
				self.cursor.execute(qField, data)
				self.conn.commit()
				logging.info("Database Insert: Table: " + tableName + " -- Fields: " + str(fields) + " -- Data: " + str(data))
				return True
			except sqlite3.Error, e:
				logging.exception("Database error: " + str(e.args[0]))
				raise
			except:
				logging.exception("Unexpected error: " + str(sys.exc_info()[0]))
				raise
		
		else:
			# Find Position of ApplicationID for replacement
			for ix in range(d_len):
				if data[ix] == "ApplicationID":
					idPos = ix
					break
			
			# Get ApplicationID and then insert data into table
			try:
				self.cursor.execute("SELECT ApplicationID FROM Application WHERE ApplicationName=?", appName)
				appID = self.cursor.fetchone()
				qData = (tableName,) + fields + data[:ix-1] + appID + data[ix+1:]
				self.cursor.execute(qField, qData)
				self.conn.commit()
				logging.info("Database Insert: Table: " + tableName + " -- Application: " + appName + " -- Fields: " + fields + " -- Data: " + data)
				return True
			except sqlite3.Error, e:
				logging.exception("Database error: " + str(e.args[0]))
				raise
			except:
				logging.exception("Unexpected error: " + str(sys.exc_info()[0]))
				raise
