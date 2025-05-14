from main import *
import matplotlib.pyplot as plt
import sys

if __name__ == '__main__':
    fname = sys.argv[1]
    with open(fname, 'rb') as f:
        data = pickle.load(f)
    
    for i, n, p, result in data:
        if result is not None:
            s = sum(d.cycle_count for d in result)
            if s != 1000:
                print(i, s)
    data_processed = [(a, b) for a, b in data]

    print(data)
