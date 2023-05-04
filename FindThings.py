from PyQt6 import QtGui
from PyQt6.QtWidgets import *
import sys
import time
import os
from os import error, path, stat
from datetime import datetime

class ShowFileInfo(QWidget):
    def __init__(self):
        super().__init__(self)
        self.resize(450, 550)
        self.formLayout = QFormLayout(self)
        groupbox = QGroupBox("Results")
        self.ResultNum = 1
            

        groupbox.setLayout(self.formLayout)
        scroll = QScrollArea(self)
        scroll.setWidget(groupbox)
        scroll.setWidgetResizable(True)
        # scroll.setFixedHeight(400)
        self.save = QPushButton("Save")
        self.save.clicked.connect(self.saveInfo)    

        layout = QVBoxLayout()
        layout.addWidget(scroll)
        layout.addWidget(self.save)

        self.setLayout(layout)


    def saveInfo(self):
        fileInfo = open("fileInfo.txt", "w")
        self.save.setDisabled(True)

        for i in range(0, self.formLayout.rowCount()):
            widget_item = self.formLayout.itemAt(i).widget()
            text = widget_item.text()
            fileInfo.write(text + "\n")

        fileInfo.close()

        self.save.setEnabled(True)

    def addResults(self, allInfo):
        self.formLayout.addRow(QLabel("Result: " + str(self.ResultNum)))
        for info in allInfo:
            s = QLabel(info)
            # s.setStyleSheet("color: #880808; font: algerian, times new roman, castellar; font:bold;  text-transform: uppercase;")
            self.formLayout.addRow(s)

        self.ResultNum += 1

    def endTask(self):
        for i in range(0, self.formLayout.rowCount()):
            self.formLayout.removeRow(0)
        self.ResultNum = 1

    
