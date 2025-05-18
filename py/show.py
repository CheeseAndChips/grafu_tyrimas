from main import *
import matplotlib.pyplot as plt
import sys
import numpy as np

if __name__ == '__main__':
    fname = sys.argv[1]
    with open(fname, 'rb') as f:
        (settings, data) = pickle.load(f)

    dtype = np.dtype([('n', np.int64), ('p', np.float64), ('r', np.float64)])

    d = np.array(
        [(n, p, (np.average([r.graph_node_count for r in results])) / n) for i, n, p, results in data],
        dtype=dtype
    ).reshape((settings.space_size, settings.space_size))

    n, p, r = d['n'], d['p'], d['r']

    plt.subplot(2, 2, 1)
    plt.pcolormesh(n, p, r, shading='auto')
    plt.xscale('log')
    plt.yscale('log')
    plt.title('Average node count largest connected component')

    n_space = settings.get_n_space()

    def line(x):
        return np.log(x) / x

    p_values = line(n_space)

    plt.plot(n_space, p_values, color='red', linewidth=2, label='y = x')
    # plt.show()

    plt.subplot(2, 2, 2)
    v = np.array(
        [np.average([int(r.cycle_count == 1) for r in results]) for _, n, p, results in data],
        dtype=np.float64
    ).reshape((settings.space_size, settings.space_size))
    plt.pcolormesh(n, p, v, shading='auto')
    plt.xscale('log')
    plt.yscale('log')
    plt.title('How many graphs are 2-connected')
    # plt.show()

    plt.subplot(2, 2, 3)
    v = np.array(
        [np.average([
            ((r.graph_edge_count - r.visited_edge_count) / r.graph_edge_count if r.graph_edge_count != 0 else 0)
            for r in results]) for _, n, p, results in data],
        dtype=np.float64
    ).reshape((settings.space_size, settings.space_size))
    plt.pcolormesh(n, p, v, shading='auto')
    plt.xscale('log')
    plt.yscale('log')
    plt.title('Average amount of bridges')
    plt.show()

