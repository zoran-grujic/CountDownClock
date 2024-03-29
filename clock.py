#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 23 22:06:01 2017

@author: Zoran Grujić
"""

import sys
import os
import time
from PyQt5 import QtGui, QtWidgets, QtCore
import configparser
dir_ = os.path.dirname(os.path.realpath(sys.argv[0]))

config=configparser.ConfigParser() #make config object 
configFile = dir_ + "/config.txt"


class ClockWindow(QtWidgets.QWidget):
    width=None
    height=None
    clockFontSize = 200

    talkTime        = 20*60 #20 min total time in seconds
    talkQuestions   = 5*60 #save 5 min for questions in seconds
    remainingTime   = talkTime
    clockRunning = False
    
    
    

    def __init__(self, width, height):
        super(ClockWindow, self).__init__()
        self.width = width
        self.height = height
        self.getConfig()
        self.remainingTime = self.talkTime
        
        self.timer = QtCore.QTimer(self)#make timer to belong to the PlotForm class

        self.setStyleSheet("QWidget { background-color: green; }")
        self.initUI()

    def initUI(self):

        """
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("FreeMono"))
        font.setBold(True)
        font.setSize(50)
        """

        self.clockLabel = QtWidgets.QLabel("15:00", self)# bottom left to indicate app status
        #self.clockLabel.setFont(font)
        
        self.setDisplayTime()

        self.helpLabel = QtWidgets.QLabel('SPACE: restart, p: pause/play,  LEFT: one minute less, RIGHT: one minute plus, UP: font increase, DOWN: font decrease', self)#

        mainVBox = QtWidgets.QVBoxLayout()
        mainVBox.addStretch(1)
        
        clockHBox = QtWidgets.QHBoxLayout()
        clockHBox.addStretch(1)
        clockHBox.addWidget(self.clockLabel)
        clockHBox.addStretch(1)

        mainVBox.addLayout(clockHBox)
        mainVBox.addStretch(1)
        mainVBox.addWidget(self.helpLabel)

        self.setLayout(mainVBox)

        self.setGeometry(150, 150, self.width-300, self.height-300)

        self.timer.setInterval( 1000)
        self.timer.timeout.connect(self.clockThick)
        self.timer.start()
        
    def setDisplayTime(self):
        if self.remainingTime > 0:
            rmSec = self.remainingTime % 60
            rmMin= int((self.remainingTime - rmSec)/60)
        else:
            rmSec = (-self.remainingTime) % 60
            rmMin= int(((-self.remainingTime) - rmSec)/60)

        
        self.clockLabel.setText("{0:02d}:{1:02d}".format(rmMin, rmSec) )
        self.clockLabel.setStyleSheet("font: %spt Comic Sans MS" % self.clockFontSize)
        
    def clockThick(self):
        if self.clockRunning:
            #decrease remaining time
            self.remainingTime = self.remainingTime - 1
            self.setDisplayTime()
            
            #set color, green
            if self.remainingTime> self.talkQuestions:
                self.setBgColor("green")
            else:
                if self.remainingTime > 0:
                    self.setBgColor("orange")
                else:
                    self.setBgColor("red")
                    
        else:
            return
        pass
    
    def getConfig(self):
        """
        Read configuration
        """
        global config

        config.read(configFile)
        #print(configFile,"         ",config, "   ", config.sections())
        self.talkTime = int(eval(config["Talk"]["talktime_sec"]))
        self.talkQuestions = int(eval(config["Talk"]["questionstime_sec"]))
        #print(self.talkTime, "   ", self.talkQuestions)
        
    def setBgColor(self, color):
        self.setStyleSheet("QWidget { background-color: %s; }" % color)
        
    def keyPressEvent(self, event):
        key = event.key()
        #print(key)

        if key == 32: #space
            #restart
            self.getConfig()
            self.clockRunning = True
            self.remainingTime = self.talkTime
            return
        if key == 80:     # p for pause/play
            self.clockRunning = not self.clockRunning
            return
        
        if key == QtCore.Qt.Key_Left:
            self.remainingTime = self.remainingTime + 60
            self.setDisplayTime()
            #print('Left Arrow Pressed')
            return
        if key == QtCore.Qt.Key_Right:
            self.remainingTime = self.remainingTime - 60
            self.setDisplayTime()
            #print('Right Arrow Pressed')
            return
        if key == QtCore.Qt.Key_Up:
            self.clockFontSize = self.clockFontSize+ 20
            self.setDisplayTime()
            #print('Up Arrow Pressed')
            return
        if key == QtCore.Qt.Key_Down:
            self.clockFontSize = self.clockFontSize- 20
            self.setDisplayTime()
            #print('Down Arrow Pressed')
            return


def main():
    
    
    # app = QtGui.QApplication(sys.argv)
    app = QtWidgets.QApplication(sys.argv)
    screen_resolution = app.desktop().screenGeometry()
    wh= [screen_resolution.width(), screen_resolution.height()]
    clock = ClockWindow(wh[0],wh[1])
    #print("Height: ", wh[1])
    
    clock.show()
    #clock.showMaximized()
    
    app.exec_()#execute until closed
    
    exit()

if __name__ == '__main__':
    main() 
