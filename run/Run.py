from db.DB import DB
from lib.logger import Logger
from winreg import *

#key = CreateKey(HKEY_LOCAL_MACHINE, "SOFTWARE\\Microsoft\Windows\\CurrentVersion\\App Paths\\vscodetest.exe")
#SetValueEx(key, '', 0, REG_SZ, 'C:\\Users\\won\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe')
#SetValueEx(key, 'Path', 0, REG_SZ, 'C:\\Users\\won\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe')
#DeleteKey(HKEY_LOCAL_MACHINE, "SOFTWARE\\Microsoft\Windows\\CurrentVersion\\App Paths\\vscodetest.exe")

class Run(object):
    logger = Logger("Run")
    
    def __init__(self):
        self.db = DB()

    def add_run_file(self, runName, runPath, runExe):
        try:
            key = CreateKey(HKEY_LOCAL_MACHINE, f"SOFTWARE\\Microsoft\Windows\\CurrentVersion\\App Paths\\{runName}")
            SetValueEx(key, '', 0, REG_SZ, runPath + "\\" + runExe)
            SetValueEx(key, 'Path', 0, REG_SZ, runPath)                     
            result = self.set_run(runName,runPath,runExe)  
        except Exception as e:
            self.logger.error(e)            
            result = "에러발생 로그확인"

        key.Close()
        return result
        

    def get_all_run_list(self): 
        rows = self.db.find_all()
        if rows is None:
            return None

        return rows

    def set_run(self, runName, runPath, runExe):
            result = self.db.save(runName, runPath, runExe)

            if result != 1:
                return "DB Error 발생"
                    
            return result      

    def delete_run(self, runId, runName, runPath, runExe):
        try:
            DeleteKey(HKEY_LOCAL_MACHINE, f"SOFTWARE\\Microsoft\Windows\\CurrentVersion\\App Paths\\{runName}")   
            result = self.db.delete_by_run_id(runId, runName, runPath, runExe)     
            if result != 1:
                return "DB Error 발생"

            return result
        except Exception as e:
            self.logger.error(e)    
    
    def get_last_run_id(self): 
        row = self.db.find_last_run_id()
        if row is None:
            return ""
        elif row == -1:
            return "DB Error 발생"

        return row[0]
