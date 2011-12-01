########################################################################
# Group: Windows Package Manager #2
# Name: Joshua Stein
# Group Members: Sebastian Imlay and Timothy James Telan
# Date: October 3, 2011
# Wrapper for database queries. Abstracts database.
########################################################################

import wpm_db
import itertools
import time

#######################################################################
# Add Functions
#######################################################################

# add_app
# Parameters: db is a database class object
#							All other parameters are strings except unistallFirst(bool) 
#								and numOldVersionsToKeep (int)
# Return: List of bools, first indicates successful db operation, all others
#           represent if item was able to be inserted (unique)
def add_app(db, appName, version, dlURL, mainURL, uninstallFirst = False, numOldVersionsToKeep = 3):
	fields = ['ApplicationName', 'CurrentVersionNum', 'DownloadURL', 'MainURL', 'UninstallFirst', 'NumOldVersionsToKeep', "Timestamp"]
	data = [appName, version, dlURL, mainURL, uninstallFirst, numOldVersionsToKeep, str(time.time())]
	try:
		# Only insert if application unique
		db.query('Application', appName)
		if db.retrieve(1) != []:
			return [True, False]
		# Insert Data (Unique application)
		insertion = db.insert('Application', fields, data)
		return [True, insertion]
	except:
		print("An error occurred when inserting the application's data.")
		return [False, False]


# add_exe_regex
# Parameters: db is a database class object
#							appName is a string 
#							regex is a list of strings
# Return: List of bools, first indicates successful db operation, all others
#           represent if item was able to be inserted (unique)
def add_exe_regex(db, appName, regex):
	fields = ['ApplicationID', 'Expression']
	insertions = []
	cont, currAppRegex = get_app_exe_regex(db, appName)
	if (not cont):
		return [False]
	try:
		for re in regex:
			if re in currAppRegex:
				insertions.append(False)
			else:			
				insertions.append(db.insert('RegExprExe', fields, (appName, re)))
				currAppRegex.append(re)
		insertions.insert(0, True)
		return insertions
	except:
		print("An error occurred when inserting the application's regular expression data for exes.")
		insertions.insert(0, False)
		return insertions


# add_version_regex
# Parameters: db is a database class object
#							appName is a string 
#							regex is a list of strings
# Return: List of bools, first indicates successful db operation, all others
#           represent if item was able to be inserted (unique)
def add_version_regex(db, appName, regex):
	fields = ['ApplicationID', 'Expression']
	insertions = []
	cont, currAppRegex = get_app_version_regex(db, appName)
	if (not cont):
		return [False]
	try:
		for re in regex:
			if re in currAppRegex:
				insertions.append(False)
			else:			
				insertions.append(db.insert('RegExprVersion', fields, (appName, re)))
				currAppRegex.append(re)
		insertions.insert(0, True)
		return insertions
	except:
		print("An error occurred when inserting the application's regular expression data for exes.")
		insertions.insert(0, False)
		return insertions


# add_scripts
# Parameters: db is a database class object
#							appName is a string
#							scriptName is a list of strings
# Return: List of bools, first indicates successful db operation, all others
#           represent if item was able to be inserted (unique)
def add_scripts(db, appName, scriptNames):
	fields = ['ApplicationID', 'Script']
	insertions = []
	cont, currAppScripts = get_app_scripts(db, appName)
	if (not cont):
		return [False]
	try:
		for script in scriptNames:
			if script in currAppScripts:
				insertions.append(False)
			else:
				insertions.append(db.insert('Scripts', fields, (appName, script)))
				currAppScripts.append(script)
		insertions.insert(0, True)
		return insertions
	except:
		print("An error occurred when inserting the application's script data.")
		insertions.insert(0, False)
		return insertions


