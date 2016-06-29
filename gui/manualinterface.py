# Temperature-conversion program using PyQt

import sys
from PyQt4 import QtCore, QtGui, uic

form_class = uic.loadUiType("gui/gui.ui")[0]                 # Load the UI

from math import radians

class MyWindowClass(QtGui.QMainWindow, form_class):
    def __init__(self, parent=None,controllers = None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)

        self.controllers = controllers

        self.fl1.valueChanged.connect(self.update_pos)  # Bind the event handlers
        self.fl2.valueChanged.connect(self.update_pos)  # Bind the event handlers
        self.fl3.valueChanged.connect(self.update_pos)  # Bind the event handlers

        self.fr1.valueChanged.connect(self.update_pos)  # Bind the event handlers
        self.fr2.valueChanged.connect(self.update_pos)  # Bind the event handlers
        self.fr3.valueChanged.connect(self.update_pos)  # Bind the event handlers

        self.rl1.valueChanged.connect(self.update_pos)  # Bind the event handlers
        self.rl2.valueChanged.connect(self.update_pos)  # Bind the event handlers
        self.rl3.valueChanged.connect(self.update_pos)  # Bind the event handlers

        self.rr1.valueChanged.connect(self.update_pos)  # Bind the event handlers
        self.rr2.valueChanged.connect(self.update_pos)  # Bind the event handlers
        self.rr3.valueChanged.connect(self.update_pos)  # Bind the event handlers

    def update_pos(self):
        fl = [radians(self.fl1.value()), radians(self.fl2.value()), radians(self.fl3.value())]
        fr = [radians(self.fr1.value()), radians(self.fr2.value()), radians(self.fr3.value())]
        rl = [radians(self.rl1.value()), radians(self.rl2.value()), radians(self.rl3.value())]
        rr = [radians(self.rl1.value()), radians(self.rl2.value()), radians(self.rl3.value())]
        for controller in self.controllers:
            controller.move_legs_to_angles(*fl)

            controller.robot.finish_iteration()


