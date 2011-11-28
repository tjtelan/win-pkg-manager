#!/usr/bin/python
import wpm_db, db_wrapper
from wpm_app import app

mydb = wpm_db.db("dbFile", "dbLog")

# Add vim to the db.
vim_name = u'vim'
vim_url = "http://www.vim.org"
vim_dl_url = "http://www.vim.org/download.php"
vim_version = "1.2.3"
vim_regex = 'href=".*vim.*\.exe"'

appLogFileName = "appLog"

validQuery, applications = db_wrapper.get_applications(mydb)
if validQuery and not vim_name in applications:
    db_wrapper.add_app(mydb, vim_name, vim_version, vim_url, vim_dl_url)
    db_wrapper.add_regex(mydb, vim_name, [vim_regex])

vim = app("vim", mydb, appLogFileName)

#vim.checkUpdates()
vim.dlUpdates()


#vBox = Application("virtual box", "https://www.virtualbox.org/wiki/Downloads", 'href=".*Win.*\.exe"')
#
#vBox.checkUpdates()
#vBox.dlUpdates()
