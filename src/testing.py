import pickle
import os
import sys

cwd = os.getcwd()
cwd = str(cwd)
cwd = cwd.replace('src','')
print(cwd + '\\dat')
sys.path.append(cwd + '\\dat')

with open(cwd + "\\dat\\currentPerson.pkl", 'rb') as f:
    f.truncate(0)
    x = pickle.load(f)
print(x)