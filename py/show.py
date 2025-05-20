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

    f, ((ax1, ax2, ax3), (ax4, ax5, ax6)) = plt.subplots(2, 3)

    f1 = ax1.pcolormesh(n, p, r, shading='auto')
    ax1.set_xscale('log')
    ax1.set_yscale('log')
    ax1.set_title('Average node count of largest connected component')

    n_space = settings.get_n_space()
    def line(x):
        return np.log(x) / x

    p_values = line(n_space)
    ax1.plot(n_space, p_values, color='red', linewidth=2, label='y = x')

    v = np.array(
        [np.average([int(r.cycle_count == 1) for r in results]) for _, n, p, results in data],
        dtype=np.float64
    ).reshape((settings.space_size, settings.space_size))
    f2 = ax2.pcolormesh(n, p, v, shading='auto')
    ax2.set_xscale('log')
    ax2.set_yscale('log')
    ax2.set_title('How many graphs are 2-connected')

    v = np.array(
        [np.average([
            ((r.graph_edge_count - r.visited_edge_count) / r.graph_edge_count if r.graph_edge_count != 0 else 0)
            for r in results]) for _, n, p, results in data],
        dtype=np.float64
    ).reshape((settings.space_size, settings.space_size))
    f3 = ax3.pcolormesh(n, p, v, shading='auto')
    ax3.set_xscale('log')
    ax3.set_yscale('log')
    ax3.set_title('Average amount of bridges')

    v = np.array(
        [np.std([
            ((r.graph_edge_count - r.visited_edge_count) / r.graph_edge_count if r.graph_edge_count != 0 else 0)
            for r in results]) for _, n, p, results in data],
        dtype=np.float64
    ).reshape((settings.space_size, settings.space_size))
    f4 = ax4.pcolormesh(n, p, v, shading='auto')
    ax4.set_xscale('log')
    ax4.set_yscale('log')
    ax4.set_title('bridges std deviation')

    def find_closest(needed_p, needed_n):
        _, n, p, results = min(data, key=lambda t: ((t[1] - needed_n)**2 + (t[2] - needed_p)**2))
        return n, p, results

    def onclick(event):
        if event.name != 'button_press_event':
            return
        if event.inaxes != ax3:
            return

        print(f'x={event.xdata}, y={event.ydata}')
        n, p, results = find_closest(event.ydata, event.xdata)
        print(f'{n=} {p=}')
        ax5.clear()
        ax5.hist(
            [(r.graph_edge_count - r.visited_edge_count) / r.graph_edge_count if r.graph_edge_count != 0 else 0 for r in results],
            bins=20,
            range=(0, 1)
        )
        plt.show()


    cid = f.canvas.mpl_connect('button_press_event', onclick)

    f.colorbar(f1, ax=ax1)
    f.colorbar(f2, ax=ax2)
    f.colorbar(f3, ax=ax3)
    f.colorbar(f4, ax=ax4)
    plt.show()

