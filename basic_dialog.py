#!/usr/bin/env python

from PyQt4 import QtGui

class BasicDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        super(BasicDialog, self).__init__(parent=parent)
        #Instantiate a layout and set it as the dialogs main layout
        main_layout = QtGui.QVBoxLayout()
        self.setLayout(main_layout)
        #Add ok and cancel buttons
        #And hook them up to dialogs accept/reject methods
        button_box = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok|\
                                            QtGui.QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        main_layout.addWidget(button_box)

    def getValues(self):
        return None

if __name__ == '__main__':
    #Instantiate a QApplication - requirement for Qt
    app = QtGui.QApplication([])
    #Instantiate, show, then raise our dialog to the front
    dlg = BasicDialog()
    dlg.show()
    dlg.raise_()
    #only getValues if 'Ok' is clicked
    if dlg.exec_():
        print dlg.getValues()
