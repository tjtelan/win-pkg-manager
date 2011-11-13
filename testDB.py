#!/usr/bin/env python
import wpm_db
import db_wrapper

mydb = wpm_db.db("dbFile", "dbLog")

print("\nInsert Test")

mydb.insert("Application", ("ApplicationName", "CurrentVersionNum"), ("App", "1.0"))
mydb.insert("RegExpr", ("ApplicationID", "Expression"), ("App", "[a-z]"))
mydb.insert("RegExpr", ("ApplicationID", "Expression"), ("App", "[0-9]"))
mydb.query("RegExpr", "App")
qList = mydb.retrieve(3)
for item in qList:
	print(item)

print("\nAfter deletion")
mydb.delete("RegExpr", ("ApplicationID", "Expression"), ("App", "[a-z]"))
mydb.query("RegExpr", "App")
qList = mydb.retrieve(3)
for item in qList:
	print(item)

print("\nBefore Update")
mydb.query("Application", "App")
qList = mydb.retrieve(1)
print(qList)

print("\n After Update")
mydb.update("Application", ("CurrentVersionNum",), ("1.1",), ("ApplicationName",), ("App",))
mydb.query("Application", "App")
qList = mydb.retrieve(1)
print(qList)

mydb.update("RegExpr", ("Expression",), ("^[4-5]",), ("ApplicationID",), ("App", ))
mydb.query("RegExpr", "App")
qList = mydb.retrieve(3)
for item in qList:
	print(item)

print("----------------DB Wrapper Test-------------------")
print("Unique App Insert Test", db_wrapper.add_app(mydb, "latestApp", "1.2.3", "http://test.com", "http://test.com/dl"))
print(db_wrapper.get_applications(mydb))
print("Non-Unique App Insert Test", db_wrapper.add_app(mydb, "latestApp", "1.2.3", "http://test.com", "http://test.com/dl"))
print("Get Version Test", db_wrapper.get_app_version(mydb, "latestApp"))
print("Get URLs Test", db_wrapper.get_app_urls(mydb, "latestApp"))
print("Add Dependencies", db_wrapper.add_dependencies(mydb, "App", ["latestApp"]))
print("Get Dependency Name", db_wrapper.get_dependencies(mydb, "App"))
mydb.query("Dependencies", "App")
qList = mydb.retrieve(1)
print(qList)
print("Add Dependencies - Error", db_wrapper.add_dependencies(mydb, "App", ["DNE"]))
