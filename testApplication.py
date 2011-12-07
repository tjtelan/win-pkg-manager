#!/usr/bin/env python2.7
import wpm_db, db_wrapper
from wpm_app import app

mydb = wpm_db.db("dbFile", "dbLog")

# Add vim to the db.
vim_name = unicode('gvim')
vim_url = "http://www.vim.org"
vim_dl_url = "http://www.vim.org/download.php"
vim_version = "1.2.3"
vim_regex = '".*vim.*\.exe"'
vim_version_regex = '\d+.*\d'


appLogFileName = "appLog"

validQuery, applications = db_wrapper.get_applications(mydb)

print 'All Applicaitons:', applications
if validQuery and not vim_name in applications:
    print 'adding vim to the db.'
    db_wrapper.add_app(mydb, vim_name, vim_version, vim_dl_url, vim_url)
    db_wrapper.add_exe_regex(mydb, vim_name, [vim_regex])
    db_wrapper.add_version_regex(mydb, vim_name, [vim_version_regex])

vim = app(vim_name, mydb, appLogFileName)
updatesAvail = vim.checkUpdates()
print 'gvim update available?', updatesAvail

if updatesAvail:
    vim.dlUpdates()

putty_name = 'putty'
putty_url = 'http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html'
putt_dl_url = 'http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html'
putty_version = '1.0'
putty_regex = '".*putty.*\.exe"'
putty_version_regex = '\d+.*\d'

if validQuery and putty_name not in applications:
    print 'adding putty to the db.'
    db_wrapper.add_app(mydb, putty_name, putty_version, putt_dl_url, putty_url)
    db_wrapper.add_exe_regex(mydb, putty_name, [putty_regex])
    db_wrapper.add_version_regex(mydb, putty_name, [putty_version_regex])

putty = app(putty_name, mydb, appLogFileName)

updatesAvail = putty.checkUpdates()
print 'putty updates available? ', updatesAvail
if updatesAvail:
    putty.dlUpdates()


winscp_name = 'winscp'
winscp_url = 'http://winscp.net/eng/download.php'
winscp_version = '1.0'
winscp_regex = '".*winscp.*\.exe"'
winscp_version_regex = '\d+.*\d'
if validQuery and winscp_name not in applications:
    print 'adding winscp to the db.'
    db_wrapper.add_app(mydb, winscp_name, winscp_version, winscp_url, winscp_url)
    db_wrapper.add_exe_regex(mydb, winscp_name, [winscp_regex])
    #db_wrapper.add_version_regex(mydb, winscp_name, [winscp_version_regex])

winscp = app(winscp_name, mydb, appLogFileName)
updatesAvail = winscp.checkUpdates()
print 'winscp updates available? ', updatesAvail
if updatesAvail:
    winscp.dlUpdates()


# Stuff for 7zip.
SevenZip_name = '7zip'
SevenZip_url = 'http://www.7-zip.org/download.html'
SevenZip_version = '1.0'
SevenZip_regex = '"http.*7z.*\.exe"'
SevenZip_version_regex = '\d+'
if validQuery and SevenZip_name not in applications:
    print 'adding SevenZip to the db.'
    db_wrapper.add_app(mydb, SevenZip_name, SevenZip_version, SevenZip_url, SevenZip_url)
    db_wrapper.add_exe_regex(mydb, SevenZip_name, [SevenZip_regex])
    db_wrapper.add_version_regex(mydb, SevenZip_name, [SevenZip_version_regex])

SevenZip = app(SevenZip_name, mydb, appLogFileName)

updatesAvail = SevenZip.checkUpdates()
print '7zip update available? ', updatesAvail
if updatesAvail:
    SevenZip.dlUpdates()
