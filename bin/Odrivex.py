from PyQt5 import QtCore, QtGui, QtWidgets;
import sys;
import os;
import socket;
import json;
ODRIVEX_FILES_PATH=os.path.join(os.path.expanduser('~'),'odrive-x');
sys.path.insert(1,ODRIVEX_FILES_PATH);
ODRIVEX_APPDATA_PATH=os.path.join(os.path.expanduser('~'),'.odrive-x');
os.makedirs(ODRIVEX_APPDATA_PATH, exist_ok=True);
AGENT_PORT_REGISTRY_FILE_PATH=os.path.join(os.path.expanduser('~'),'.odrive-agent','.oreg');
class Odrivex():
    def tether():
        with open(AGENT_PORT_REGISTRY_FILE_PATH, 'r') as oreg_f:
            data=json.loads(oreg_f.read());
            port=data["current"]["protocol"];
        socketOdriveagent=socket.socket(socket.AF_INET, socket.SOCK_STREAM);
        socketOdriveagent.connect(('127.0.0.1', port));
        return socketOdriveagent;
    def receive(socketOdriveagent):
        data=True;
        buffer='';
        while data:
            data=socketOdriveagent.recv(1024*1024);
            buffer+=data.decode('utf-8');
            while buffer.find('\n') != -1:
                responseOdriveagent, buffer= buffer.split('\n', 1);
                jsonresponseOdriveagent = json.loads(responseOdriveagent);
        return jsonresponseOdriveagent;
    def showError(message):
        error=QtWidgets.QMessageBox();
        error.setWindowTitle("Error");
        error.setText(message);
        error.exec_();
    def showMessage(message):
        success=QtWidgets.QMessageBox();
        success.setWindowTitle("Alert");
        success.setText(message);
        success.exec_();
