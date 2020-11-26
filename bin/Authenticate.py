from PyQt5 import QtCore, QtGui, QtWidgets;
import sys;
import os;
import socket;
import json;
ODRIVEX_FILES_PATH=os.path.join(os.path.expanduser('~'),'odrive-x');
sys.path.insert(1,ODRIVEX_FILES_PATH);
from bin.Odrivex import Odrivex, ODRIVEX_APPDATA_PATH;
from gui.Gui import Gui;
from gui.AuthenticateGui import AuthenticateGui;
class Authenticate():
    def setupUi(self):
        self.obj_QMainWindow__setupUi=QtWidgets.QMainWindow();
        Gui.centering(self.obj_QMainWindow__setupUi);
        self.obj_AuthenticateGui=AuthenticateGui();
        self.obj_AuthenticateGui.setupUi(self.obj_QMainWindow__setupUi);
        self.obj_QMainWindow__setupUi.show();
        self.obj_AuthenticateGui.btn_authenticate.clicked.connect(self.authenticate);
    def authenticate(self):
        authkey=self.obj_AuthenticateGui.authkey.text();
        socketOdriveagent=Odrivex.tether();
        socketOdriveagent.sendall((json.dumps({'command':'authenticate','parameters':{'authKey':authkey}})+'\n').encode('utf-8'));
        responseOdriveagent=Odrivex.receive(socketOdriveagent);
        socketOdriveagent.close();
        if (responseOdriveagent['messageType']=='Status'):
            success=QtWidgets.QMessageBox();
            success.setWindowTitle("Welcome");
            name=str(responseOdriveagent['message']).replace("Hello","");
            success.setText(name);
            success.exec_();
            self.obj_AuthenticateGui.btn_authenticate.setEnabled(False);
            self.obj_AuthenticateGui.authkey.setEnabled(False);
            socketOdriveagent=Odrivex.tether();
            socketOdriveagent.sendall((json.dumps({'command':'status','parameters':{}})+'\n').encode('utf-8'));
            responseOdriveagent=Odrivex.receive(socketOdriveagent);
            socketOdriveagent.close();
            message=responseOdriveagent['message'];
            email=message['authorizedEmail'];
            accountType=message['authorizedAccountSourceType']
            self.obj_AuthenticateGui.name.setText("Name: "+name);
            self.obj_AuthenticateGui.name.adjustSize();
            self.obj_AuthenticateGui.email.setText("Email: "+email);
            self.obj_AuthenticateGui.email.adjustSize();
            self.obj_AuthenticateGui.ac.setText("Account Type: "+accountType);
            self.obj_AuthenticateGui.ac.adjustSize();
            userInfo={
                        "name":
                                name,
                        "email":
                                email,
                        "accountType":
                                    accountType
                    };
            with open(ODRIVEX_APPDATA_PATH+'/user_info','w') as user_info_f:
                json.dump(userInfo,user_info_f,indent=None);
        if (responseOdriveagent['messageType']=='Error'):
            Odrivex.showError(responseOdriveagent['message']);
if __name__=="__main__":
    obj_QApplication=QtWidgets.QApplication(sys.argv);
    obj_Authenticate=Authenticate();
    obj_Authenticate.setupUi();
    sys.exit(obj_QApplication.exec_());
