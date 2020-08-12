# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'auth.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class AuthenticateGui(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(552, 300)
        MainWindow.setMinimumSize(QtCore.QSize(550, 300))
        MainWindow.setMaximumSize(QtCore.QSize(552, 300))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(12)
        MainWindow.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("/home/ubuntu/odrive-x/icon/odrive.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame_1 = QtWidgets.QFrame(self.groupBox)
        self.frame_1.setMaximumSize(QtCore.QSize(16777215, 200))
        self.frame_1.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_1.setObjectName("frame_1")
        self.gridLayout = QtWidgets.QGridLayout(self.frame_1)
        self.gridLayout.setObjectName("gridLayout")
        self.btn_verify = QtWidgets.QPushButton(self.frame_1)
        self.btn_verify.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("/home/ubuntu/odrive-x/icon/verified-account.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_verify.setIcon(icon1)
        self.btn_verify.setIconSize(QtCore.QSize(20, 20))
        self.btn_verify.setObjectName("pushButton")
        self.gridLayout.addWidget(self.btn_verify, 0, 1, 1, 1)
        self.authkey = QtWidgets.QLineEdit(self.frame_1)
        self.authkey.setMinimumSize(QtCore.QSize(450, 25))
        self.authkey.setMaximumSize(QtCore.QSize(450, 25))
        self.authkey.setMaxLength(45)
        self.authkey.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[a-z-A-Z-0-9_]+")))
        self.authkey.setClearButtonEnabled(True)
        self.authkey.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.authkey, 0, 0, 1, 1)
        self.verticalLayout_2.addWidget(self.frame_1)
        self.frame = QtWidgets.QFrame(self.groupBox)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.name = QtWidgets.QLabel(self.frame)
        self.name.setObjectName("name")
        self.gridLayout_2.addWidget(self.name, 0, 0, 1, 1)
        self.ac = QtWidgets.QLabel(self.frame)
        self.ac.setObjectName("ac")
        self.gridLayout_2.addWidget(self.ac, 0, 1, 1, 1)
        self.email = QtWidgets.QLabel(self.frame)
        self.email.setObjectName("email")
        self.gridLayout_2.addWidget(self.email, 1, 0, 1, 2)
        self.verticalLayout_2.addWidget(self.frame)
        self.verticalLayout.addWidget(self.groupBox)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "odrive-x"))
        self.groupBox.setTitle(_translate("MainWindow", "Authentication"))
        self.name.setText(_translate("MainWindow", "Name:"))
        self.ac.setText(_translate("MainWindow", "Account Type:"))
        self.email.setText(_translate("MainWindow", "Email:"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = AuthenticateGui()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
