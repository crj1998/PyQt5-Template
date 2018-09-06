#!user/bin/env python
#!-*-coding:utf-8 -*-
#!Time: 2018/8/27 13:38
#!Author: Renjie Chen
#!Function: 用于日期范围选择

from PyQt5.QtWidgets import QCalendarWidget, QDialog, QApplication, QPushButton, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import QDate
import datetime
class CalendarDialog(QDialog):
    def __init__(self,mindate=QDate(2005,1,1),maxdate=QDate(datetime.date.today())):
        super().__init__()
        self.mindate=mindate
        self.maxdate=maxdate
        self.date=maxdate
        self.initUI()
    def initUI(self):
        self.button=QPushButton('完成',self)
        self.button.clicked.connect(self.getdate)
        self.calendar=QCalendarWidget(self)
        self.calendar.setGridVisible(True)
        self.calendar.setFirstDayOfWeek(7)
        self.calendar.setDateRange(self.mindate,self.maxdate)
        self.calendar.setHorizontalHeaderFormat(QCalendarWidget.ShortDayNames)
        self.calendar.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        vbox=QVBoxLayout()
        vbox.addStretch()
        vbox.addWidget(self.calendar)
        vbox.addWidget(self.button)
        hbox=QHBoxLayout()
        hbox.addStretch()
        hbox.addLayout(vbox)
        self.setLayout(hbox)
        self.setFixedSize(335,350)
        
    def getdate(self):
        self.date=self.calendar.selectedDate()
        self.done(1)