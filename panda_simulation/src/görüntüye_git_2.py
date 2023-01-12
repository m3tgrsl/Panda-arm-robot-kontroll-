#!/usr/bin/env python3
#-*- coding:utf-8 -*-
import sys
import subprocess
from PySide2.QtWidgets import QApplication, QPushButton

def run_code():
  subprocess.call(["python", "/home/m3t/catkin_sws/src/panda_simulation/src/görüntüye_git.py"])

# QApplication nesnesi oluşturma
app = QApplication(sys.argv)

# buton oluşturma ve gösterme
button = QPushButton("Kodu Çalıştır")
button.clicked.connect(run_code)
button.show()

# uygulamayı başlatma
sys.exit(app.exec_())

