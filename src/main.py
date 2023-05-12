"""
SlidexCell - improved data collection of environmental observations in any weather
Copyright © 2023 Nabeth Ghazi

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, version 3.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

import os
import sys

from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

import export
import res  # pyrcc5 resources\res.qrc -o res.py
import scanner


def prev():
    widget.setCurrentIndex(widget.currentIndex() - 1)


def next():
    widget.setCurrentIndex(widget.currentIndex() + 1)


def home():
    while widget.count() > 1:
        temp = widget.widget(1)
        widget.removeWidget(temp)
        temp.deleteLater()

    widget.setCurrentIndex(0)


def info():
    os.startfile("resources\\docs\\standard-operating-procedures.pdf")


class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("main.ui", self)
        self.new_entry.clicked.connect(self.gen_screens)
        self.instructions.clicked.connect(info)
        self.about.clicked.connect(self.about_clicked)

    def gen_screens(self):
        form_screens = [
            Screen1(),
            Screen2(),
            Screen3(),
            Screen4(),
            Screen5(),
            Screen6(),
        ]
        for screen in form_screens:
            widget.addWidget(screen)
        next()

    def about_clicked(self):
        os.startfile("..\\docs\\one-pager.pdf")


class Screen1(QDialog):
    def __init__(self):
        super(Screen1, self).__init__()
        loadUi("screen1.ui", self)
        self.prev.clicked.connect(prev)
        self.home.clicked.connect(home)
        self.next.clicked.connect(next)
        self.info.clicked.connect(info)
        self.use_device.clicked.connect(self.use_device_checked)

    def use_device_checked(self):
        if self.use_device.isChecked():
            self.collector.setText("John Doe")
            self.collector.setEnabled(False)
            self.collectionDate.setDate(QDate.currentDate())
            self.collectionDate.setEnabled(False)
            self.locationName.setCurrentIndex(1)
            self.locationName.setEnabled(False)

        else:
            self.collector.setEnabled(True)
            self.collectionDate.setEnabled(True)
            self.locationName.setEnabled(True)


class Screen2(QDialog):
    def __init__(self):
        super(Screen2, self).__init__()
        loadUi("screen2.ui", self)
        self.prev.clicked.connect(prev)
        self.home.clicked.connect(home)
        self.next.clicked.connect(next)
        self.info.clicked.connect(info)
        self.scan.clicked.connect(self.scan_pushed)

    def scan_pushed(self):
        entries = scanner.cam_scan()

        fields = (self.chlorine, self.bromine, self.ph, self.alkalinity, self.hardness)

        for i, field in enumerate(fields):
            if i < len(entries):
                field.setText(entries[i])


class Screen3(QDialog):
    def __init__(self):
        super(Screen3, self).__init__()
        loadUi("screen3.ui", self)
        self.prev.clicked.connect(prev)
        self.home.clicked.connect(home)
        self.next.clicked.connect(next)
        self.info.clicked.connect(info)
        self.info_2.clicked.connect(info)


class Screen4(QDialog):
    def __init__(self):
        super(Screen4, self).__init__()
        loadUi("screen4.ui", self)
        self.prev.clicked.connect(prev)
        self.home.clicked.connect(home)
        self.next.clicked.connect(next)
        self.info.clicked.connect(info)


class Screen5(QDialog):
    def __init__(self):
        super(Screen5, self).__init__()
        loadUi("screen5.ui", self)
        self.prev.clicked.connect(prev)
        self.home.clicked.connect(home)
        self.next.clicked.connect(next)
        self.info.clicked.connect(info)


class Screen6(QDialog):
    def __init__(self):
        super(Screen6, self).__init__()
        loadUi("screen6.ui", self)
        self.prev.clicked.connect(prev)
        self.home.clicked.connect(home)
        self.info.clicked.connect(info)
        self.sub.clicked.connect(self.gen_csv)

    def gen_csv(self):
        path = "..\\output\\database.csv"

        # generate excel
        with open("resources\\docs\\fields.txt", "r") as f:
            headers = [line.strip() for line in f.readlines()]

        entries = []
        for i, header in enumerate(headers):
            var_name = header.split()[0]
            var_name = var_name[0].lower() + var_name[1:]

            if i < 3:
                entries.append(
                    export.retrieve_string(getattr(widget.widget(1), var_name))
                )
            elif i < 9:
                entries.append(
                    export.retrieve_string(getattr(widget.widget(2), var_name))
                )
            elif i < 13:
                entries.append(
                    export.retrieve_string(getattr(widget.widget(3), var_name))
                )
            elif i < 16:
                entries.append(
                    export.retrieve_string(getattr(widget.widget(4), var_name))
                )
            elif i < 22:
                entries.append(
                    export.retrieve_string(getattr(widget.widget(5), var_name))
                )
            else:
                entries.append(
                    export.retrieve_string(getattr(widget.widget(6), var_name))
                )

        export.csv_append_row(path, headers, entries)

        os.startfile(path)
        home()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    widget = QStackedWidget()

    screens = [MainWindow()]
    widget.addWidget(screens[0])

    widget.setFixedWidth(480)
    widget.setFixedHeight(870)
    widget.show()

    try:
        sys.exit(app.exec())
    except:
        exit()
