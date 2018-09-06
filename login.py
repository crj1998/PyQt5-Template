#!user/bin/env python
#!-*-coding:utf-8 -*-
#!Time: 2018/8/23 20:47
#!Author: Renjie Chen
#!Function: 登录界面

from PyQt5.QtWidgets import QDialog, QApplication, QLineEdit, QLabel, QPushButton, QMessageBox, QCheckBox, QGridLayout, QCompleter, QWidget, QLayout
from PyQt5.QtCore import Qt, QEvent, QRegExp, QObject, QTimer
from PyQt5.QtGui import QKeyEvent, QKeySequence, QRegExpValidator, QFont, QPixmap, QStandardItemModel, QIcon
import random
import os

class RetrieveDialog(QDialog):

    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon('Valid.ico'))
        #Qt.WindowCloseButtonHint 仅有关闭按钮
        #Qt.SubWindow 仅有标题栏，不再任务栏
        #Qt.SplashScreen 标题栏，按钮都没有，不可关闭
        #Qt.WindowTitleHint,Qt.WindowSystemMenuHint
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowTitle("找回密码")
        self.user=''
        self.password=''
        self.createWidgets()
        self.createGridLayout()

    def createWidgets(self):
        self.lb1 = QLabel('邮箱：',self)
        self.lb2 = QLabel('验证码：',self)
        self.lb3 = QLabel('新密码：', self)
        self.lb4 = QLabel('确认密码：', self)
        
        self.lb1.setFixedSize(85, 20)
        self.lb2.setFixedSize(85, 20)
        self.lb3.setFixedSize(85, 20)
        self.lb4.setFixedSize(85, 20)

        self.lb1a = QLabel(self)
        self.lb3a = QLabel(self)
        self.lb4a = QLabel(self)
        self.lb1a.setFixedSize(30,30)
        self.lb3a.setFixedSize(30,30)
        self.lb4a.setFixedSize(30,30)

        self.pix_info = QPixmap('Info.ico')
        self.pix_valid = QPixmap('Valid.ico')
        self.pix_error = QPixmap('Error.ico')
        self.lb1a.setPixmap(self.pix_info)
        self.lb3a.setPixmap(self.pix_info)
        self.lb4a.setPixmap(self.pix_info)
        self.lb1a.setToolTip('邮箱地址为空')
        self.lb3a.setToolTip('密码为空')
        self.lb4a.setToolTip('密码为空')

        self.edit1 = QLineEdit(self)
        self.edit2 = QLineEdit(self)
        self.edit3 = QLineEdit(self)
        self.edit4 = QLineEdit(self)
        self.edit1.setFixedSize(450,25)
        self.edit2.setFixedHeight(25)
        self.edit3.setFixedSize(450,25)
        self.edit4.setFixedSize(450,25)
        self.edit1.setClearButtonEnabled(True)
        self.edit2.setClearButtonEnabled(True)
        self.edit3.setClearButtonEnabled(True)
        self.edit4.setClearButtonEnabled(True)
        self.edit1.setPlaceholderText("请注意邮箱格式")
        self.edit3.setPlaceholderText("长度不少于8位，不超过16位，必须包含数字和字母")
        self.edit4.setPlaceholderText("请再次输入密码")
        self.edit3.setContextMenuPolicy(Qt.NoContextMenu)
        self.edit4.setContextMenuPolicy(Qt.NoContextMenu)
        self.edit3.setEchoMode(QLineEdit.Password)
        self.edit4.setEchoMode(QLineEdit.Password)
        self.edit2.setEnabled(False)

        self.model = QStandardItemModel(0, 1, self)
        completer = QCompleter(self.model, self)
        self.edit1.setCompleter(completer)
        completer.activated[str].connect(self.edit1.setText)
        self.edit1.textEdited[str].connect(self.autocomplete)

        regx = QRegExp("^[0-9A-Za-z_.-]{3,16}@[0-9A-Za-z-]{1,10}(\.[a-zA-Z0-9-]{0,10}){0,2}\.[a-zA-Z0-9]{2,6}$")
        validator = QRegExpValidator(regx, self.edit1)
        self.edit1.setValidator(validator)
        regx = QRegExp("[0-9]{8}$")
        validator = QRegExpValidator(regx, self.edit2)
        self.edit2.setValidator(validator)
        regx = QRegExp("[0-9A-Za-z]{16}$")
        validator = QRegExpValidator(regx, self.edit3)
        self.edit3.setValidator(validator)
        validator = QRegExpValidator(regx, self.edit4)
        self.edit4.setValidator(validator)
        

        self.bt1 = QPushButton('发送验证码',self)
        self.bt2 = QPushButton('确定', self)
        self.bt1.setEnabled(False)
        self.bt2.setEnabled(False)
        self.bt2.setFixedSize(150,35)
        self.bt1.clicked.connect(self.sendcode)
        self.bt2.clicked.connect(self.sign_in)
        #self.bt2.setCheckable(True)

        self.count = 14
        self.time = QTimer(self)
        self.time.setInterval(1000)
        self.time.timeout.connect(self.Refresh)

        self.time_100ms = QTimer(self)
        self.time_100ms.setInterval(100)
        self.time_100ms.timeout.connect(self.Refresh_100ms)
        self.time_100ms.start()

        self.time_100msa = QTimer(self)
        self.time_100msa.setInterval(100)
        self.time_100msa.timeout.connect(self.Refresh_100msa)

        self.extension = QWidget()
        self.extension.hide()
        #self.bt2.toggled.connect(self.extension.setVisible)


    def createGridLayout(self):
        initgrid = QGridLayout()
        initgrid.setSpacing(10)
        initgrid.addWidget(self.lb1, 0, 1, 1, 1)
        initgrid.addWidget(self.lb2, 1, 1, 1, 1)
        initgrid.addWidget(self.edit1, 0, 2, 1, 2)
        initgrid.addWidget(self.edit2, 1, 2, 1, 1)
        initgrid.addWidget(self.lb1a, 0, 4, 1, 1)
        initgrid.addWidget(self.bt1, 1, 3)

        extensiongrid = QGridLayout()
        extensiongrid.setSpacing(10)
        #设置距离四周的空白
        extensiongrid.setContentsMargins(0, 0, 0, 0)
        extensiongrid.addWidget(self.lb3, 2, 1, 1, 1)
        extensiongrid.addWidget(self.lb4, 3, 1, 1, 1)
        extensiongrid.addWidget(self.edit3, 2, 2, 1, 2)
        extensiongrid.addWidget(self.edit4, 3, 2, 1, 2)
        extensiongrid.addWidget(self.lb3a, 2, 4, 1, 1)
        extensiongrid.addWidget(self.lb4a, 3, 4, 1, 1)
        self.extension.setLayout(extensiongrid)

        mainLayout = QGridLayout()
        mainLayout.setSizeConstraint(QLayout.SetFixedSize)
        mainLayout.addLayout(initgrid,0,0)
        mainLayout.addWidget(self.extension,1,0)
        mainLayout.addWidget(self.bt2,2,0)
        mainLayout.setAlignment(self.bt2,Qt.AlignCenter)
        mainLayout.setRowStretch(2, 1)
        self.setLayout(mainLayout)

    def eventFilter(self, object, event):
        if object == self.edit3 or object == self.edit4:
            if event.type() == QEvent.MouseMove or event.type() == QEvent.MouseButtonDblClick:
                return True
            elif event.type() == QEvent.KeyPress:
                key = QKeyEvent(event)
                if key.matches(QKeySequence.SelectAll) or key.matches(QKeySequence.Copy) or key.matches(
                        QKeySequence.Paste):
                    return True
        return QDialog.eventFilter(self, object, event)

    def sign_in(self):
        if self.bt2.text()=="确定":
            if self.edit2.text() != self.code:
                self.edit2.clear()
                QMessageBox.warning(self, "警告", "验证码错误！")
            else:
                self.bt2.setText("完成")
                self.bt2.setEnabled(False)
                self.extension.setVisible(True)
                self.edit2.setEnabled(False)
                self.time_100msa.start()
        else:
            self.password=self.edit3.text()
            QMessageBox.information(self, "提示", "密码修改成功！\n账号：%s \n密码：%s"%(self.user,self.password))
            self.done(1)

    def sendcode(self):
        if self.bt1.isEnabled():
            self.extension.setVisible(False)
            self.time_100ms.stop()
            self.code=''.join(random.sample("0123456789",8))
            self.user=self.edit1.text()
            self.edit1.setEnabled(False)
            self.edit2.setEnabled(True)
            self.time.start()
            self.bt1.setEnabled(False)
            self.bt1.setText('15秒后重发')
            self.bt2.setEnabled(True)
            self.time_100msa.stop()
            print(self.code)

    def autocomplete(self, text):
        if '@' in self.edit1.text():
            return
        emaillist = ["@live.com", "@139.com", "@126.com", "@163.com", "@gmail.com", "@qq.com"]
        self.model.removeRows(0, self.model.rowCount())
        for i in range(0, len(emaillist)):
            self.model.insertRow(0)
            self.model.setData(self.model.index(0, 0), text + emaillist[i])

    def Refresh(self):
        if self.count > 0:
            self.bt1.setText(str(self.count)+'秒后重发')
            self.count -= 1
        else:
            self.time.stop()
            self.time_100ms.start()
            self.edit1.setEnabled(True)
            self.bt1.setEnabled(True)
            self.bt1.setText('发送验证码')
            self.count = 14

    def Refresh_100ms(self):
        text = self.edit1.text()
        if text == '':
            self.lb1a.setPixmap(self.pix_info)
            self.lb1a.setToolTip('邮箱地址为空')
            self.bt1.setEnabled(False)
        elif "@" not in text:
            self.lb1a.setPixmap(self.pix_error)
            self.lb1a.setToolTip('邮箱地址非法')
            bool1 = False
        else:
            self.lb1a.setPixmap(self.pix_valid)
            self.lb1a.setToolTip('邮箱地址合法')
            self.bt1.setEnabled(True)

    def Refresh_100msa(self):
        text = self.edit3.text()
        if text == '':
            self.lb3a.setPixmap(self.pix_info)
            self.lb3a.setToolTip('密码为空')
            bool3 = False
        elif 0<len(text)<8:
            self.lb3a.setPixmap(self.pix_error)
            self.lb3a.setToolTip('密码长度小于8位')
            bool3 = False
        else:
            self.lb3a.setPixmap(self.pix_valid)
            self.lb3a.setToolTip('密码有效')
            bool3 = True

        text = self.edit4.text()
        if text == '':
            self.lb4a.setPixmap(self.pix_info)
            self.lb4a.setToolTip('密码为空')
            bool4 = False
        elif text != self.edit3.text():
            self.lb4a.setPixmap(self.pix_error)
            self.lb4a.setToolTip('密码不一致')
            bool4 = False
        else:
            self.lb4a.setPixmap(self.pix_valid)
            self.lb4a.setToolTip('密码有效')
            bool4 = True

        if bool3 and bool4:
            self.bt2.setEnabled(True)
        else:
            self.bt2.setEnabled(False)



if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    dialog = RetrieveDialog()
    dialog.show()
    sys.exit(app.exec_())
    #r = pwd.exec_()
    #if r:
    #    print(pwd.text)