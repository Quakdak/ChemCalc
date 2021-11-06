import sqlite3

import sympy
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QWidget

from classes.request import Request
from scripts.chemistry import chemass, parse_compound, elements


class ChemCalc(QMainWindow):
    def __init__(self):
        super().__init__()
        self.sw = Information()
        uic.loadUi('data/main.ui', self)
        self.requests = []
        self.request_index = -1
        self.init_requests()
        self.init_widgets()

    def init_widgets(self):
        self.setWindowTitle('Chemcalc')
        self.mass.clicked.connect(self.show_element_weight)
        self.equalizer.clicked.connect(self.show_balance)
        self.help.clicked.connect(self.info)
        self.next.clicked.connect(self.show_next_request)
        self.previous.clicked.connect(self.show_previous_request)

    def init_requests(self):
        session = sqlite3.connect("db/ChemCalc.db")
        cursor = session.cursor()
        requests_local = cursor.execute("SELECT request_left, request_right, result FROM Requests").fetchall()
        print(requests_local)
        self.requests.append(Request("", "", ""))
        for elem in requests_local:
            req = Request(elem[0], elem[1], elem[2])
            self.requests.append(req)
        session.close()
        self.request_index = len(self.requests) - 1
        print("SELF.REQUESTS: ")
        for elem in self.requests:
            print(elem)
        print("LOG:", elements)

    def show_next_request(self):
        print("SHOWING NEXT REQUEST :", end="")
        self.request_index += 1
        if self.request_index == len(self.requests):
            self.request_index -= 1
        print(self.request_index)
        req_tmp = self.requests[self.request_index]
        self.show_request(
            req_tmp.left,
            req_tmp.right,
            req_tmp.result
        )

    def show_previous_request(self):
        print("SHOWING PREVIOUS REQUEST :", end="")
        self.request_index -= 1
        if self.request_index < 0:
            self.request_index = 0
        print(self.request_index)
        req_tmp = self.requests[self.request_index]
        self.show_request(
            req_tmp.left,
            req_tmp.right,
            req_tmp.result
        )

    def show_element_weight(self):
        element = self.chemel.text()
        try:
            a = eval(chemass(element))
            a = str(a) + ' а.е.м.'
        except Exception:
            a = 'Ошибка ввода'
        self.answ2.setText(a)

    def show_request(self, lhs, rhs, result):
        self.left.setText(lhs)
        self.right.setText(rhs)
        self.answ1.setText(result)

    def show_balance(self):
        try:
            lhs_copy = self.left.text()
            rhs_copy = self.right.text()
            lhs_strings = self.left.text().split()
            lhs_compounds = [parse_compound(compound) for compound in lhs_strings]

            rhs_strings = self.right.text().split()
            rhs_compounds = [parse_compound(compound) for compound in rhs_strings]

            els = sorted(set().union(*lhs_compounds, *rhs_compounds))
            els_index = dict(zip(els, range(len(els))))

            w = len(lhs_compounds) + len(rhs_compounds)
            h = len(els)
            A = [[0] * w for _ in range(h)]
            for col, compound in enumerate(lhs_compounds):
                for el, num in compound.items():
                    row = els_index[el]
                    A[row][col] = num
            for col, compound in enumerate(rhs_compounds, len(lhs_compounds)):
                for el, num in compound.items():
                    row = els_index[el]
                    A[row][col] = -num

            A = sympy.Matrix(A)
            coeffs = A.nullspace()[0]
            coeffs *= sympy.lcm([term.q for term in coeffs])

            lhs = " + ".join(["{} {}".format(coeffs[i], s) for i, s in enumerate(lhs_strings)])
            rhs = " + ".join(["{} {}".format(coeffs[i], s) for i, s in enumerate(rhs_strings, len(lhs_strings))])
            answer = "{} -> {}".format(lhs, rhs)
            self.answ1.setText(answer)
            session = sqlite3.connect("db/ChemCalc.db")
            cursor = session.cursor()
            print("LHS == " + lhs_copy)
            print("RHS == " + rhs_copy)
            print("ANSWER == " + answer)
            cursor.execute('INSERT INTO Requests(request_left, request_right, result) '
                           'VALUES (?, ?, ?)', (lhs_copy, rhs_copy, answer)).fetchall()
            cur_request = Request(lhs_copy, rhs_copy, answer)
            self.requests.append(cur_request)
            self.request_index = len(self.requests) - 1
            session.commit()
            session.close()

        except Exception:
            self.answ1.setText('Ошибка ввода(См.справку)')

    def info(self):
        self.sw.show()


class Information(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('data/info.ui', self)
        self.setWindowTitle('Info')
