from PyQt5 import QtCore, QtGui, QtWidgets;
from PyQt5.QtWidgets import QFileDialog;
import sys;
import os;
import socket;
import json;
ODRIVEX_FILES_PATH=os.path.join(os.path.expanduser('~'),'odrive-x');
sys.path.insert(1,ODRIVEX_FILES_PATH);
from bin.Odrivex import Odrivex, ODRIVEX_APPDATA_PATH;
from gui.MountGui import MountGui;
from gui.NavigatorGui import NavigatorGui;
from gui.Gui import Gui;
class Mount():
    def setupUi(self):
        self.obj_MountGui=MountGui();
        self.obj_NavigatorGui=NavigatorGui();
        self.obj_QMainWindow__setupUi=QtWidgets.QMainWindow();
        self.obj_MountGui.setupUi(self.obj_QMainWindow__setupUi);
        Gui.centering(self.obj_QMainWindow__setupUi);
        self.obj_QMainWindow__setupUi.show();
        self.obj_QMainWindow__navigate=QtWidgets.QMainWindow();
        self.obj_NavigatorGui.setupUi(self.obj_QMainWindow__navigate);
        Gui.centering(self.obj_QMainWindow__navigate);
        self.obj_MountGui.btn_local.clicked.connect(self.local);
        self.obj_MountGui.btn_cloud.clicked.connect(self.obj_QMainWindow__navigate.show);
        self.obj_MountGui.btn_mount.clicked.connect(self.mount);
        self.obj_NavigatorGui.web.loadProgress.connect(self.statusLoading);
        self.obj_NavigatorGui.web.loadFinished.connect(self.statusDone);
        self.obj_NavigatorGui.pushButton.clicked.connect(self.extract);
    def extract(self):
        url=str(self.obj_NavigatorGui.web.url());
        url=(url.replace(url[:19],"")).rstrip("')")
        valPath="";
        for i in range(30):
            valPath=valPath+(url[i]);
        if(valPath!="https://www.odrive.com/browse/"):
            error=QtWidgets.QMessageBox();
            error.setWindowTitle("Error");
            error.setText("Invalid path");
            error.exec_();
        else:
            self.remoteDir=(url.replace(valPath,"")).replace("+"," ").strip();
            self.obj_MountGui.remote_path.setText("/"+str(self.remoteDir));
            self.obj_QMainWindow__navigate.close();
    def statusLoading(self):
        self.obj_NavigatorGui.statusBar.showMessage("Loading...");
    def statusDone(self):
        self.obj_NavigatorGui.statusBar.showMessage("Done",1000);
    def local(self):
        self.localDir=QFileDialog.getExistingDirectory(None, 'Select a directory',"/home");
        self.obj_MountGui.local_path.setText(self.localDir);
    def mount(self):
        self.remoteDir=str(self.obj_MountGui.remote_path.text());
        socketOdriveagent=Odrivex.tether();
        socketOdriveagent.sendall((json.dumps({'command':'mount','parameters':{'localPath':self.localDir,'remotePath':self.remoteDir}})+'\n').encode('utf-8'));
        responseOdriveagent=Odrivex.receive(socketOdriveagent);
        socketOdriveagent.close();
        if (responseOdriveagent['messageType']=='Status'):
            Odrivex.showMessage(responseOdriveagent['message']);
            self.obj_QMainWindow__setupUi.close();
            FILE_DOES_NOT_EXIST=False;
            if(not(os.path.isfile(ODRIVEX_APPDATA_PATH+'/'+'mount'))):
                mount={
                        "1":
                            {"localPath":
                                        self.localDir,
                            "remotePath":
                                        self.remoteDir}
                    };
                FILE_DOES_NOT_EXIST=True;
            else:
                mount={
                        "localPath":
                                    self.localDir,
                        "remotePath":
                                    self.remoteDir
                    };
            if(FILE_DOES_NOT_EXIST):
                with open(ODRIVEX_APPDATA_PATH+'/mount','w') as mount_f:
                    json.dump(mount,mount_f,indent=None);
            else:
                with open(ODRIVEX_APPDATA_PATH+'/mount','r') as mount_f:
                    directories=json.loads(mount_f.read());
                directoriesList=[];
                for i in range(len(directories)):
                    directoriesList.append(directories[str(i+1)]);
                directoriesList.append(mount);
                directories={};
                for i in range(len(directoriesList)):
                    directories[str(i+1)]=directoriesList[i];
                with open(ODRIVEX_APPDATA_PATH+'/mount','w') as mount_f:
                    json.dump(directories,mount_f,indent=None);
        if (responseOdriveagent['messageType']=='Error'):
            Odrivex.showError(responseOdriveagent['message']);
if __name__ == "__main__":
    obj_QApplication=QtWidgets.QApplication(sys.argv);
    obj_Mount=Mount();
    obj_Mount.setupUi();
    sys.exit(obj_QApplication.exec_());
