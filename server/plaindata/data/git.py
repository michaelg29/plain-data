"""
    git connection
"""

import os

def saveFile(path, message):
    os.system('git add ' + path)
    os.system('git commit -m "' + message + '"')

def push():
    os.system('git push -all origin')