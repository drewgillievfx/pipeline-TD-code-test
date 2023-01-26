#!/usr/bin/env python

# from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import QtCore

class BasicDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(BasicDialog, self).__init__(parent=parent)
        # Instantiate a layout and set it as the dialogs main layout
        main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(main_layout)
        # Add ok and cancel buttons
        # And hook them up to dialogs accept/reject methods
        button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok|\
                                            QtWidgets.QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        main_layout.addWidget(button_box)

    def getValues(self):
        return None

if __name__ == '__main__':
    # Instantiate a QApplication - requirement for Qt
    app = QtWidgets.QApplication([])
    # Instantiate, show, then raise our dialog to the front
    dlg = BasicDialog()
    dlg.show()
    dlg.raise_()
    # only getValues if 'Ok' is clicked
    if dlg.exec_():
        values = dlg.getValues()
        print(values)
