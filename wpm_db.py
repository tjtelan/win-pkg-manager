########################################################################
# Group: Windows Package Manager #2
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
		self.commit = True
		self.conn = sqlite3.connect(dbFileName)
		self.cursor = self.conn.cursor()
		
		# Check existance of each table and create if necessary
		tableCheck = "SELECT name FROM sqlite_master WHERE name=? AND type='table'"
		
		# Tuples with name names and strings of sql queries for table construction
		tableNames = [("Statistics",),("Application",),("RegExpr",),("Scripts",),("Dependencies",),("Files",),("OldFiles",)]

		tableConstruct = ["CREATE TABLE Statistics(ID INTEGER PRIMARY KEY, NumUpdatesNeeded INTEGER, NumSuccUpdates INTEGER, Date TEXT)",
		"CREATE TABLE Application(ID INTEGER PRIMARY KEY, ApplicationName TEXT, CurrentVersionNum TEXT, DownloadURL TEXT, MainURL TEXT, UninstallFirst BOOLEAN, NumOldVersionsToKeep INTEGER, Timestamp TEXT)",
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
				except sqlite3.Error as e:
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
	# Close database connection and save any changes made to the database, if needed
	def close(self):
		if self.commit:
			self.conn.commit()
		self.cursor.close()
		self.conn.close()
		logging.info("Database: Changes saved and connection closed")


	# change_commit
	# Parameters: commitBool is a boolean
	# Returns: None
	# Changes whether insert/update/delete commit after execution
	def change_commit(self, commitBool):
		self.commit = commitBool


	# rollback
	# Parameters: None
	# Returns: None
	# Returns to last commit and turns commit back to True
	def rollback(self):
		self.conn.rollback()
		self.cursor = self.conn.cursor()
		self.commit = True


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
			except sqlite3.Error as e:
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
	def query(self, tableName=None, appName=None, selectField=('*',), dependencyNames = False):
		
		# Table and application must be defined
		if tableName == None or (appName == None and tableName != "Application"):
			return False

		# Build sql queries
		sF_Len = len(selectField) - 1
		qField = ["SELECT ", selectField[0]]
		for ix in range(sF_Len):
			qField.append(", ")
			qField.append(selectField[ix + 1])

	
		if tableName == "Application":
			if appName != None:
				qField.append(" FROM Application WHERE ApplicationName=?")
			else:
				qField.append(" FROM Application")
		elif tableName == "Dependencies" and dependencyNames:
			qField.append (" From Application, Dependencies WHERE Application.ID == Dependencies.Dependency AND ApplicationID IN (SELECT ApplicationID FROM Application WHERE ApplicationName=?)")
		else:	
			qField.append(" FROM ")
			qField.append(tableName)
			qField.append(" WHERE ApplicationID IN (SELECT ID FROM Application WHERE ApplicationName=?)")
		qField = "".join(qField)

		# Execute sql queries
		try:
			if appName == None:
				self.cursor.execute(qField)
			else:
				self.cursor.execute(qField, (appName,))
				
			logging.info("Database Query: Application: " + str(appName) + " -- Table: " + tableName + " -- Fields: " + str(selectField))
			return True
		except sqlite3.Error as e:
			logging.exception("Database error: " + str(e.args[0]))
			raise
		except:
			logging.exception("Unexpected error: " + str(sys.exc_info()[0]))
			raise


	# insert
	# Parameters: tableName is a string
	# 						fields is a list (or tuple) of column names
	#							data is a list (or tuple) of data values in proper order w.r.t. fields
	#									if table != Application, appName goes where appID would be
	# Exception: sqlite3.Error if db error
	# Insert data into a table
	def insert(self, tableName=None, fields=None, data=None):

		# All fields must be defined
		if tableName == None or fields == None or data == None or len(fields) != len(data):
			return False

		f_len = len(fields) - 1
		d_len = f_len
		
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
				if self.commit:
					self.conn.commit()
				logging.info("Database Insert: Table: " + tableName + " -- Fields: " + str(fields) + " -- Data: " + str(data))
				return True
			except sqlite3.Error as e:
				logging.exception("Database error: " + str(e.args[0]))
				raise
			except:
				logging.exception("Unexpected error: " + str(sys.exc_info()[0]))
				raise
		
		else:
			# Find Position of ApplicationID for replacement
			for ix in range(d_len):
				if fields[ix] == "ApplicationID":
					idPos = ix
					break
			
			# Get ApplicationID and then insert data into table
			try:
				self.cursor.execute("SELECT ID FROM Application WHERE ApplicationName=?", (data[idPos],))
				appID = self.cursor.fetchone()
				qData = list(data)
				qData[idPos] = appID[0]
				self.cursor.execute(qField, qData)
				if self.commit:
					self.conn.commit()
				logging.info("Database Insert: Table: " + tableName + " -- Application: " + data[idPos] + " -- Fields: " + str(fields) + " -- Data: " + str(qData))
				return True
			except sqlite3.Error as e:
				logging.exception("Database error: " + str(e.args[0]))
				raise
			except:
				logging.exception("Unexpected error: " + str(sys.exc_info()[0]))
				raise
	
	# delete
	# Parameters: tableName is a string 
	# 						fields is a list (or tuple) of column names
	#							data is a list (or tuple) of data values in proper order w.r.t. fields
	#								if table != Application, appName goes where appID would be
	# Exception: sqlite3.Error if db error
	# Delete a row from a table
	def delete(self, tableName=None, fields=None, data=None):

		# All fields must be defined
		if tableName == None or fields == None or data == None or len(fields) != len(data):
			return False

		f_len = len(fields)
		d_len = f_len
		
		# Build query
		qField = ["DELETE FROM ", tableName, " WHERE ", fields[0], "=?"]
		for ix in range(1,f_len):
			qField.append(" and ")
			qField.append(fields[ix])
			qField.append("=?")
		qField = "".join(qField)

		# Execute the query
		if tableName == 'Application':
			try:
				self.cursor.execute(qField, data)
				if self.commit:
					self.conn.commit()
				logging.info("Database Delete: Table: " + tableName + " -- Fields: " + str(fields) + " -- Data: " + str(data))
				return True
			except sqlite3.Error as e:
				logging.exception("Database error: " + str(e.args[0]))
				raise
			except:
				logging.exception("Unexpected error: " + str(sys.exc_info()[0]))
				raise
		
		else:
			# Find Position of ApplicationID for replacement
			for ix in range(d_len):
				if fields[ix] == "ApplicationID":
					idPos = ix
					break
			
			# Get ApplicationID and then delete data from table
			try:
				self.cursor.execute("SELECT ID FROM Application WHERE ApplicationName=?", (data[idPos],))
				appID = self.cursor.fetchone()
				qData = list(data)
				qData[idPos] = appID[0]
				self.cursor.execute(qField, qData)
				if self.commit:
					self.conn.commit()
				logging.info("Database Delete: Table: " + tableName + " -- Application: " + data[idPos] + " -- Fields: " + str(fields) + " -- Data: " + str(data))
				return True
			except sqlite3.Error as e:
				logging.exception("Database error: " + str(e.args[0]))
				raise
			except:
				logging.exception("Unexpected error: " + str(sys.exc_info()[0]))
				raise

	# update
	# Parameters: tableName is a string 
	# 						setFields and colFields are lists (or tuples) of column names
	#							setToFields and colRestrict are lists (or tuples) of data values in proper order w.r.t. fields
	#								if table != Application, appName goes where appID would be
	# Exception: sqlite3.Error if db error
	# Delete a row from a table
	def update(self, tableName=None, setFields=None, setToFields=None, colFields=None, colRestrict=None):

		# No field may be empty
		if tableName == None or setFields == None or setToFields == None or colFields == None or colRestrict == None:
			return False

		# Fields need to be of equal length
		if len(setFields) != len(setToFields) or len(colFields) != len(colRestrict) or len(setFields) == 0 or len(colFields) == 0:
			return False

		s_len = len(setFields)
		c_len = len(colRestrict)

		qField = ["UPDATE ", tableName, " SET ", setFields[0], "=?"]
		for ix in range(1,s_len):
			qField.append(",")
			qField.append(setFields[ix])
			qField.append("=?")
		qField.append(" WHERE ")
		qField.append(colFields[0])
		qField.append("=?")
		for ix in range(1,c_len):
			qField.append(" and ")
			qField.append(colFields[ix])
			qField.append("=?")
		qField = "".join(qField)

		# Execute the query
		if tableName == 'Application':
			try:
				qData = list(setToFields) + list(colRestrict)
				self.cursor.execute(qField, qData)
				if self.commit:
					self.conn.commit()
				logging.info("Database Update: Table: " + tableName + " -- Column Fields: " + str(colFields) + " -- Restrictions: " + str(colRestrict) + " -- Set Fields: " + str(setFields) + " -- Set To: " + str(setToFields))
				return True
			except sqlite3.Error as e:
				logging.exception("Database error: " + str(e.args[0]))
				raise
			except:
				logging.exception("Unexpected error: " + str(sys.exc_info()[0]))
				raise
		
		else:
			# Find Position of ApplicationID for replacement
			for ix in range(c_len):
				if colFields[ix] == "ApplicationID":
					idPos = ix
					break
			
			# Get ApplicationID and then delete data from table
			try:
				self.cursor.execute("SELECT ID FROM Application WHERE ApplicationName=?", (colRestrict[idPos],))
				appID = self.cursor.fetchone()
				qData = list(colRestrict)
				qData[idPos] = appID[0]
				qData = list(setToFields) + qData
				self.cursor.execute(qField, qData)
				if self.commit:
					self.conn.commit()
				logging.info("Database Update: Table: " + tableName + " -- Application: " + colRestrict[idPos]  + " -- Column Fields: " + str(colFields) + " -- Restrictions: " + str(colRestrict) + " -- Set Fields: " + str(setFields) + " -- Set To: " + str(setToFields))
				return True
			except sqlite3.Error as e:
				logging.exception("Database error: " + str(e.args[0]))
				raise
			except:
				logging.exception("Unexpected error: " + str(sys.exc_info()[0]))
				raise
