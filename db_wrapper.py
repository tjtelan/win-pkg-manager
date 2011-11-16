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


# add_regex
# Parameters: db is a database class object
#							appName is a string 
#							regex is a list of strings
# Return: List of bools, first indicates successful db operation, all others
#           represent if item was able to be inserted (unique)
def add_regex(db, appName, regex):
	fields = ['ApplicationID', 'Expression']
	insertions = []
	cont, currAppRegex = get_app_regex(db, appName)
	if (not cont):
		return [False]
	try:
		for re in regex:
			if re in currAppRegex:
				insertions.append(False)
			else:			
				insertions.append(db.insert('RegExpr', fields, (appName, re)))
				currAppRegex.append(re)
		insertions.insert(0, True)
		return insertions
	except:
		print("An error occurred when inserting the application's regular expression data.")
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

# add_file
# Parameters: db is a database class object
#							All other parameters are strings
# Return: List of bools, first indicates successful db operation, all others
#           represent if item was able to be inserted (unique)
def add_file(db, appName, currEXEFileName, localEXELocation, EXEType):
	fields = ['ApplicationID', 'CurrEXEFileName', 'LocalEXELocation', 'EXEType']
	data = [appName, currEXEFileName, localEXELocation, EXEType]	
	try:
		insertion = db.insert('Files', fields, data)
		return [True, insertion]
	except:
		print("An error occurred when inserting the application's file data.")
		return [False, False]


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
			db.update("Application", ("timestamp",), (str(time.time()),), ("ApplicationName",), (appName,))
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

<<<<<<< HEAD

=======
>>>>>>> f82551751a213876383c551884acc384ab0c262f
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

<<<<<<< HEAD

# get_app_dependencies
=======
# get_dependencies
>>>>>>> f82551751a213876383c551884acc384ab0c262f
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






# del_app_regex
# Parameters: db is a database class object
#							appName is a string 
#							regex is a list of strings
# Return: List of bools, first indicates successful db operation, all others
#           represent if item was deleted successfully
def del_app_regex(db, appName, regex = []):
	fields = ['ApplicationID', 'Expression']
	deletions = []
	try:
		if regex != []:
			for re in regex:
				deletions.append(db.delete('RegExpr', fields, (appName, re)))
		else:
			deletions.append(db.delete('RegExpr', [fields[0]], (appName,)))
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


