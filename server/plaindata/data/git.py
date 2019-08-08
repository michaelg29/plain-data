"""
    git connection
"""

import os

"""
    adds file to git and commits to repository
"""
def saveFile(path, message):
    os.system('git add ' + path)
    os.system('git commit -m "' + message + '"')

"""
    pushes all commits through master branch
"""
def push():
    os.system('git push --all origin')