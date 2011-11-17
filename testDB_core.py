#!/usr/bin/env python
import wpm_db

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

print ("\nDoesn't commit")
mydb.change_commit(False)
mydb.update("RegExpr", ("Expression",), ("^[4-5]",), ("ApplicationID",), ("App", ))
mydb.query("RegExpr", "App")
qList = mydb.retrieve(3)
for item in qList:
	print(item)

print ("\nRollback")
mydb.rollback()
mydb.query("RegExpr", "App")
qList = mydb.retrieve(3)
for item in qList:
	print(item)