# add_dependencies(db, appName, dependList)
# Parameters: db is a database class object
#							appName is a string
#							dependList is a list of strings
# Return: List of bools, first indicates successful db operation, all others
#           represent if item was able to be inserted (unique)
def add_dependencies(db, appName, dependList):
	fields = ['ApplicationID', 'Dependency']
	insertions = []	
	cont, currAppDependencies = get_app_dependencies(db, appName)
	if (not cont):
		return [False]
	try:
		for dApp in dependList:
      # Determine if dependency application exists
			if not db.query("Application", dApp, ("ID",)):
				insertions.append(False)
				continue
			result = db.retrieve(1)
			if result == []:
				insertions.append(False)
				continue

      # Determine if dependency application is already listed as a dependency
			if dApp in currAppDependencies:			
				insertions.append(False)
				continue

			insertions.append(db.insert("Dependencies", fields, (appName, result[0][0])))
			currAppDependencies.append(dApp)
		insertions.insert(0, True)
		return insertions
	except:
		print("An error occurred when inserting dependencies into the database.")
		insertions.insert(0, False)
		return insertions


# add_update_file
# Parameters: db is a database class object
#							All other parameters are strings
# Functionality: If only versionNum is given, updates version number of application
#								 If every variable is defined, performs a full add/update
#	Standard Usage: All fields defined. May cause inconsistency between current file and version otherwise
# Return: True if successful, false otherwise
def add_update_file(db, appName, versionNum, currEXEFileName = None, localEXELocation = None, EXEType = None):
	try:
		if currEXEFileName == None or localEXELocation == None or EXEType == None:
			return db.update("Application", ("CurrentVersionNum",), (versionNum,), ("ApplicationName",), (appName,))
	
		# Suspend commits - Prevent inconsistent states from multiple sql statements
		db.change_commit(False)
		if not db.query("Application", appName, ("CurrentVersionNum", "NumOldVersionsToKeep")):
			db.rollback()
			return False
		appList = db.retrieve(1)

		if not db.update("Application", ("CurrentVersionNum","Timestamp"), (versionNum, str(time.time())), ("ApplicationName",), (appName,)):
			db.rollback()
			return False

		# Add new file if application has none yet
		if not db.query("Files", appName, ("CurrEXEFileName",)):
			db.rollback()
			return False	
		currFile = db.retrieve(1)
		
		fields = ['ApplicationID', 'CurrEXEFileName', 'LocalEXELocation', 'EXEType']
		data = [appName, currEXEFileName, localEXELocation, EXEType]
		if currFile == []:
			if not db.insert('Files', fields, data):
				db.rollback()
				return False
		else:
			if not db.delete('Files', ('ApplicationID',),(appName,)):
				db.rollback()
				return False
			if not db.update('OldFiles', ('OldCount',), ('OldCount + 1',), ('ApplicationID',), (appName,)):
				db.rollback()
				return False
			if not db.insert('OldFiles', ('ApplicationID', 'OldVersionNum', 'OldEXEFileName','OldCount'), \
											 (appName, appList[0][0] ,currFile[0][0], 1)):
				db.rollback()
				return False
			if not db.delete('OldFiles', ('ApplicationID', 'OldCount'), (appName, appList[0][1] + 1)):
				db.rollback()
				return False
			if not db.insert('Files', fields, data):
				db.rollback()
				return False
	
		db.change_commit(True)
		return True
	except:
		print("An error occurred when updating version and/or adding file into database.")
		db.rollback()
		return False


# add_stats
# Parameters: db is a database class object
#							numUpdatesNeeded is an integer
#							numSuccUpdates is an integer (successful updates)
# Return: True if successful, false otherwise
def add_stats(db, numUpdatesNeeded, numSuccUpdates):
	fields = ['NumUpdatesNeeded', 'NumSuccUpdates', 'Timestamp']
	data = [numUpdatesNeeded, numSuccUpdates, str(time.time())]
#	try:
	if not db.insert("Statistics", fields, data):
		return False
	return True
#	except:
#		print("An error occurred when adding statistics into the database.")
#		return False


#######################################################################
# Get/Retrieve Functions
#######################################################################

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
		if db.query("Application", appName, ("CurrentVersionNum", "Timestamp")):
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


