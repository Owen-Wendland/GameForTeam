import pickle
import os
import sys

cwd = os.getcwd()
cwd = str(cwd)
cwd = cwd.replace('src','')
print(cwd + '\\dat')
sys.path.append(cwd + '\\dat')

with open(cwd + "\\dat\\currentPerson.pkl", 'rb') as f:
    x = pickle.load(f)
print(x)
with open(cwd + "\\dat\\topTen.pkl", 'rb') as f:
    x = pickle.load(f)
print(x)