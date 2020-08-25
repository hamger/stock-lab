import csv

def readCsvFile(path):
    res = []
    with open(path, 'r') as f:
        file = csv.reader(f)
        for line in file:
            res.append(line[0])
    return res