class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__(self)
        self.resize(585, 199)
        
        font = QtGui.QFont()
        font.setPointSize(12)
        self.keepGoing = True
        self.enterLabel = myLabel(self, "Enter Keyword or name:", font, 20, 10, 181, 31)
        self.enterLabel.alignCenter()
        
        self.enterName = QTextEdit(self)
        self.enterName.setGeometry(220, 10, 341, 31)

        self.dirLabel = myLabel(self, "Enter Directory:", font, 20, 60, 181, 31)
        self.dirValue =QTextEdit(self)
        self.dirValue.setGeometry(220, 60, 341, 31)

        self.progressLabel = myLabel(self, "Progess:", font, 20, 285, 71, 31)

        self.resultsLabel = myLabel(self, "Results Found:", font, 350, 290, 121, 31)
        self.amountThrough = myLabel(self, "Amount Scanned:", font, 350, 330, 121, 31)
        self.searchStatusLabel = myLabel(self, "Search Status", font, 80, 240, 401, 31)
        self.searchStatusLabel.alignCenter()
        self.timeLapsedNum = myLabel(self, "0", font, 140, 360, 201, 31)

        self.timeLapsedLabel = myLabel(self, "Time Lapsed:", font, 20, 360, 101, 31)
        font.setPointSize(10)
        self.resultsValue = myLabel(self, "0", font, 480, 290, 101, 31)
        self.scannedValue = myLabel(self, "0", font, 480, 330, 101, 31)

        font.setPointSize(11)

        self.fileCheck = QCheckBox(self)
        self.fileCheck.setText("File")
        self.fileCheck.setGeometry(190, 110, 51, 17)
        self.fileCheck.setFont(font)

        self.folderCheck = QCheckBox(self)
        self.folderCheck.setText("Folder")
        self.folderCheck.setGeometry(350, 110, 70, 17)
        self.folderCheck.setFont(font)

        self.notShow = QCheckBox(self)
        self.notShow.setText("Not show")
        self.notShow.setGeometry(480, 110, 70, 17)

        self.search = myButton(self, "Search", 480, 160, 81, 31)
        self.enterName.setText("report")
        self.dirValue.setText("C:\\Users\\noure\\Documents")
        self.search.clicked.connect(self.getInfo)
        self.cancel = myButton(self, "Cancel", 480, 400, 81, 31)
        self.cancel.clicked.connect(self.cancelOp)

        self.showProgress = progressBar(self, 100, 0, 150, 290, 118, 23)
        self.infoShow = ShowFileInfo()

    def getInfo(self):
        self.fileNum = 1
        self.folderNum = 1
        self.keywords = self.enterName.toPlainText()
        self.keepGoing = True
        self.keywords = self.keywords.split(",")
        self.directory = self.dirValue.toPlainText().strip()
        self.chooseDisable()
        self.infoShow.endTask()

        if self.notShow.isChecked():
            self.enterName.setText("")
        app.processEvents()
        
        self.startIt()


    def chooseDisable(self, disabled=True):
        if disabled:
            self.resize(585, 442)
            self.search.setDisabled(True)
            self.fileCheck.setDisabled(True)
            self.folderCheck.setDisabled(True)
            self.dirValue.setDisabled(True)
            self.enterName.setDisabled(True)
            self.cancel.setEnabled(True)
            
        else:
            self.search.setEnabled(True)
            self.fileCheck.setEnabled(True)
            self.folderCheck.setEnabled(True)
            self.dirValue.setEnabled(True)
            self.enterName.setEnabled(True)
            self.cancel.setDisabled(True)

        
    def cancelOp(self):
        self.keepGoing = False

    def is_junction(self, path: str) -> bool:
        try:
            return bool(os.readlink(path))
        except OSError:
            return False


    def startIt(self):
        self.results = 0
        self.scanned = 0
        self.folderDir = []
        self.amount = 0

        for dir in os.listdir(self.directory):
            a = self.directory + "\\" + dir
            if os.path.isdir(a) and not self.is_junction(a):
                try:
                    os.listdir(a)
                    self.folderDir.append(dir)
                except PermissionError:
                    print("Permission Error")
       

        self.amount = len(self.folderDir)+1

        self.showProgress.setMaximum(self.amount)
        self.resultsValue.changeText(self.results)
        self.showProgress.setValue(0)
        app.processEvents()
        self.amount = 0

        time1 = time.time()
        self.findIt()
        time2 = time.time()
        print("MyProj2: " + str(time2-time1))

    def findIt(self):
        
        if self.fileCheck.isChecked():
            fileInfo = open("fileInfo.txt", "w")

        if self.folderCheck.isChecked():
            folderInfo = open("folderInfo.txt", "w")

        time1 = time.time()
        try:
            for path_2, folders, files in os.walk(self.directory):
                if self.keepGoing:
                    if self.fileCheck.isChecked():  
                        for file in files:
                            lowerFile = file.lower().strip()
                            for word in self.keywords:
                                word = word.strip().lower()
                                if word in lowerFile:
                                    # self.searchFiles(path_2, file, files, folders)
                                    self.writeFiles(path_2, file, files, folders, fileInfo)
                                    self.results += 1
                            


                    
                    if self.folderCheck.isChecked():
                        for folder in folders:
                            lowerFol = folder.lower()
                            for word in self.keywords:
                                word = word.strip().lower()
                                if word in lowerFol:
                                    # self.searchFolders(path_2, folder, files, folders, folderInfo)
                                    self.writingFolders(path_2, folder, files, folders, folderInfo)
                                    self.results += 1
                    self.scanned += 1
                                    
                else:
                    break
            
                
                for di in self.folderDir:
                    if self.directory[-1] == "\\":
                        if path_2 == (self.directory + di):
                            self.amount += 1
                    else:
                        if path_2 == (self.directory +  "\\" + di):
                            self.amount += 1
                    
                self.timeLapsedNum.changeText(round(time.time() - time1, 2))
                self.resultsValue.changeText(self.results)
                self.scannedValue.changeText(self.scanned)
                self.showProgress.setValue(self.amount)
                app.processEvents()
        except Exception as e:
            print("FindIt: " + str(e))

        self.amount += 1
        self.showProgress.setValue(self.amount)
        app.processEvents()
        # self.infoShow.show()
        
        if self.fileCheck.isChecked():
            fileInfo.close()

        if self.folderCheck.isChecked():
            folderInfo.close()

        

        self.chooseDisable(False)

    def searchFolders(self, thePath, cFolder, files, folders):
        try:
            info1 = []
            realSize = 0
            info1.append(thePath +"\n")
            info1.append("Folder Name: {}\n".format(cFolder))
            info1.append("Files: {}\n".format(files))
            info1.append("Folders: {}\n".format(folders))

            for p, fol, fil in os.walk(thePath +"\\"+ cFolder):
                for fileSize in fil:
                    realSize += path.getsize(p+"\\"+fileSize)

            info1.append("Size: {}KB\n\n".format(realSize/1000))

            self.infoShow.addResults(info1)
        except:
            print(error)


    def writeFiles(self, thePath, cFile, files, folders, writing):
        
        try:
            writing.write("Result: {}\n".format(self.fileNum))
            writing.write(thePath + "\n")
            writing.write("filename: {}\n".format(cFile))
            writing.write("Files: {}\n".format(files))
            writing.write("Folders: {}\n".format(folders))
            writing.write("Size: {}KB\n\n".format(path.getsize(thePath +"\\"+ cFile)/1000))
        except Exception as e:
            print("Write Files: " + str(e))
        self.fileNum += 1

    
    def writingFolders(self, thePath, cFolder, files, folders, writing):
        
        try:
            realSize = 0
            writing.write("Result: {}\n".format(self.folderNum))
            writing.write(thePath +"\n")
            writing.write("Folder Name: {}\n".format(cFolder))
            writing.write("Files: {}\n".format(files))
            writing.write("Folders: {}\n".format(folders))

            for p, fol, fil in os.walk(thePath +"\\"+ cFolder):
                for fileSize in fil:
                    realSize += path.getsize(p+"\\"+fileSize)

            writing.write("Size: {}KB\n\n".format(realSize/1000))

        except Exception as e:
            print("Writing Folders: " + str(e))

        self.folderNum += 1



    def searchFiles(self, thePath, cFile, files, folders):
        try:
            info1 = []
            info1.append(thePath)
            info1.append("filename: {}".format(cFile))
            info1.append("Files: {}".format(files))
            info1.append("Folders: {}".format(folders))
            info1.append("Size: {}KB\n\n".format(path.getsize(thePath +"\\"+ cFile)/1000))

            self.infoShow.addResults(info1)
        except:
            print(error)





app = QApplication(sys.argv)
win = MyWindow()
win.show()
sys.exit(app.exit())