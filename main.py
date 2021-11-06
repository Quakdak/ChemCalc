from sys import exit, argv

from PyQt5.QtWidgets import QApplication

from classes.widgets import ChemCalc

if __name__ == '__main__':
    app = QApplication(argv)
    ex = ChemCalc()
    ex.show()
    exit(app.exec_())
