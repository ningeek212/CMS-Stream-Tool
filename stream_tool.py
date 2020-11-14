import sys
import ctf_game_parser

import PyQt5.QtWidgets as QtWidgets
from PyQt5.QtCore import Qt


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("CMS Stream Tool")

        team1_edit = QtWidgets.QLineEdit()
        team2_edit = QtWidgets.QLineEdit()
        team_layout = QtWidgets.QFormLayout()
        team_layout.addRow(self.tr("&Red Team:"), team1_edit)
        team_layout.addRow(self.tr("&Blue Team:"), team2_edit)

        map1_edit = QtWidgets.QLineEdit()
        map2_edit = QtWidgets.QLineEdit()
        map3_edit = QtWidgets.QLineEdit()
        map_layout = QtWidgets.QFormLayout()
        map_layout.addRow(self.tr("&Map 1:"), map1_edit)
        map_layout.addRow(self.tr("&Map 2:"), map2_edit)
        map_layout.addRow(self.tr("&Map 3:"), map3_edit)

        input_layout = QtWidgets.QVBoxLayout()
        input_layout.addWidget(QtWidgets.QLabel("Teams:"))
        input_layout.addLayout(team_layout)
        input_layout.addWidget(QtWidgets.QLabel("Maps:"))
        input_layout.addLayout(map_layout)

        widget = QtWidgets.QWidget()
        widget.setLayout(input_layout)
        self.setCentralWidget(widget)


app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec_()
