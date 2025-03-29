from __future__ import division
import numpy as np
import datetime
#import MySQLdb
import pymysql
import os
import subprocess
import fnmatch
import time
from distutils.dir_util import copy_tree

import utilities.database as database

def duplicate_backslashes(path):
    retstr = ""
    for c in path:
        retstr += c
        if c == '\\':
            retstr += c
    return retstr


class Operator():
    
    def __init__(self,setupname=None,datapath=None,codepath=None,libs=[],databaseDetials=None):
        
        # saves the ID (unique identifier) of the last experiment started
        self.currentID = None
        
        # the absolute path to the data is storage
        if datapath is None:
            #self.dataPath=os.getenv("HOME")+'/data'
            #self.dataPath=os.getenv("USERPROFILE")+'\\data' #Windows port
            self.dataPath = 'D:\\data'
        else:
            self.dataPath   =datapath
        
        # the absolute path where the code resides
        if codepath is None:
            #self.codePath=os.getenv("HOME")+'/code'
            self.codePath=os.getenv("USERPROFILE")+'\\code' #Windows port
        else:
            self.codePath = codepath
        
        # create database handler
        if databaseDetials==None:
            self.db = database.Database()
        else:
            self.db = database.Database(databaseDetails=databaseDetials)
        
        # Force a setup name
        if setupname in self.db.properties['setups'] or setupname == 'Rogue':
            self.setupName=setupname
        else:
            print("You need to provide a setup name choose from:")
            for setup in self.db.properties['setups']:
                print("\t"+setup)
            print ("\n\nIf yout setup is new, add it to the database")
            raise Exception()
        
        # Check of libararies that we copy
        self.userDefinedLibraryDirs=[]
        if len(libs)==0:
            print("You are not copying any libraries. Are you sure about that?")
        else:
            for library in libs:
                self.userDefinedLibraryDirs.append(library)
        
        # Used to trim the juptyer file
        self.excludeMarker = ">>>>>"
        self.includeMarker = "<<<<<"
        self.lineIgnoreKeys = ["get_ipython().",".runExperiment("]
        
        
    
    
    
    def runExperiment(self,nbPath,databaseEntries,pythonversion='3.6'):
        """
        Run the experiment:
        
            1. Generates a unique identifier for the measurement. 
            2. Generates a database entry. 
            3. Creates the file structure in the self.dataPath folder. 
            4. Creates a python file from the specified file in nbPath. 
            5. Copies all its dependencies into the created folders. 
            6. Opens a terminal window ready to running the script
        
        Prints information 
            - on which script it runs,
            - whether the database entry test flag is set,
            - the directory of the current measurement.
        
        Note that if the test flag in the database entries is set to true, the data will be 
        deleted from the database at some point.
        
        Parameters
        ==========
        
        nbPath: string
           File path of the notebook to be executed. Path is relative to self.codePath 
                            (e.g. "vibrometer/scripts/quadrupole/scan1D").
        
        databaseEntries: dict
          Dictionary specifying the database entries. Required keys are defined in self.db.reqDatabaseKeys.
        
                
        """
        # check for completeness of the databaseEntries
        if not self.db.isComplete(databaseEntries):
            return None
        
        # check appropriate file ending of the specified noteobok 
        if not nbPath.endswith(".ipynb"):
            self.currentNbPath = nbPath + ".ipynb"
       
        #temp = nbPath.split("/")[:-1]
        temp = nbPath.split("\\")[:-1] #Windows port
        for k in range(len(temp)):
            #temp.insert(2*(k)+1,'/')
            temp.insert(2*(k)+1,'\\') #Windows port
        #print("  %s\033[43m%s\033[0m"%(''.join(temp),nbPath.split("/")[-1]))
        print("  %s\033[43m%s\033[0m"%(''.join(temp),nbPath.split("\\")[-1])) #Windows port
        
        # check test flag and inform the user about the choice made
        if databaseEntries['test']:
            print("in test mode")
            print("  all your data will be \033[41m deleted \033[0m!")
        
        # Create the file strucutre
        self.createFileStructure()
        print("The directory is %s"%self.currentFoldername)
        
        # Export all code into it
        self.exportCode()
        
        # Create database entry
        success = self.db.createMeasurementEntry(self.currentID,
                                                 self.now,
                                                 self.currentFoldernameForDB,databaseEntries)
        
        # If all went well, we go for it
        if success:
            self.startExperiment(pythonversion)
        else:
            os.system("rm -rf %s"%self.currentFoldername)
            print("Could not generate database entry. Did not start experiment.")
        return self.currentID,self.currentFoldername
    
    def createFileStructure(self):
        """
        Creates the file structure in the target directory of the experiment.
        
        The foldername structure is
        self.dataPath/self.setupName/date/uniqueIdentifier 
        
        """
        
        # created a unique identifier for the current run of the experiment
        self.createIdentifier()
        
        # create foldername
        self.now = datetime.datetime.now()
        #self.currentFoldername = self.dataPath+\
        #                '/'+self.setupName+\
        #                '/'+'%04i'%self.now.year+'-'+'%02i'%self.now.month+'-'+'%02i'%self.now.day+\
        #                '/'+self.currentID
        #Windows port
        self.currentFoldername = self.dataPath+\
                        '\\'+self.setupName+\
                        '\\'+'%04i'%self.now.year+'-'+'%02i'%self.now.month+'-'+'%02i'%self.now.day+\
                        '\\'+self.currentID
        self.currentFoldernameForDB = self.setupName+\
                        '/'+'%04i'%self.now.year+'-'+'%02i'%self.now.month+'-'+'%02i'%self.now.day+\
                        '/'+self.currentID
        #self.currentFoldernameForDB = self.setupName+\
        #                '\\'+'%04i'%self.now.year+'-'+'%02i'%self.now.month+'-'+'%02i'%self.now.day+\
        #                '\\'+self.currentID
        
        # create folder 
        #folderStruct = self.currentFoldername.split("/")
        folderStruct = self.currentFoldername.split("\\") #Windows port
        tempFolder = ''
        for fs in folderStruct[1:]:
            #tempFolder = tempFolder +"/"+fs
            tempFolder = tempFolder +"\\"+fs #Windows port
            if not os.path.exists(tempFolder):
                os.system("mkdir "+tempFolder)
        # create code folder structure
        #if not os.path.exists(self.currentFoldername+"/modules"):
        if not os.path.exists(self.currentFoldername+"\\modules"): #Windows port
            # import folders
            #os.system("mkdir "+self.currentFoldername+"/modules")
            #f = open(self.currentFoldername+'/modules/__init__.py','w')
            os.system("mkdir "+self.currentFoldername+"\\modules") #Windows port
            f = open(self.currentFoldername+'\\modules\\__init__.py','w') #Windows port
            f.close()
            for directory in self.userDefinedLibraryDirs:
                #subFolderStruct = directory.split("/")
                subFolderStruct = directory.split("\\") #Windows port
                #tempSubFolder = self.currentFoldername+"/modules"
                tempSubFolder = self.currentFoldername+"\\modules" #Windows port
                for fs in subFolderStruct:
                    #tempSubFolder = tempSubFolder + "/" + fs
                    tempSubFolder = tempSubFolder + "\\" + fs #Windows port
                    if not os.path.exists(tempSubFolder):
                        os.system("mkdir "+tempSubFolder)
                        #f = open(tempSubFolder+'/__init__.py','w')
                        f = open(tempSubFolder+'\\__init__.py','w') #Windows port
                        f.close()
    
    def exportCode(self,fromiP=True):
        """
        Export code into folder structure of current run. 
        
        """
        #nbName = self.currentNbPath.split("/")[-1].split(".")[0]
        nbName = self.currentNbPath.split("\\")[-1].split(".")[0] #Windows port
        
        # create script
        if fromiP:
            #os.system("jupyter nbconvert --to script "+self.codePath+'/'+self.currentNbPath)
            print("python -m nbconvert --to script "+self.codePath+'\\'+self.currentNbPath)
            os.system("python -m nbconvert --to script "+self.codePath+'\\'+self.currentNbPath) #Windows port
        else:
            #Pascal please du your shit.
            pass
        
        # adjust script
        f = open(nbName+".py",'r+')
        lines = f.readlines()
        include = True
        fromFuture = True
        importStarted = False
        for k, line in enumerate(lines):
            if line.startswith("from ") or line.startswith("import "):
                importStarted = True
            # check whether we are still in the from __future__ phase (from __future__ statements have to be at the very beginning of the code).
            if importStarted and not line.startswith("from __future__") and fromFuture:
                fromFuture = False
                # load os library as the first library after any from __future__ directive.
                # change into the correct working directory before any other import statements, such that the relative paths are correct.
                lines.insert(k,"os.chdir('%s')\n"%duplicate_backslashes(self.currentFoldername))
                lines.insert(k,"import os\n")
            # check whether line is suposed to be part of the code or not
            if self.excludeMarker in line:
                include = False
                lines[k] = '#'+line
                continue
            if self.includeMarker in line:
                include = True
                lines[k] = '#'+line
                continue
            if include:
                # comment lines matching self.lineIgnoreKeys
                for lineIgnoreKey in self.lineIgnoreKeys:
                    if lineIgnoreKey in line:
                        lines[k] = "# "+line
            else:
                # comment lines not to be included
                lines[k] = '#'+line
        # create standardized end of file
        lines.append('print("")\n')
        lines.append('print("")\n')
        lines.append('print("")\n')
        lines.append('print("****************************")\n')
        lines.append('print("Made it to the end of run.py")\n')
        f.seek(0)
        f.writelines(lines)
        f.close()
        
        # move script
        #os.system("mv "+nbName+".py "+self.currentFoldername+"/"+"run.py")
        #os.rename(nbName+".py", self.currentFoldername+"\\"+"run.py") #Windows port
        import shutil
        shutil.move(nbName+".py", self.currentFoldername+"\\"+"run.py") #Move to different physical media

        # copy all the import files
        libPath = "C:\\Users\\Control\\pythonlibs" #Windows port
        for directory in self.userDefinedLibraryDirs:
            #os.system("cp -r "+self.codePath+"/"+directory+"/* "+self.currentFoldername+"/modules/"+directory)
            copy_tree(libPath+"\\"+directory, self.currentFoldername+"\\modules\\"+directory) #Windows port

        # replace userDefinedLibraries in all the modules
        # find all the files we just copied into the data (and modules) folder
        matches = []
        for root, dirnames, filenames in os.walk(self.currentFoldername):
            for filename in fnmatch.filter(filenames,'*.py'):
                matches.append(os.path.join(root,filename))
        # go through all the files and replace their import directives 
        for filename in matches:
            f = open(filename,'r+')
            lines = f.readlines()
            for k, line in enumerate(lines):
                for directory in self.userDefinedLibraryDirs:
                    #libPath = directory.replace("/",".")
                    libPath = directory.replace("\\",".") #Windows port
                    replace = False
                    # replace all the import statements to relative import statements
                    if line.startswith("from "+libPath):
                        lines[k] = line.replace("from "+libPath,"from modules."+libPath)
                    if line.startswith("import "+libPath):
                        lines[k] = line.replace("import "+libPath,"import modules."+libPath)
                    # replace all the self.codePath strings by the proper relative path
                    if self.codePath in line:
                        #lines[k] = line.replace(self.codePath,self.currentFoldername+"/modules")
                        lines[k] = line.replace(self.codePath,self.currentFoldername+"\\modules") #Windows port
            f.seek(0)
            f.writelines(lines)
            f.close()
        return
    
    def startExperiment(self,pythonversion='3.6'):
        """
        Starts the experiment. Do not call this method directly. Use runExperiment() instead.
        
        """
        
        #script='''
        #tell application "iTerm"
        #    set newWindow to (create window with default profile)
        #    # Split panel
        #    tell current session of newWindow
        #        set name to "Runnig MID: %s"
        #        set rows to 30
        #        split horizontally with default profile
        #    end tell
        #
        #    # Exec commands
        #    tell first session of current tab of newWindow
        #        write text "workon mm-runexperiment"
        #        write text "cd %s"
        #        write text "clear"
        #        write text "pwd"
        #        write text "python -u run.py > run.log"
        #    end tell
        #    tell second session of current tab of current window
        #        write text "cd %s"
        #        write text "tail -f run.log"
        #    end tell
        #    activate
        #end tell
        #'''%(self.currentID,self.currentFoldername,self.currentFoldername)

        
        #p = subprocess.Popen(['osascript', '-'], 
        #                     stdin=subprocess.PIPE, 
        #                     stdout=subprocess.PIPE, 
        #                     stderr=subprocess.PIPE)
        #stdout, stderr = p.communicate(script.encode())

        #Windows port
        powershell_script = r'''
        # Start Python script in the top panel, change python 
        $topPanel = New-Object System.Diagnostics.ProcessStartInfo
        $topPanel.FileName = "powershell.exe"
        $topPanel.Arguments = "echo 'running in %s'; cd %s; python -u run.py | tee -filepath log.txt; Read-Host 'Script ended, press Enter to exit...'" # here change python to python3 for venv
        $topPanel.CreateNoWindow = $false
        $topPanel.UseShellExecute = $true
        [System.Diagnostics.Process]::Start($topPanel)
        '''%(self.currentID, self.currentFoldername)
        # Full path to the PowerShell script
        script_path = os.path.abspath('powershell_script.ps1')

        # Save the PowerShell script to a .ps1 file
        with open('powershell_script.ps1', 'w') as ps_file:
            ps_file.write(powershell_script)

        # Run the PowerShell script using subprocess
        subprocess.run(['powershell.exe', '-ExecutionPolicy', 'Bypass', '-File', 'powershell_script.ps1'])

        time.sleep(5)
        # Clean up the temporary PowerShell script file
        os.remove(script_path)

    def createIdentifier(self):
        """
        Create a unique identifier for the current run of the experiment.
        
        Creates random identifier and checks with database that it is unique.
        Repeats until uniques is achieved.
        
        """
        # boolean whether generated identifier is unique
        newID = False
        success = True
        while(not newID):
            # create random integer
            num=np.random.randint(1,62**5)
            # choose number system with base 62
            base = 62
            identifier = ''
            k = 0
            # basis for number system
            digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
            # rewrite num with respect to base 62
            while num > 0:
                rest = np.mod(num,base)
                num  = (num-rest)/base
                identifier = digits[int(rest)]+identifier
                k += 1
            # zero padding
            for n in range(k,5):
                identifier = '0'+identifier
            
            # check that the identifier is unused
            # create sql request
            sql = "SELECT mid FROM measurements"
            [success,dbSamples] = self.db.executeSqlRequest(sql)
            if success:
                # check for uniqueness
                newID = identifier not in dbSamples
            else:
                print("Could not access database to check for uniqueness of identifier. Set identifier to non-unique identifier '00000'.")
        if newID:
            self.currentID = identifier