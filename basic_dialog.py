#!/usr/bin/env python

# from PyQt5 import QtGui
from PyQt5 import QtWidgets
# from PyQt5 import QtCore
import datetime

class BasicDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(BasicDialog, self).__init__(parent=parent)
        # Instantiate a layout and set it as the dialogs main layout
        main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(main_layout)

        # Add ok and cancel buttons
        # And hook them up to dialogs accept/reject methods
        button_box = QtWidgets.QDialogButtonBox(
                                            QtWidgets.QDialogButtonBox.Ok|\
                                            QtWidgets.QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        main_layout.addWidget(button_box)

        # Add QLineEdit : Name
        self.name_edit = QtWidgets.QLineEdit()
        self.name_edit.setObjectName("Name")
        main_layout.addWidget(QtWidgets.QLabel("Name"))
        main_layout.addWidget(self.name_edit)

        # Add QComboBox : A B C
        self.combo_box = QtWidgets.QComboBox()
        self.combo_box.addItems(["A", "B", "C"])
        self.combo_box.setObjectName("Type")
        main_layout.addWidget(QtWidgets.QLabel("Type"))
        main_layout.addWidget(self.combo_box) 

        # Add QDateWidget : Need By
        self.need_date = QtWidgets.QDateEdit()
        self.need_date.setDate(datetime.datetime.now().date() +
                                datetime.timedelta(days=7))
        self.need_date.setMinimumDate(datetime.datetime.now().date())
        self.need_date.setCalendarPopup(True)
        self.need_date.setObjectName("Need By:")
        main_layout.addWidget(QtWidgets.QLabel("Need By:"))
        main_layout.addWidget(self.need_date)

        # Add QTextEdit : Notes
        self.text_edit = QtWidgets.QTextEdit()
        self.text_edit.setPlaceholderText("Write any notes here...")
        self.text_edit.setObjectName("Notes")
        main_layout.addWidget(QtWidgets.QLabel("Notes"))
        main_layout.addWidget(self.text_edit)

    def getValues(self):
        return {
                "Name:": self.name_edit.text(),
                "Type:": self.combo_box.currentText(),
                "Need By:": self.need_date.date().toPyDate(),
                "Notes:": self.text_edit.toPlainText(),
        }
        # return None
 
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