# get_app_exe_regex
# Parameters: db is a database class object
#							appName is a string
# Return: Tuple of the form (Bool, List), list contains strings
#					bool is true if successful, false otherwise
def get_app_exe_regex(db, appName):
	try:
		if db.query("RegExprExe", appName, ("Expression",)):
			l = db.retrieve()
			return (True, list(itertools.chain.from_iterable(l)))
		else:
			return (False, [])
	except:
		print("An error occurred when retrieving application names from database.")
		return (False, [])


# get_app_version_regex
# Parameters: db is a database class object
#							appName is a string
# Return: Tuple of the form (Bool, List), list contains strings
#					bool is true if successful, false otherwise
def get_app_version_regex(db, appName):
	try:
		if db.query("RegExprVersion", appName, ("Expression",)):
			l = db.retrieve()
			return (True, list(itertools.chain.from_iterable(l)))
		else:
			return (False, [])
	except:
		print("An error occurred when retrieving application names from database.")
		return (False, [])


# get_app_dependencies
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


# get_app_scripts
# Parameters: db is a database class object
#							appName is a string
# Return: Tuple of the form (Bool, List)
#					bool is true if successful, false otherwise
def get_app_scripts(db, appName):
	try:
		if not db.query("Scripts", appName, ("Script",)):
			return (False, [])
		l = db.retrieve()
		return (True, list(itertools.chain.from_iterable(l)))
	except:
		print("An error occurred when retrieving application scripts from the database.")
		return (False, [])


# get_app_unistallFirst
# Parameters: db is a database class object
#							appName is a string
# Return: Tuple of the form (Bool, Bool)
#					First bool indicates query successful
#					Second bool is app flag
def get_app_uninstallFirst(db, appName):
	try:
		if not db.query("Application", appName, ("UninstallFirst",)):
			return (False, False)
		l = db.retrieve()
		flag = True if l[0][0] == 1 else False
		return (True, flag)
	except:
		print("An error occurred when retrieving application uninstallFirst flag from the database.")
		return (False, False)


# get_app_currFile
# Parameters: db is a database class object
#							appName is a string
# Return: Tuple of the form (Bool, List)
#					bool is true if successful, false otherwise
def get_app_currFile(db, appName):
	try:
		if not db.query("Files", appName):
			return (False, [])
		l = db.retrieve()
		return (True, l)
	except:
		print("An error occurred when retrieving application files from the database.")
		return (False, [])


# get_app_oldFiles
# Parameters: db is a database class object
#							appName is a string
# Return: Tuple of the form (Bool, List)
#					bool is true if successful, false otherwise
def get_app_oldFiles(db, appName):
	try:
		if not db.query("OldFiles", appName):
			return (False, [])
		l = db.retrieve()
		return (True, l)
	except:
		print("An error occurred when retrieving old application files from the database.")
		return (False, [])


# get_stats
# Parameters: db is a database class object
#							timeRange is either an empty list of a list of two integers
# Return: Tuple of the form (Bool, List)
#					bool is true if successful, false otherwise
def get_stats(db, timeRange = []):
	try:
		if not db.query("Statistics", timeRange = timeRange):
			return (False, [])
		l = db.retrieve()
		return (True, l)
	except:
		print("An error occured when retrieving statistics from the database.")
		return (False, [])


#######################################################################
# Update Functions
#######################################################################

# update_main_url
# Parameters: db is a database class object
#							appName is a string
#							mURL is a string
# Return: True if successful, false otherwise
def update_main_url(db, appName, mainURL):
	try:
		return db.update("Application", ("MainURL",), (mainURL,), ("ApplicationName",), (appName,))
	except:
		print("An error occurred when updating the main url in the database.")
		return False


# update_dl_url
# Parameters: db is a database class object
#							appName is a string
#							dlURL is a string
# Return: True if successful, false otherwise
def update_download_url(db, appName, dlURL):
	try:
		return db.update("Application", ("DownloadURL",), (dlURL,), ("ApplicationName",), (appName,))
	except:
		print("An error occurred when updating the download url in the database.")
		return False


