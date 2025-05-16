from main import *
import matplotlib.pyplot as plt
import sys
import numpy as np

if __name__ == '__main__':
    fname = sys.argv[1]
    with open(fname, 'rb') as f:
        data = pickle.load(f)

    dtype = np.dtype([('n', np.int64), ('p', np.float64), ('r', np.float64)])
    
    d = np.array(
        [(n, p, (np.average([r.graph_node_count for r in results])) / n) for i, n, p, results in data],
        dtype=dtype
    ).reshape((30, 30))

    n, p, r = d['n'], d['p'], d['r']

    plt.pcolormesh(n, p, r, shading='auto')
    plt.xscale('log')
    plt.yscale('log')

    n_space = np.round(np.logspace(2.5, 2, num=30)).astype(int)

    def line(x):
        return np.log(x) / x

    p_values = line(n_space)

    plt.plot(n_space, p_values, color='red', linewidth=2, label='y = x')
    plt.show()

    v = np.array(
        [sum(r.cycle_count == 1 for r in results) for _, n, p, results in data],
        dtype=np.float64
    ).reshape((30, 30))
    plt.pcolormesh(n, p, v, shading='auto')
    plt.xscale('log')
    plt.yscale('log')
    plt.show()

    v = np.array(
        [np.average([
            ((r.graph_edge_count - r.visited_edge_count) / r.graph_edge_count if r.graph_edge_count != 0 else 0)
            for r in results]) for _, n, p, results in data],
        dtype=np.float64
    ).reshape((30, 30))
    plt.pcolormesh(n, p, v, shading='auto')
    plt.xscale('log')
    plt.yscale('log')
    plt.show()

