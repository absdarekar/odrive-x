from PyQt5 import QtCore, QtGui, QtWidgets;
from PyQt5.QtWidgets import QFileDialog;
import sys;
import os;
sys.path.insert(1, "/home/ubuntu/odrive-x")
from gui.MountGui import MountGui;
from gui.NavigatorGui import NavigatorGui;
class Mount():
    def centering(self,arg_window):
        window=arg_window.frameGeometry();
        center=QtWidgets.QDesktopWidget().availableGeometry().center();
        window.moveCenter(center);
        arg_window.move(window.topLeft());
    def ui(self):
        self.obj_QMainWindow__ui=QtWidgets.QMainWindow();
        self.centering(self.obj_QMainWindow__ui);
        self.obj_MountGui=MountGui();
        self.obj_MountGui.setupUi(self.obj_QMainWindow__ui);
        self.obj_QMainWindow__ui.show();
        self.obj_MountGui.btn_local.clicked.connect(self.local);
        self.obj_MountGui.btn_cloud.clicked.connect(self.navigate);
        self.obj_MountGui.btn_mount.clicked.connect(self.mount);
    def navigate(self):
        self.obj_QMainWindow__navigate=QtWidgets.QMainWindow();
        self.centering(self.obj_QMainWindow__navigate);
        self.obj_NavigatorGui=NavigatorGui();
        self.obj_NavigatorGui.setupUi(self.obj_QMainWindow__navigate);
        self.obj_QMainWindow__navigate.show();
        self.obj_NavigatorGui.web.loadProgress.connect(self.statusLoading);
        self.obj_NavigatorGui.web.loadFinished.connect(self.statusDone);
        self.obj_NavigatorGui.pushButton.clicked.connect(self.extract);
    def extract(self):
        self.remote_dir=str(self.obj_NavigatorGui.web.url());
        self.obj_MountGui.remote_path.setText(self.remote_dir);
        self.obj_QMainWindow__navigate.close();
    def statusLoading(self):
        self.obj_NavigatorGui.statusBar.showMessage("Loading...");
    def statusDone(self):
        self.obj_NavigatorGui.statusBar.showMessage("Done",1000);
    def local(self):
        self.local_dir=QFileDialog.getExistingDirectory(None, 'Select a directory',"/home");
        self.obj_MountGui.local_path.setText(self.local_dir);
    def mount(self):
        os.system("sudo odrive mount "+self.local_dir+" "+self.remote_dir+" 2>&1 |tee /home/ubuntu/.odrive-x/mount.txt");
        with open("/home/ubuntu/.odrive-x/mount.txt") as mount_f:
            info=QtWidgets.QMessageBox();
            info.setWindowTitle("odrive-x");
            alert=mount_f.readline().rstrip("\n");
            info.setText(alert);
            info.exec_();
if __name__ == "__main__":
    obj_QApplication=QtWidgets.QApplication(sys.argv)
    obj_Mount=Mount();
    obj_Mount.ui();
    sys.exit(obj_QApplication.exec_())
