from PyQt5 import QtCore, QtGui, QtWidgets;
import sys;
import os;
sys.path.insert(1, "/home/ubuntu/odrive-x")
from gui.AuthenticateGui import AuthenticateGui;
class Authenticate():
    def centering(self,arg_window):
        window=arg_window.frameGeometry();
        center=QtWidgets.QDesktopWidget().availableGeometry().center();
        window.moveCenter(center);
        arg_window.move(window.topLeft());
    def validate(self):
        self.obj_QMainWindow__validate=QtWidgets.QMainWindow();
        self.centering(self.obj_QMainWindow__validate);
        self.obj_AuthenticateGui=AuthenticateGui();
        self.obj_AuthenticateGui.setupUi(self.obj_QMainWindow__validate);
        self.obj_QMainWindow__validate.show();
        self.obj_AuthenticateGui.btn_verify.clicked.connect(self.authenticate);
    def authenticate(self):
        authkey=self.obj_AuthenticateGui.authkey.text();
        os.makedirs("/home/ubuntu/.odrive-x", exist_ok=True);
        os.system("sudo odrive authenticate "+authkey+" 2>&1 |tee /home/ubuntu/.odrive-x/prompt.txt");
        with open("/home/ubuntu/.odrive-x/prompt.txt") as prompt_f:
            if(prompt_f.read(5)=="Hello"):
                success=QtWidgets.QMessageBox();
                success.setWindowTitle("Welcome");
                name=prompt_f.readline().rstrip("\n");
                success.setText(name);
                success.exec_();
                self.obj_AuthenticateGui.btn_verify.setEnabled(False);
                self.obj_AuthenticateGui.authkey.setEnabled(False);
                self.obj_AuthenticateGui.name.setText("Name: "+name);
                self.obj_AuthenticateGui.name.adjustSize();
                os.system("sudo odrive status 2>&1 |tee /home/ubuntu/.odrive-x/status.txt");
                with open("/home/ubuntu/.odrive-x/status.txt") as status_f:
                    text=status_f.readlines();
                    info=str(text[3].split("\n")).split(" ");
                    email=info[1];
                    accountType=info[-2].rstrip("',");
                    self.obj_AuthenticateGui.email.setText("Email: "+email);
                    self.obj_AuthenticateGui.email.adjustSize();
                    self.obj_AuthenticateGui.ac.setText("Account Type: "+accountType);
                    self.obj_AuthenticateGui.ac.adjustSize();
            else:
                prompt_f.seek(0);
                error=QtWidgets.QMessageBox();
                error.setWindowTitle("Error");
                error.setText(prompt_f.readline().rstrip("\n"));
                error.exec_();
if __name__ == "__main__":
    obj_QApplication=QtWidgets.QApplication(sys.argv)
    obj_Authenticate=Authenticate();
    obj_Authenticate.validate();
    sys.exit(obj_QApplication.exec_())
