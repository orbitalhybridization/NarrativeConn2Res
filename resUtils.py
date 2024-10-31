import numpy as np
import reservoirpy as rpy
from conn2res.connectivity import Conn

networks_all = {"DA":"Dorsal Attention","DMN":"Default Mode Network","FP":"Frontoparietal","LIM":"Limbic","SM":"Somatomotor","VA":"Ventral Attention","VIS":"Visual"}

def createConn2ResReservoirs(networks=None, seed=1, lr=0.05, sr=1.0, input_connectivity=0.5, activation='tanh', 
                            vectorDim=100, Win_random_weight=True, include_baseline=True):

    if networks is None:
        networks = networks_all
    
    else:
        networks = {n:networks_all[n] for n in networks}

    # load connectivity data of one subject
    connectivity_path = '../../../conn2res/examples/data/human/connectivity.npy'
    conn = Conn(filename=connectivity_path, subj_id=0)

    # scale conenctivity weights between [0,1] and normalize by spectral radius
    conn.scale_and_normalize() # this makes the spectral radius 1, which we can modify with alpha later

    # get path of network labels for each node
    nodes_path = '../../../conn2res/examples/data/human/rsn_mapping.npy'

    # Init reservoirs with networks from Conn2Res
    rpy.verbosity(0)
    rpy.set_seed(seed)
    # get the connectivity matrix (w) for each network
    # and make an input matrix (w_in) that maps from the input to the network
    # then pass these into reservoirpy
    reservoirs = {network: None for network in networks}
    for network in networks:
        nodes = conn.get_nodes(network,filename=nodes_path)
        W = conn.w[np.ix_(nodes,nodes)]
        nNodes = W.shape[0]
        if Win_random_weight:
            Win = np.random.rand(nNodes, vectorDim) - 0.5
        else:
            Win = np.ones((nNodes, vectorDim))
        # we might want to make this a sparse matrix
        res = rpy.nodes.Reservoir(lr=lr, sr=sr, W=W, Win=Win, input_connectivity=input_connectivity,
                                seed=seed, activation=activation)
        reservoirs[network] = res
        
    if include_baseline:
        reservoirs["Baseline"] = rpy.nodes.Reservoir(vectorDim, lr=lr, sr=sr, seed=seed, input_connectivity=input_connectivity, activation=activation)

    return reservoirs

def simulateReservoirs(reservoirs, inputData):

    # simulate reservoirs
    states = {network: None for network in reservoirs}
    for network in reservoirs:
        res = reservoirs[network]
        states[network] = res.run(inputData)

    # if include_original_res_states:
    #     states["Baseline"] = np.load('reservoirStatesBuffer.npy') # import states from original NIR code
    #     # NOTE: this does not use the baseline res created above. might want to change/investigate this later

    return states