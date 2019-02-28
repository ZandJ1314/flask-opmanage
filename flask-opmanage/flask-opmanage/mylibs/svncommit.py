# -*- coding: utf-8 -*-
import sys,time,random,json,traceback,subprocess,pysvn,os,shutil
reload(sys)
sys.setdefaultencoding('utf8')
from flask import current_app
from . import filemd5
from .. import db
from .. import cache
from ..models import *

def get_login(realm,username,may_save):
    return True,svn_username,svn_pass,True
def svn_update(svnUrl,svnDir):
    try:
        global svn_username,svn_pass
        svn_username = current_app.config.get('SVNUSERNAME')
        svn_pass = current_app.config.get('SVNPASS')
        client = pysvn.Client()
        client.callback_get_login = get_login
        if os.path.exists(svnDir):
            client.update(svnDir)
        else:
            client.checkout(svnUrl,svnDir)
        return 0
    except:
        errorlog = traceback.format_exc()
        current_app.logger.error(errorlog)
        return 1

def svn_commit(svnDir,log_message):
    try:
        global svn_username,svn_pass
        svn_username = current_app.config.get('SVNUSERNAME')
        svn_pass = current_app.config.get('SVNPASS')
        client = pysvn.Client()
        client.callback_get_login = get_login
        changes = client.status(svnDir)
        for f in changes:
            if f.text_status == pysvn.wc_status_kind.unversioned:
                client.add(f.path)
        client.checkin(svnDir,log_message)
        return 0
    except:
        errorlog = traceback.format_exc()
        current_app.logger.error(errorlog)
        return 1

def CommitPlanRes():
    commitMsg = {}
    try:
        svnUrl = current_app.config.get('SVNURL')
        gameName = current_app.config.get('GAMENAME')
        svnUrl = "%s/%sres" %(svnUrl,gameName)
        svnDir = "svndata/%sres" %(gameName)
        svnUpdateCode = svn_update(svnUrl,svnDir)
        if svnUpdateCode != 0:
            commitMsg['code'] = 3
            return commitMsg
        else:
            distPath = os.path.join(svnDir,"%splanres" %(gameName))
            if not os.path.exists(distPath):
                os.mkdir(distPath)
            shutil.copy("upload/res.zip",distPath)
            log_message = "commit res"
            svnCommitCode = svn_commit(svnDir,log_message)
            if svnCommitCode != 0:
                commitMsg['code'] = 4
                return commitMsg
            else:
                commitMsg['code'] = 0
                return commitMsg
    except:
        commitMsg['code'] = 6
        errorlog = traceback.format_exc()
        current_app.logger.error(errorlog)
        return commitMsg

def CommitGameData(dbName,tablesName):
    commitMsg = {}
    try:
        datasrcIP = current_app.config.get('DATASRCIP')
        datasrcPort = current_app.config.get('DATASRCPORT')
        datasrcUser = current_app.config.get('DATASRCUSER')
        datasrcPass = current_app.config.get('DATASRCPASS')
        svnUrl = current_app.config.get('SVNURL')
        gameName = current_app.config.get('GAMENAME')
        svnUrl = "%s/%sdata" %(svnUrl,gameName)
        svnDir = "svndata/%sdata" %(gameName)
        try:
            if os.path.exists("upload"):
                pass
            else:
                os.mkdir("upload")
            if tablesName == "all":
                MysqlDumpCmd = "/usr/bin/mysqldump -h %s -P %s -u %s -p%s %s > upload/game_data.sql" %(datasrcIP,datasrcPort,datasrcUser,datasrcPass,dbName)
                NewTablesName = "all"
            else:
                tablesNameSplit = tablesName.split(',')
                NewTablesName = ' '.join(tablesNameSplit)
                MysqlDumpCmd = "/usr/bin/mysqldump -h %s -P %s -u %s -p%s %s %s > upload/game_data.sql" %(datasrcIP,datasrcPort,datasrcUser,datasrcPass,dbName,NewTablesName)
            p = subprocess.Popen("%s" %(MysqlDumpCmd),shell=True,close_fds=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            p.wait()
            errorput = p.stderr.read()
            stdoutput = p.stdout.read()
            if p.returncode != 0:
                commitMsg['code'] = 2
                current_app.logger.error(errorput)
                return commitMsg
            else:
                if os.path.exists("svndata"):
                    pass
                else:
                    os.mkdir("svndata")
                svnUpdateCode = svn_update(svnUrl,svnDir)
                if svnUpdateCode != 0:
                    commitMsg['code'] = 3
                    return commitMsg
                else:
                    shutil.copy("upload/game_data.sql","%s/%sgamedata_yw" %(svnDir,gameName))
                    log_message = "commit tables %s" %(NewTablesName)
                    svnCommitCode = svn_commit(svnDir,log_message)
                    if svnCommitCode != 0:
                        commitMsg['code'] = 4
                        return commitMsg
                    else:
                        gameDataMd5 = filemd5.FileMd5("upload/game_data.sql")
                        commitMsg['code'] = 0
                        commitMsg['GameDataMd5'] = gameDataMd5
                        commitMsg['svnDir'] = "%sgamedata_yw" %(gameName)
                        return commitMsg
        except:
            commitMsg['code'] = 5
            errorlog = traceback.format_exc()
            current_app.logger.error(errorlog)
            return commitMsg
    except:
        commitMsg['code'] = 6
        errorlog = traceback.format_exc()
        current_app.logger.error(errorlog)
        return commitMsg
                    
            
            
            