########################################################################
# Group: Windows Package Manager #2
# Name: Joshua Stein
# Group Members: Sebastian Imlay and Timothy James Telan
# Date: October 3, 2011
# Wrapper for database queries. Abstracts database.
########################################################################

import wpm_db
import itertools

# add_app
# Parameters: db is a database class object
#							All other parameters are strings except unistallFirst(bool) 
#								and numOldVersionsToKeep (int)
# Return: True if successful, false otherwise
def add_app(db, appName, version, dlURL, mainURL, uninstallFirst = False, numOldVersionsToKeep = 3):
	fields = ['ApplicationName', 'CurrentVersionNum', 'DownloadURL', 'MainURL', 'UninstallFirst', 'NumOldVersionsToKeep']
	data = [appName, version, dlURL, mainURL, uninstallFirst, numOldVersionsToKeep]
	try:
		# Only insert if application unique
		db.query('Application', appName)
		if db.retrieve(1) != []:
			print("An application already exists with that name.")
			return False

		# Insert Data (Unique application)
		db.insert('Application', fields, data)
		return True
	except:
		print("An error occurred when insterting the application's data.")
		return False

# add_regex
# Parameters: db is a database class object
#							appName is a string 
#							regex is a list of strings
# Return: True if successful, false otherwise
def add_regex(db, appName, regex):
	fields = ['ApplicationID', 'Expression']
	try:
		for re in regex:
			db.insert('RegExpr', fields, (appName, re))
		return True
	except:
		print("An error occurred when insterting the application's regular expression data.")
		return False

# add_scripts
# Parameters: db is a database class object
#							appName is a string
#							scriptName is a list of strings
# Return: True if successful, false otherwise
def add_scripts(db, appName, scriptNames):
	fields = ['ApplicationID', 'Script']
	try:
		for script in scriptNames:
			db.insert('Scripts', fields, (appName, script))
		return True
	except:
		print("An error occurred when insterting the application's script data.")
		return False

# add_file
# Parameters: db is a database class object
#							All other parameters are strings
# Return: True if successful, false otherwise
def add_file(db, appName, currEXEFileName, localEXELocation, EXEType):
	fields = ['ApplicationID', 'CurrEXEFileName', 'LocalEXELocation', 'EXEType']
	data = [appName, currEXEFileName, localEXELocation, EXEType]
	try:
		db.insert('Files', fields, data)
		return True
	except:
		print("An error occurred when insterting the application's file data.")
		return False

# add_dependencies(db, appName, dependList)
# Parameters: db is a database class object
#							appName is a string
#							dependList is a list of strings
#	Return: True if successful, false otherwise
def add_dependencies(db, appName, dependList):
	fields = ['ApplicationID', 'Dependency']
	try:
		for dApp in dependList:
			if not db.query("Application", dApp, ("ID",)):
				return False
			result = db.retrieve(1)
			if result == []:
				return False
			if db.insert("Dependencies", fields, (appName, result[0][0])):
				return True
			else:
				False
	except:
		print("An error occurred when inserting dependencies into the database.")
		return False

# get_applications
# Parameters: db is a database class object
# Return: Tuple of the form (Bool, List), 
#					bool is true if successful, false otherwise
def get_applications(db):
	try:
		if db.query("Application", None, ("ApplicationName",)):
			l = db.retrieve()
			return (True, list(itertools.chain.from_iterable(l)))
		else:
			return (False, [])
	except:
		print("An error occurred when retrieving application names from database.")
		return (False, [])

# get_app_version
# Parameters: db is a database class object
#							appName is a string
# Return: Tuple of the form (Bool, List),
#					bool is true if successful, false otherwise
def get_app_version(db, appName):
	try:
		if db.query("Application", appName, ("CurrentVersionNum",)):
			l = db.retrieve()
			return (True, list(itertools.chain.from_iterable(l)))
		else:
			return (False, [])
	except:
		print("An error occurred when retrieving application names from database.")
		return (False, [])


# get_app_urls
# Parameters: db is a database class object
#							appName is a string
# Return: Tuple of the form (Bool, List), list contains mainURL and dlURL
#					bool is true if successful, false otherwise
def get_app_urls(db, appName):
	try:
		if db.query("Application", appName, ("MainURL","DownloadURL")):
			l = db.retrieve()
			return (True, list(itertools.chain.from_iterable(l)))
		else:
			return (False, [])
	except:
		print("An error occurred when retrieving application names from database.")
		return (False, [])

# get_app_regex
# Parameters: db is a database class object
#							appName is a string
# Return: Tuple of the form (Bool, List), list contains strings
#					bool is true if successful, false otherwise
def get_app_regex(db, appName):
	try:
		if db.query("RegExpr", appName, ("Expression",)):
			l = db.retrieve()
			return (True, list(itertools.chain.from_iterable(l)))
		else:
			return (False, [])
	except:
		print("An error occurred when retrieving application names from database.")
		return (False, [])

# get_dependencies
# Parameters: db is a database class object
#							appName is a string
# Return: Tuple of the form (Bool, List)
#					bool is true if successful, false otherwise
def get_app_dependencies(db, appName):
	try:
		if not db.query("Dependencies", appName, ("ApplicationName",), True):
			return (False, [])
		l = db.retrieve()
		return (True, list(itertools.chain.from_iterable(l)))
	except:
		print("An error occurred when retrieving application dependencies from the database.")
		return (False, [])
