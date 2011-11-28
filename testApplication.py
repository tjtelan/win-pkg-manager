#!/usr/bin/python
import wpm_db, db_wrapper
from wpm_app import app

mydb = wpm_db.db("dbFile", "dbLog")

# Add vim to the db.
vim_name = u'vim'
vim_url = "www.vim.org"
vim_dl_url = "http://www.vim.org/download.php"
vim_version = "1.2.3"
vim_regex = 'href=".*vim.*\.exe"'

if not vim_name in db_wrapper.get_applications(mydb)[1]:
    #print db_wrapper.get_applications(mydb)
    db_wrapper.add_app(mydb, vim_name, vim_version, vim_url, vim_dl_url)
    db_wrapper.add_regex(mydb, vim_name, [vim_regex])
else:
    print db_wrapper.get_app_regex(mydb, vim_name)

vim = app("vim", mydb)

vim.checkUpdates()
vim.dlUpdates()


#vim = Application("vim", "http://www.vim.org/download.php", 'href=".*\.exe"')
#vim = app("vim", "http://www.vim.org/download.php", 'href=".*vim.*\.exe"')
#vim.checkUpdates()

#vBox = Application("virtual box", "https://www.virtualbox.org/wiki/Downloads", 'href=".*Win.*\.exe"')
#
#vBox.checkUpdates()
#vBox.dlUpdates()
