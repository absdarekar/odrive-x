from PyQt5 import QtCore, QtGui, QtWidgets;
from PyQt5.QtWidgets import QFileDialog;
import sys;
import os;
import socket;
import json;
sys.path.insert(1,os.path.join(os.path.expanduser('~'),'odrive-x'));
from gui.MountGui import MountGui;
from gui.NavigatorGui import NavigatorGui;
from gui.Gui import Gui;
from Odrivex import Odrivex;
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
            self.remote_dir=(url.replace(valPath,"")).replace("+","\ ");
            self.obj_MountGui.remote_path.setText(self.remote_dir);
            self.obj_QMainWindow__navigate.close();
    def statusLoading(self):
        self.obj_NavigatorGui.statusBar.showMessage("Loading...");
    def statusDone(self):
        self.obj_NavigatorGui.statusBar.showMessage("Done",1000);
    def local(self):
        self.remote_dir="/"
        self.local_dir=QFileDialog.getExistingDirectory(None, 'Select a directory',"/home");
        self.obj_MountGui.local_path.setText(self.local_dir);
    def mount(self):
        socket_odriveagent=Odrivex.tether();
        socket_odriveagent.sendall((json.dumps({'command':'mount','parameters':{'localPath':self.local_dir,'remotePath':self.remote_dir}})+'\n').encode('utf-8'));
        response_odriveagent=Odrivex.receive(socket_odriveagent);
        socket_odriveagent.close();
        if (response_odriveagent['messageType']=='Status'):
            success=QtWidgets.QMessageBox();
            success.setWindowTitle("Alert");
            success.setText(response_odriveagent['message']);
            success.exec_();
            mount={"localPath":self.local_dir,"remotePath":self.remote_dir};
            with open(os.path.join(os.path.expanduser('~'),'.odrive-x')+'/'+'mount','w') as mount_f:
                json.dump(mount,mount_f,indent=None);
            self.obj_QMainWindow__setupUi.close();
        if (response_odriveagent['messageType']=='Error'):
            error=QtWidgets.QMessageBox();
            error.setWindowTitle("Error");
            error.setText(response_odriveagent['message']);
            error.exec_();
if __name__ == "__main__":
    obj_QApplication=QtWidgets.QApplication(sys.argv)
    obj_Mount=Mount();
    obj_Mount.setupUi();
    sys.exit(obj_QApplication.exec_())
