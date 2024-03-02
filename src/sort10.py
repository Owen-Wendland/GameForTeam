import pickle
import os
import sys

cwd = os.getcwd()
cwd = str(cwd)
cwd = cwd.replace('src','')
sys.path.append(cwd + '\\dat')

#sets all to blank
'''
b = {
                "initial1": 'blank1',
                "team1": 'blank',
                "points1": 10,
                "initial2": 'blank2',
                "team2": 'blank',
                "points2": 9,
                "initial3": 'blank3',
                "team3": 'blank',
                "points3": 8,
                "initial4": 'blank4',
                "team4": 'blank',
                "points4": 7,
                "initial5": 'blank5',
                "team5": 'blank',
                "points5": 6,
                "initial6": 'blank6',
                "team6": 'blank',
                "points6": 5,
                "initial7": 'blank7',
                "team7": 'blank',
                "points7": 4,
                "initial8": 'blank8',
                "team8": 'blank',
                "points8": 3,
                "initial9": 'blank9',
                "team9": 'blank',
                "points9": 2,
                "initial10": 'blank10',
                "team10": 'blank',
                "points10": 1
            }

with open(cwd + "\\dat\\topTen.pkl", "wb") as f:
    pickle.dump(b, f)'''
    

with open(cwd + "\\dat\\currentPerson.pkl", 'rb') as f:
    x = pickle.load(f)
    
with open(cwd + "\\dat\\topTen.pkl", 'rb') as f:
    z = pickle.load(f)
with open(cwd + "\\dat\\topTen.pkl", 'rb') as f:
    a = pickle.load(f)
found = ''
pastp = z[('points1')]
pasti = z[('initial1')] 
pastt = z[('team1')]
for i in range(10):
    i = i+1
    if(x['points'] > z[('points' + str(i))] and found == ''):
        found = i
        pastp = z[('points' + str(i))]
        pasti = z[('initial' + str(i))] 
        pastt = z[('team' + str(i))]
        z[('points' + str(i))] = x['points']
        z[('initial' + str(i))] = x['initial']
        z[('team' + str(i))] = x['team']
    else:
        z[('points' + str(i))] = pastp
        z[('initial' + str(i))] = pasti
        z[('team' + str(i))] = pastt
        pastp = a[('points' + str(i))]
        pasti = a[('initial' + str(i))] 
        pastt = a[('team' + str(i))]

if(found != ''):
    with open(cwd + "\\dat\\topTen.pkl", "wb") as f:
                    f.truncate(0)
                    pickle.dump(z, f)