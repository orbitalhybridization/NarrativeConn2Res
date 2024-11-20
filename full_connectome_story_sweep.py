# pull story embeddings
# embeddings_dir = '/home/ijackson/dynamics/sandbox/repos/NarrativeConn2Res/data/transcript_embeddings'
embeddings_dir = '/home/ijackson/dynamics/sandbox/repos/NarrativeConn2Res/data/transcript_embeddings_shifted'
import os
import numpy as np

from conn2res.connectivity import Conn
from conn2res.reservoir import EchoStateNetwork
from conn2res.readout import Readout
from conn2res import readout, plotting
from resUtils import networks_all, conn, nodes_path
from tqdm import tqdm

condition = 'shifted_embeddings' # 'original_embeddings'

story_embeddings_path_list = [os.path.join(embeddings_dir, x) for x in os.listdir(embeddings_dir)]

for i,story_embeddings_path in tqdm(enumerate(story_embeddings_path_list)):
    story_name = story_embeddings_path.split('/')[-1]
    print("Getting embeddings: ", story_name)

    random_story_embeddings = np.load(story_embeddings_path)

    # set up Conn2Res
    output_networks = networks_all
    nVectorDim = 100 # wiki2vec dimensionality

    # input nodes: limbic system
    input_nodes = nodes_from=conn.get_nodes('LIM', filename=nodes_path)

    # output nodes: varies
    output_nodes_all = {network: conn.get_nodes(network, filename=nodes_path) for network in output_networks}

    w_in = np.zeros((nVectorDim, conn.n_nodes))
    w_in[:, input_nodes] = np.eye(nVectorDim,input_nodes.shape[0])

    # alphas
    ALPHAS = np.linspace(0, 2, 11)[1:]
    ACT_FCN = 'tanh'

    # create echo state networks by output network and alpha
    esn_states = {network: {alpha: [] for alpha in ALPHAS} for network in output_networks}
    for alpha in tqdm(ALPHAS):
        print("Alpha: ", alpha)
        for network in output_networks:
            esn = EchoStateNetwork(w=conn.w, activation_function=ACT_FCN)
            esn.w = alpha * conn.w
            states = esn.simulate(ext_input=random_story_embeddings, w_in=w_in, 
                                output_nodes=output_nodes_all[network])
            esn_states[network][alpha] = states

    # now save the states to pkl
    import pickle
    states_dir = f'data/whole_connectome_states/{condition}'
    with open(f'{states_dir}/{story_name}.pkl', 'wb') as f:
        pickle.dump(esn_states, f)

