from PyQt5 import QtCore, QtGui, QtWidgets;
from PyQt5.QtCore import QUrl
import sys;
import os;
sys.path.insert(1, "/home/ubuntu/odrive-x");
from gui.NavigatorGui import NavigatorGui;
class Navigator():
    def centering(self,arg_window):
        window=arg_window.frameGeometry();
        center=QtWidgets.QDesktopWidget().availableGeometry().center();
        window.moveCenter(center);
        arg_window.move(window.topLeft());
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
        url=str(self.obj_NavigatorGui.web.url());
        self.obj_QMainWindow__navigate.close();
    def statusLoading(self):
        self.obj_NavigatorGui.statusBar.showMessage("Loading...");
    def statusDone(self):
        self.obj_NavigatorGui.statusBar.showMessage("Done",1000);
if __name__ == "__main__":
    obj_QApplication=QtWidgets.QApplication(sys.argv);
    obj_Navigator=Navigator();
    obj_Navigator.navigate();
    sys.exit(obj_QApplication.exec_());
