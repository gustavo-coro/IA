'''

### Code and Library by https://github.com/lantunes
### Library at https://github.com/lantunes/netomaton/tree/master
### Or by pip 'pip install netomaton'

'''


import netomaton as ntm
import numpy as np

def patch_asscalar(a):
    return a.item()

def ler_arquivo(file_path:str) -> list:
    num_cidades = np.loadtxt(file_path, delimiter=' ', skiprows=0, max_rows=1, dtype=int)
    cordenadas = np.loadtxt(file_path, delimiter=' ', skiprows=1, dtype=float)

    coords_list = list()

    for i in range(num_cidades):
        xd = cordenadas[i][0]
        yd = cordenadas[i][1]
        coords_list.append((xd, yd))

    return coords_list


if __name__ == "__main__":

    setattr(np, "asscalar", patch_asscalar)

    points = ler_arquivo('instancia.txt')

    A, B, C, D, n, dt, timesteps = 500, 500, 200, 500, 15, 1e-05, 1000  
    # A, B, C, D, n, dt, timesteps = 300, 300, 100, 300, 12, 1e-05, 1000  
    # A, B, C, D, n, dt, timesteps = 400, 400, 150, 400, 12, 1e-05, 1000  
    # A, B, C, D, n, dt, timesteps = 500, 500, 150, 300, 12, 1e-05, 1000  

    tsp_net = ntm.HopfieldTankTSPNet(points, dt=dt, A=A, B=B, C=C, D=D, n=n)

    adjacency_matrix = tsp_net.adjacency_matrix

    # -0.022 was chosen so that the sum of V for all nodes is 10; some noise is added to break the symmetry
    initial_conditions = [-0.022 + np.random.uniform(-0.1*0.02, 0.1*0.02) for _ in range(len(adjacency_matrix))]

    trajectory = ntm.evolve(initial_conditions=initial_conditions, activity_rule=tsp_net.activity_rule,
                            network=ntm.topology.from_adjacency_matrix(adjacency_matrix), timesteps=timesteps)

    ntm.animate_activities(trajectory, shape=(10, 10))

    activities = ntm.get_activities_over_time_as_list(trajectory)
    permutation_matrix = tsp_net.get_permutation_matrix(activities)
    #print(permutation_matrix)

    G, pos, length = tsp_net.get_tour_graph(points, permutation_matrix)

    print(length)

    tsp_net.plot_tour(G, pos)