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

import csv

from PyQt5.QtWidgets import *


def retrieve_string(form_widget):
    if isinstance(form_widget, QLineEdit):
        return form_widget.text()

    elif isinstance(form_widget, QDateEdit):
        return form_widget.date().toString("yyyy-MM-dd")

    elif isinstance(form_widget, QComboBox):
        return (
            form_widget.itemText(form_widget.currentIndex())
            if form_widget.currentIndex()
            else ""
        )

    elif isinstance(form_widget, QPlainTextEdit):
        return form_widget.toPlainText()

    elif isinstance(form_widget, QSlider):
        WATER_COLOURS = [
            "blue",
            "blue-green",
            "light green",
            "dark green",
            "green-brown",
            "brown",
            "grey",
        ]
        return WATER_COLOURS[form_widget.value()]


def csv_append_row(filename, headers, row):
    # read the headers
    try:
        with open(filename, "r") as f:
            reader = csv.reader(f)
            if not any(reader):
                existing_headers = []
            else:
                f.seek(0)
                existing_headers = next(reader)
    except FileNotFoundError:
        existing_headers = []

    # headers match
    if existing_headers == headers:
        with open(filename, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(row)
    else:
        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(headers)

            if existing_headers:
                for row in reader:
                    writer.writerow(row)
            writer.writerow(row)
