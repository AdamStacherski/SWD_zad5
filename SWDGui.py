# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\admin\Desktop\dwad\SWDGui.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow,QWidget, QVBoxLayout,QLabel, QFileDialog,QMessageBox
import sys
import os
import pandas as pd
import RSM
import SP
import topsis_example
import utastar
import matplotlib.pyplot as plt
import compare_rankings

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.lista_dan = []
        self.path = ""

        self.n_criteria = 0

        self.punkty = QtGui.QStandardItemModel()
        self.klasy = QtGui.QStandardItemModel()
        self.klasy.setHorizontalHeaderLabels(["punkt", "klasa"])
        self.rank = QtGui.QStandardItemModel()
        self.rank.setHorizontalHeaderLabels(["punkt", "score"])


        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(939, 721)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(80, 30, 141, 41))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.openFile)


        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(630, 30, 141, 41))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.compute)

        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(360, 40, 131, 21))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItems(["RSM","Topsis","SPCS","STAR", "Porównanie 1", "Porównanie 2", "Porównanie 3", "Porównanie 4"])

        self.punktyView = QtWidgets.QTableView(self.centralwidget)
        self.punktyView.setGeometry(QtCore.QRect(70, 150, 256, 192))
        self.punktyView.setObjectName("punktyView")
        self.punktyView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.punktyView.setModel(self.punkty)

        self.klasyView = QtWidgets.QTableView(self.centralwidget)
        self.klasyView.setGeometry(QtCore.QRect(600, 150, 256, 192))
        self.klasyView.setObjectName("klasyView")
        self.klasyView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.klasyView.setModel(self.klasy)

        self.rankView = QtWidgets.QTableView(self.centralwidget)
        self.rankView.setGeometry(QtCore.QRect(330, 420, 256, 192))
        self.rankView.setObjectName("rankView")
        self.rankView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.rankView.setModel(self.rank)


        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(110, 120, 161, 21))
        self.label.setObjectName("label")

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(700, 130, 55, 16))
        self.label_2.setObjectName("label_2")

        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(430, 400, 55, 16))
        self.label_3.setObjectName("label_3")

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def compute(self):
        if self.rank.rowCount() != 0:
            self.klasy = QtGui.QStandardItemModel()
            self.klasy.setHorizontalHeaderLabels(["punkt", "klasa"])
            self.rank = QtGui.QStandardItemModel()
            self.rank.setHorizontalHeaderLabels(["punkt", "score"])
        used = self.comboBox.currentText()
        if used == "RSM":
            ranking,A1,A2,w = RSM.main(self.lista_dan,self.path)
            for i in range(len(w)):
                newItem = QtGui.QStandardItem(str(list(w)[i]))
                self.rank.appendRow(newItem)
                row_id = self.rank.rowCount() - 1
                self.rank.setData(self.rank.index(row_id,1),str(w[list(w)[i]]))
            for i in A1:
                newItem = QtGui.QStandardItem(str(i))
                self.klasy.appendRow(newItem)
                row_id = self.klasy.rowCount() - 1
                self.klasy.setData(self.klasy.index(row_id,1),"A1")
            for i in A2:
                newItem = QtGui.QStandardItem(str(i))
                self.klasy.appendRow(newItem)
                row_id = self.klasy.rowCount() - 1
                self.klasy.setData(self.klasy.index(row_id,1),"A2")
            self.rankView.resizeColumnsToContents()
            self.klasyView.resizeColumnsToContents()
            self.do_figure_RSM(ranking)
        elif used == "SPCS":
            if len(self.lista_dan[0]) == 2:
                ranking,A1,A2 = SP.main(self.lista_dan)
                ranking = dict(sorted(SP.change(ranking,self.path).items(), key = lambda x: x[1]))
                for i in range(len(ranking)):
                    newItem = QtGui.QStandardItem(str(list(ranking)[i]))
                    self.rank.appendRow(newItem)
                    row_id = self.rank.rowCount() - 1
                    self.rank.setData(self.rank.index(row_id,1),str(ranking[list(ranking)[i]]))

                for i in A1:
                    newItem = QtGui.QStandardItem(str(i))
                    self.klasy.appendRow(newItem)
                    row_id = self.klasy.rowCount() - 1
                    self.klasy.setData(self.klasy.index(row_id,1),"A1")

                for i in A2:
                    newItem = QtGui.QStandardItem(str(i))
                    self.klasy.appendRow(newItem)
                    row_id = self.klasy.rowCount() - 1
                    self.klasy.setData(self.klasy.index(row_id,1),"A2")
                self.rankView.resizeColumnsToContents()
                self.klasyView.resizeColumnsToContents()
                self.do_figure_SP(ranking)
            elif len(self.lista_dan[0]) == 3:
                pass
            # TODO funckaj spcs dla 3 zmeinnych do organizacji.
        elif used == "Topsis":
            solution, named_ranking = topsis_example.main(self.path)
            s = {u: value for u, value in sorted(named_ranking.items(), key=lambda item: item[1],reverse=True)}
            for key, value in s.items(): # ranking do posortowania
                newItem = QtGui.QStandardItem(str(key))
                self.rank.appendRow(newItem)
                row_id = self.rank.rowCount() - 1
                self.rank.setData(self.rank.index(row_id,1),str(value))
            self.do_figure_SP(solution.get_dict_ranking())
        elif used == "STAR":
            s = utastar.main(self.path)
            for key,value in s.items():
                newItem = QtGui.QStandardItem(str(key))
                self.rank.appendRow(newItem)
                row_id = self.rank.rowCount() - 1
                self.rank.setData(self.rank.index(row_id,1),str(value))
            self.do_figure_STAR(s)

        elif "Porównanie" in used:
            if self.n_criteria == 0:
                return

            ranking,A1,A2, r1 = RSM.main(self.lista_dan,self.path)
            r1 = {name: i+1 for i, name in enumerate(r1.keys())}
            if self.n_criteria <= 2:
                r2, A1, A2 = SP.main(self.lista_dan)
                r2 = dict(sorted(SP.change(r2, self.path).items(), key=lambda x: x[1]))
                r2 = {name: i+1 for i, name in enumerate(r2.keys())}
            else:
                r2 = None
            solution, r3 = topsis_example.main(self.path)
            r3 = {u: value for u, value in sorted(r3.items(), key=lambda item: item[1], reverse=True)}
            r3 = {name: i+1 for i, name in enumerate(r3.keys())}
            r4 = utastar.main(self.path)
            r4 = {name: score[1] for name, score in r4.items()}

            considered_ranks = [r1, r2, r3, r4]
            beer_sets = [set(r.keys()) for r in considered_ranks if r is not None]
            common_beers = set.intersection(*beer_sets)
            methods_ranks = [[] for r in considered_ranks if r is not None]
            for beer in common_beers:
                for i, r in enumerate([rank for rank in considered_ranks if rank is not None]):
                    methods_ranks[i].append(r[beer])
            considered_method_names = ["RSM", "SPCS", "TOPSIS", "UTA"]
            method_names = [name for r, name in zip(considered_ranks, considered_method_names) if r is not None]
            comparison_type = int(used[-1])
            compare_rankings.main(rankings=methods_ranks, type=comparison_type, methods=method_names)

    def do_figure_RSM(self,data):
        fig = plt.figure(figsize=(12,12))
        if len(self.lista_dan[0]) == 2:
            x = []
            y = []
            for tup in self.lista_dan:
                x.append(tup[0])
                y.append(tup[1])

            plt.scatter(x,y)
            x2 = []
            y2 = []
            new_data = list(data)
            i = 0
            for cos in new_data:
                if i > 5:
                    break
                x2.append(cos.a)
                y2.append(cos.b)
                i += 1
            plt.scatter(x2,y2,c="red")
            plt.show()
        elif len(self.lista_dan[0]) == 3:
            ax = fig.add_subplot(projection='3d')
            x = []
            y = []
            z = []
            for tup in self.lista_dan:
                x.append(tup[0])
                y.append(tup[1])
                z.append(tup[2])
            ax.scatter(x,y,z)
            x2 = []
            y2 = []
            z2 = []
            i = 0
            for key in data.keys():
                if i > 5:
                    break
                x2.append(key.a)
                y2.append(key.b)
                z2.append(key.c)
                i += 1
                print(i)
            print(len(x2))
            ax.scatter(x2,y2,z2,c='red')
            plt.show()

    def do_figure_SP(self,data):
        fig = plt.figure(figsize=(12,12))
        if len(self.lista_dan[0]) == 2:
            x = []
            y = []
            for tup in self.lista_dan:
                x.append(tup[0])
                y.append(tup[1])

            plt.scatter(x,y)
            x2 = []
            y2 = []
            new_data = list(data)
            i = 0
            for cos in new_data:
                if i > 5:
                    break
                x2.append(cos[0])
                y2.append(cos[1])
                i += 1
            plt.scatter(x2,y2,c="red")
            plt.show()
        elif len(self.lista_dan[0]) == 3:
            ax = fig.add_subplot(projection='3d')
            x = []
            y = []
            z = []
            for tup in self.lista_dan:
                x.append(tup[0])
                y.append(tup[1])
                z.append(tup[2])
            ax.scatter(x,y,z)
            x2 = []
            y2 = []
            z2 = []
            i = 0
            for key,value in data.items():
                if i > 5:
                    break
                x2.append(key[0])
                y2.append(key[1])
                z2.append(key[2])
                i += 1
            ax.scatter(x2,y2,z2,c='red')
            plt.show()

    def do_figure_STAR(self,data):
        fig = plt.figure(figsize=(12,12))
        if len(self.lista_dan[0]) == 2:
            x = []
            y = []
            for tup in self.lista_dan:
                x.append(tup[0])
                y.append(tup[1])

            plt.scatter(x,y)
            x2 = []
            y2 = []
            new_data = list(data)
            i = 0
            for cos in new_data:
                if i > 5:
                    break
                x2.append(cos[1])
                y2.append(cos[2])
                i += 1
            plt.scatter(x2,y2,c="red")
            plt.show()
        elif len(self.lista_dan[0]) == 3:
            ax = fig.add_subplot(projection='3d')
            x = []
            y = []
            z = []
            for tup in self.lista_dan:
                x.append(tup[0])
                y.append(tup[1])
                z.append(tup[2])
            ax.scatter(x,y,z)
            x2 = []
            y2 = []
            z2 = []
            i = 0
            for key,value in data.items():
                if i > 5:
                    break
                x2.append(key[1])
                y2.append(key[2])
                z2.append(key[3])
                i += 1
            ax.scatter(x2,y2,z2,c='red')
            plt.show()

    def openFile(self):
        file_filter = "Data File (*.csv)"
        response = QFileDialog.getOpenFileName(
            parent = None,
            caption = "Select a data file",
            directory = os.getcwd(),
            filter = file_filter,
            initialFilter = file_filter
        )
        if response[0] != "":
            self.path = response[0]
            data = pd.read_csv(response[0])
            self.n_criteria = len(data.columns) - 2
            self.punkty.setHorizontalHeaderLabels(list(data.columns)[1:])
            for index,row in data.iterrows():
                newItem = QtGui.QStandardItem(row[1])
                self.punkty.appendRow(newItem)
                row_id = self.punkty.rowCount() - 1
                helper = []
                for i in range(1,len(data.columns)-1):
                    self.punkty.setData(self.punkty.index(row_id,i),float(row[i+1]))
                    helper.append(float(row[i+1]))
                self.lista_dan.append(tuple(helper))
        self.punktyView.resizeColumnsToContents()
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Wczytaj dane z pliku"))
        self.pushButton_2.setText(_translate("MainWindow", "Stwórz ranking"))
        self.label.setText(_translate("MainWindow", "Alternatywy z kryteriami"))
        self.label_2.setText(_translate("MainWindow", "Klasy"))
        self.label_3.setText(_translate("MainWindow", "Ranking"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
