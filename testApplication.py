#!/usr/bin/python
import wpm_db
from wpm_app import app


mydb = wpm_db.db("dbFile", "dbLog")

#vim = Application("vim", "http://www.vim.org/download.php", 'href=".*\.exe"')
vim = app("vim", "http://www.vim.org/download.php", 'href=".*vim.*\.exe"')
#vim.checkUpdates()
vim.dlUpdates()

#vBox = Application("virtual box", "https://www.virtualbox.org/wiki/Downloads", 'href=".*Win.*\.exe"')
#
#vBox.checkUpdates()
#vBox.dlUpdates()
