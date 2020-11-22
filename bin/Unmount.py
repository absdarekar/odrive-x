from PyQt5 import QtCore, QtGui, QtWidgets;
import sys;
import os;
import socket;
import json;
sys.path.insert(1,os.path.join(os.path.expanduser('~'),'odrive-x'));
from gui.Gui import Gui;
from gui.UnmountGui import UnmountGui;
from Odrivex import Odrivex;
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
        with open(os.path.join(os.path.expanduser('~'),'.odrive-x')+'/'+'mount','r') as mount_f:
            dirs=json.loads(mount_f.read());
        self.local_dir=dirs['localPath'];
        self.obj_UnmountGui.comboBox.addItem(self.local_dir);
    def unmount(self):
        socket_odriveagent=Odrivex.tether();
        socket_odriveagent.sendall((json.dumps({'command':'unmount','parameters':{'localPath':self.local_dir}})+'\n').encode('utf-8'));
        response_odriveagent=Odrivex.receive(socket_odriveagent);
        socket_odriveagent.close();
        if (response_odriveagent['messageType']=='Status'):
            success=QtWidgets.QMessageBox();
            success.setWindowTitle("Alert");
            success.setText(response_odriveagent['message']);
            success.exec_();
            self.obj_QMainWindow__setupUi.close();
        if (response_odriveagent['messageType']=='Error'):
            error=QtWidgets.QMessageBox();
            error.setWindowTitle("Error");
            error.setText(response_odriveagent['message']);
            error.exec_();
if __name__ == "__main__":
    obj_QApplication=QtWidgets.QApplication(sys.argv)
    obj_Mount=Unmount();
    obj_Mount.setupUi();
    sys.exit(obj_QApplication.exec_())
