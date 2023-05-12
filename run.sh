#!/bin/bash
cd src
pyrcc5 resources/res.qrc -o res.py
python main.py