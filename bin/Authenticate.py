from PyQt5 import QtCore, QtGui, QtWidgets;
import sys;
import os;
import socket;
import json;
sys.path.insert(1,os.path.join(os.path.expanduser('~'),'odrive-x'));
from gui.Gui import Gui;
from gui.AuthenticateGui import AuthenticateGui;
from Odrivex import Odrivex;
class Authenticate():
    def ui(self):
        self.obj_QMainWindow__ui=QtWidgets.QMainWindow();
        Gui.centering(self.obj_QMainWindow__ui);
        self.obj_AuthenticateGui=AuthenticateGui();
        self.obj_AuthenticateGui.setupUi(self.obj_QMainWindow__ui);
        self.obj_QMainWindow__ui.show();
        self.obj_AuthenticateGui.btn_authenticate.clicked.connect(self.authenticate);
    def authenticate(self):
        authkey=self.obj_AuthenticateGui.authkey.text();
        socket_odriveagent=Odrivex.tether();
        socket_odriveagent.sendall((json.dumps({'command':'authenticate','parameters':{'authKey':authkey}})+'\n').encode('utf-8'));
        response_odriveagent=Odrivex.receive(socket_odriveagent);
        socket_odriveagent.close();
        if (response_odriveagent['messageType']=='Status'):
            success=QtWidgets.QMessageBox();
            success.setWindowTitle("Welcome");
            name=str(response_odriveagent['message']).replace("Hello","");
            success.setText(name);
            success.exec_();
            self.obj_AuthenticateGui.btn_authenticate.setEnabled(False);
            self.obj_AuthenticateGui.authkey.setEnabled(False);
            socket_odriveagent=Odrivex.tether();
            socket_odriveagent.sendall((json.dumps({'command':'status','parameters':{}})+'\n').encode('utf-8'));
            response_odriveagent=Odrivex.receive(socket_odriveagent);
            socket_odriveagent.close();
            message=response_odriveagent['message'];
            email=message['authorizedEmail'];
            accountType=message['authorizedAccountSourceType']
            self.obj_AuthenticateGui.name.setText("Name: "+name);
            self.obj_AuthenticateGui.name.adjustSize();
            self.obj_AuthenticateGui.email.setText("Email: "+email);
            self.obj_AuthenticateGui.email.adjustSize();
            self.obj_AuthenticateGui.ac.setText("Account Type: "+accountType);
            self.obj_AuthenticateGui.ac.adjustSize();
            user_info={"name":name,"email":email,"accountType":accountType};
            with open(os.path.join(os.path.expanduser('~'),'.odrive-x')+'_user_info.json','w') as user_info_f:
                json.dump(user_info,user_info_f,indent=None);
        if (response_odriveagent['messageType']=='Error'):
            error=QtWidgets.QMessageBox();
            error.setWindowTitle("Error");
            error.setText(response_odriveagent['message']);
            error.exec_();
if __name__=="__main__":
    obj_QApplication=QtWidgets.QApplication(sys.argv)
    obj_Authenticate=Authenticate();
    obj_Authenticate.ui();
    sys.exit(obj_QApplication.exec_())
