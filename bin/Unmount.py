from PyQt5 import QtCore, QtGui, QtWidgets;
from PyQt5.QtWidgets import QFileDialog;
import sys;
import os;
sys.path.insert(1, "/home/ubuntu/odrive-x")
from gui.UnmountGui import UnmountGui;
class Unmount():
    def centering(self,arg_window):
        window=arg_window.frameGeometry();
        center=QtWidgets.QDesktopWidget().availableGeometry().center();
        window.moveCenter(center);
        arg_window.move(window.topLeft());
    def ui(self):
        self.obj_QMainWindow__ui=QtWidgets.QMainWindow();
        self.centering(self.obj_QMainWindow__ui);
        self.obj_UnmountGui=UnmountGui();
        self.obj_UnmountGui.setupUi(self.obj_QMainWindow__ui);
        self.obj_QMainWindow__ui.show();
        self.obj_UnmountGui.btn_local.clicked.connect(self.local);
        self.obj_UnmountGui.btn_unmount.clicked.connect(self.unmount);
    def local(self):
        self.local_dir=QFileDialog.getExistingDirectory(None, 'Select a directory',"/home");
        self.obj_UnmountGui.local_path.setText(self.local_dir);
    def unmount(self):
        os.system("sudo odrive unmount "+self.local_dir+" 2>&1 |tee /home/ubuntu/.odrive-x/unmount.txt");
        with open("/home/ubuntu/.odrive-x/unmount.txt") as unmount_f:
            info=QtWidgets.QMessageBox();
            info.setWindowTitle("odrive-x");
            alert=unmount_f.readline().rstrip("\n");
            info.setText(alert);
            info.exec_();
if __name__ == "__main__":
    obj_QApplication=QtWidgets.QApplication(sys.argv)
    obj_Mount=Unmount();
    obj_Mount.ui();
    sys.exit(obj_QApplication.exec_())
