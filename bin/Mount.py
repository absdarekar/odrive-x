from PyQt5 import QtCore, QtGui, QtWidgets;
from PyQt5.QtWidgets import QFileDialog;
import sys;
import os;
sys.path.insert(1, "/home/ubuntu/odrive-x")
from gui.MountGui import MountGui;
class Mount():
    def centering(self,arg_window):
        window=arg_window.frameGeometry();
        center=QtWidgets.QDesktopWidget().availableGeometry().center();
        window.moveCenter(center);
        arg_window.move(window.topLeft());
    def ui(self):
        self.obj_QMainWindow__mount=QtWidgets.QMainWindow();
        self.centering(self.obj_QMainWindow__mount);
        self.obj_MountGui=MountGui();
        self.obj_MountGui.setupUi(self.obj_QMainWindow__mount);
        self.obj_QMainWindow__mount.show();
        self.remote_dir=self.obj_MountGui.remote_path.text();
        self.obj_MountGui.btn_local.clicked.connect(self.local);
        self.obj_MountGui.btn_cloud.clicked.connect(self.cloud);
        self.obj_MountGui.btn_mount.clicked.connect(self.mount);
    def local(self):
        self.local_dir=QFileDialog.getExistingDirectory(None, 'Select a directory',"/home");
        self.obj_MountGui.local_path.setText(self.local_dir);
    def cloud(self):
        pass;
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
