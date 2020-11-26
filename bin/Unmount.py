from PyQt5 import QtCore, QtGui, QtWidgets;
import sys;
import os;
import socket;
import json;
ODRIVEX_FILES_PATH=os.path.join(os.path.expanduser('~'),'odrive-x');
sys.path.insert(1,ODRIVEX_FILES_PATH);
from bin.Odrivex import Odrivex, ODRIVEX_APPDATA_PATH;
from gui.Gui import Gui;
from gui.UnmountGui import UnmountGui;
class Unmount():
    def setupUi(self):
        self.obj_UnmountGui=UnmountGui();
        self.obj_QMainWindow__setupUi=QtWidgets.QMainWindow();
        self.obj_UnmountGui.setupUi(self.obj_QMainWindow__setupUi);
        Gui.centering(self.obj_QMainWindow__setupUi);
        self.getPath();
        self.obj_QMainWindow__setupUi.show();
        self.obj_UnmountGui.pushButton.clicked.connect(self.unmount);
    def getPath(self):
        isFile=os.path.isfile(ODRIVEX_APPDATA_PATH+'/mount');
        if(isFile):
            with open(ODRIVEX_APPDATA_PATH+'/mount','r') as mount_f:
                self.directories=json.loads(mount_f.read());
            for i in range(len(self.directories)):
                self.obj_UnmountGui.comboBox.addItem(str(i+1)+". "+str(self.directories[str(i+1)]['localPath']));
    def unmount(self):
        currentText=self.obj_UnmountGui.comboBox.currentText();
        localPath=currentText[currentText.index(".")+1:].strip();
        index=currentText.replace(localPath,"").replace(".","").strip();
        socketOdriveagent=Odrivex.tether();
        socketOdriveagent.sendall((json.dumps({'command':'unmount','parameters':{'localPath':localPath}})+'\n').encode('utf-8'));
        responseOdriveagent=Odrivex.receive(socketOdriveagent);
        socketOdriveagent.close();
        if (responseOdriveagent['messageType']=='Status'):
            Odrivex.showMessage(responseOdriveagent['message']);
            self.obj_QMainWindow__setupUi.close();
            directoriesList=[];
            for i in range(len(self.directories)):
                directoriesList.append(self.directories[str(i+1)]);
            directoriesList.remove(self.directories[index]);
            self.directories={};
            for i in range(len(directoriesList)):
                self.directories[str(i+1)]=directoriesList[i];
            with open(ODRIVEX_APPDATA_PATH+'/mount','w') as mount_f:
                json.dump(self.directories,mount_f,indent=None);
        if (responseOdriveagent['messageType']=='Error'):
            Odrivex.showError(responseOdriveagent['message']);
if __name__ == "__main__":
    obj_QApplication=QtWidgets.QApplication(sys.argv);
    obj_Mount=Unmount();
    obj_Mount.setupUi();
    sys.exit(obj_QApplication.exec_());