# revert_app
# Parameters: db is a dabase class object
#             appName is a string
#             oldCount is the value associated to an old version to revert to
#             path is the path to the executable
#             exeType is the exeType of the file to revert to
# Return: True if successful, false otherwise
def revert_app(db, appName, oldCount, path, exeType):
	try:
		cont, oldFiles = get_app_oldFiles(db, appName)
		if not cont:
			return False
		
		oldFiles = sorted(oldFiles, cmp=lambda x,y: cmp(x[-1], y[-1]))
		db.change_commit(False)
		
		if not db.update("Application", ("CurrentVersionNum","Timestamp"), (oldFiles[int(oldCount) - 1][3], str(time.time())), ("ApplicationName",), (appName,)):
			db.rollback()
			return False
		
		for i in range(int(oldCount)):
			if not db.delete("OldFiles", ("ApplicationID","OldCount"), (appName,i+1)):
				db.rollback()
				return False
		for i in range(int(oldCount), len(oldFiles)):
			if not db.update("OldFiles", ("OldCount",), (oldFiles[i][-1] - oldFiles[int(oldCount) - 1][-1],), ("ApplicationID",), (appName,)):
				db.rollback()
				return False

		"CREATE TABLE Files(ID INTEGER PRIMARY KEY, ApplicationID INTEGER REFERENCES Application(ID), CurrEXEFileName TEXT, LocalEXELocation TEXT, EXEType TEXT)",
		if not db.update("Files", ("CurrEXEFileName", "LocalEXELocation", "EXEType"), (oldFiles[int(oldCount) - 1][2], path, exeType), ("ApplicationID",), (appName,)):
			db.rollback()
			return False
		
		db.change_commit(True)
		return True
	except:
		print("An error occurred when reverting back to an old version in the database.")
		db.rollback()
		return False

#######################################################################
# Delete Functions
#######################################################################

# del_app_regex
# Parameters: db is a database class object
#							appName is a string 
#							regex is a list of strings
# Return: List of bools, first indicates successful db operation, all others
#           represent if item was deleted successfully
def del_app_exe_regex(db, appName, regex = []):
	fields = ['ApplicationID', 'Expression']
	deletions = []
	try:
		if regex != []:
			for re in regex:
				deletions.append(db.delete('RegExprExe', fields, (appName, re)))
		else:
			deletions.append(db.delete('RegExprExe', [fields[0]], (appName,)))
		deletions.insert(0, True)
		return deletions
	except:
		print("An error occurred when deleting the application's regular expression data.")
		deletions.insert(0, False)
		return deletions


# del_app_version_regex
# Parameters: db is a database class object
#							appName is a string 
#							regex is a list of strings
# Return: List of bools, first indicates successful db operation, all others
#           represent if item was deleted successfully
def del_app_version_regex(db, appName, regex = []):
	fields = ['ApplicationID', 'Expression']
	deletions = []
	try:
		if regex != []:
			for re in regex:
				deletions.append(db.delete('RegExprVersion', fields, (appName, re)))
		else:
			deletions.append(db.delete('RegExprVersion', [fields[0]], (appName,)))
		deletions.insert(0, True)
		return deletions
	except:
		print("An error occurred when deleting the application's regular expression data.")
		deletions.insert(0, False)
		return deletions


# del_app_scripts
# Parameters: db is a database class object
#							appName is a string
#							scriptName is a list of strings
# Return: List of bools, first indicates successful db operation, all others
#           represent if item was deleted successfully
def del_app_scripts(db, appName, scriptNames = []):
	fields = ['ApplicationID', 'Script']
	deletions = []
	try:
		if scriptNames != []:
			for script in scriptNames:
				deletions.append(db.delete('Scripts', fields, (appName, script)))
		else:
			deletions.append(db.delete('Scripts', [fields[0]], (appName,)))
		deletions.insert(0, True)
		return deletions
	except:
		print("An error occurred when deleting the application's script data.")
		deletions.insert(0, False)
		return deletions


