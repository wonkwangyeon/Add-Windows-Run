import sys
import time
from PyQt5.QtWidgets import *
from run.Run import Run
from lib.logger import Logger


class AddWindowsRun(QWidget):
    logger = Logger("AddWindowsRun")

    def __init__(self):
        super().__init__()
        self.windowsRun = Run()
        self.initUI()
        self.logger.info("Start Run Add Windows Run") 

    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)

        self.labelRunName = QLabel(self)
        self.labelRunName.setText("Run Name : ")

        self.runNameEdit = QLineEdit()
        grid.addWidget(self.labelRunName, 0, 0)
        grid.addWidget(self.runNameEdit, 0, 1, 1,4)

        self.labelRunPath = QLabel(self)
        self.labelRunPath.setText("Run File Path : ")

        self.runPathEdit = QLineEdit()
        grid.addWidget(self.labelRunPath, 1, 0)
        grid.addWidget(self.runPathEdit, 1, 1, 1,4)

        self.labelRunExe = QLabel(self)
        self.labelRunExe.setText("Run File.exe : ")

        self.runExeEdit = QLineEdit()
        grid.addWidget(self.labelRunExe, 2, 0)
        grid.addWidget(self.runExeEdit, 2, 1, 1,4)

        btnAdd = QPushButton('ADD')
        btnAdd.clicked.connect(self.btnAdd_clicked)

        btnDelete = QPushButton('DELETE')
        btnDelete.clicked.connect(self.btnDelete_clicked)
        grid.addWidget(btnDelete, 3, 3)
        grid.addWidget(btnAdd, 3, 4)

        self.tableWidget = QTableWidget()        
        self.tableWidget.setColumnCount(4)
        columnHeaders = ['ID', 'Run Name', 'Run File Path', 'Run File.exe']                
        self.tableWidget.setHorizontalHeaderLabels(columnHeaders)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)        
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        grid.addWidget(self.tableWidget, 4, 0, 1, 5)

        self.setWindowTitle('Add Windows Run')
        self.resize(600, 450)
        self.center()
        self.table_setting()
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def table_setting(self):
        runList=self.windowsRun.get_all_run_list()    

        if runList is None:
            self.tableWidget.setRowCount(0)
        else:
            self.tableWidget.setRowCount(len(runList))

            for idx, list in enumerate(runList):            
                self.tableWidget.setItem(idx, 0, QTableWidgetItem(str(list[0])))
                self.tableWidget.setItem(idx, 1, QTableWidgetItem(list[1]))
                self.tableWidget.setItem(idx, 2, QTableWidgetItem(list[2]))
                self.tableWidget.setItem(idx, 3, QTableWidgetItem(list[3]))
  
    def btnAdd_clicked(self):        
        result = self.windowsRun.add_run_file(self.runNameEdit.text(), self.runPathEdit.text(), self.runExeEdit.text())
        if result == 1:            
            rowCount = self.tableWidget.rowCount()
            self.tableWidget.setRowCount(rowCount+1)
            lastRunId = self.windowsRun.get_last_run_id()
            if lastRunId != -1:
                self.tableWidget.setItem(rowCount, 0, QTableWidgetItem(str(lastRunId)))
                self.tableWidget.setItem(rowCount, 1, QTableWidgetItem(self.runNameEdit.text()))
                self.tableWidget.setItem(rowCount, 2, QTableWidgetItem(self.runPathEdit.text()))
                self.tableWidget.setItem(rowCount, 3, QTableWidgetItem(self.runExeEdit.text()))
                self.runNameEdit.clear()
                self.runPathEdit.clear()
                self.runExeEdit.clear()
                QMessageBox.question(self, 'Message', '실행 레지스트리에 추가되었습니다.',
                                        QMessageBox.Yes)
            else:
                QMessageBox.question(self, 'Message', result,
                                    QMessageBox.Yes)
        else:
             QMessageBox.question(self, 'Message', result,
                                    QMessageBox.Yes)

    def btnDelete_clicked(self): 
        currentRow = self.tableWidget.currentRow()
        if currentRow != -1:
            runId = self.tableWidget.item(currentRow, 0).text()
            runName = self.tableWidget.item(currentRow, 1).text()
            runPath = self.tableWidget.item(currentRow, 2).text()
            runExe = self.tableWidget.item(currentRow, 3).text()
            result = self.windowsRun.delete_run(runId, runName, runExe, runPath)
            if result == 1:
                self.tableWidget.removeRow(self.tableWidget.currentRow())
                QMessageBox.question(self, 'Message', '삭제되었습니다.',
                                    QMessageBox.Yes) 
            else:
                QMessageBox.question(self, 'Message', result,
                                    QMessageBox.Yes)
        else :
            QMessageBox.question(self, 'Message', '행을 선택해주세요.',
                                    QMessageBox.Yes)            
           

if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = AddWindowsRun()
   sys.exit(app.exec_())