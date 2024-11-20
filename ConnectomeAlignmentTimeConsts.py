import numpy as np
import pickle
import os

originalStates = pickle.load(open('./data/whole_connectome_states/original_embeddings/sherlock_transcript_embeddings.npy.pkl', 'rb'))
shiftedStates = pickle.load(open('./data/whole_connectome_states/shifted_embeddings/sherlock_transcript.npy.pkl', 'rb'))

# now get the time constants for each RSN and alpha value
import resUtils as rutils
from tqdm import tqdm

networks = rutils.networks_all
alphas = np.linspace(0, 2, 11)[1:]

all_data = []
# each story has a different point of shift, so we need to find that (should be 20% and 60%)
# for each story, find the point of shift
window_size = 20
timeconstants = {networks: {alphas: [] for alphas in alphas} for networks in networks}
for i, network in tqdm(enumerate(networks)):
    for j, alpha in enumerate(alphas):
        original = originalStates[network][alpha]
        shifted = shiftedStates[network][alpha]

        # find the point of return from shift based on the length of the states
        convergence_point = int(len(original) * 0.6)

        data = original[convergence_point-window_size:] - shifted[convergence_point-window_size:]

        dataT = data.T

        # get the time constant, which is time for the data to reach 1/2 of the original value
        taus = np.zeros(dataT.shape[0])
        res_maxes = np.zeros(dataT.shape[0])

        #calculate the alignment time:  dataT(neurons,time)
        #interate over reservoir neuron
        for neuron in range(dataT.shape[0]):
            # get the value
            max = abs(dataT[neuron,0])
            if max > -1:  #WAS 0.05
                for timestep in range(dataT.shape[1]):
                    if abs(dataT[neuron,timestep]) < max/2:
                        taus[neuron] = timestep
                        res_maxes[neuron] = max
                        max=-1
        
        # normalize by network size?
        # timeconstants = timeconstants / len(timeconstants)
        timeconstants[network][alpha] = taus # better way to do this?

# now we have the time constants for each RSN and alpha value
dynamical_regimes = {'stable': alphas[0:3], 'critical': alphas[3:6], 'chaotic': alphas[6:9]}
densities = rutils.nonzero_densities
normalize_by_density = False
order = {"VIS","SM","DA","VA","LIM","FP","DMN"} # use order from the paper

# now we can create boxplots for each RSN in a single plot, with three subplots for each dynamical regime

import matplotlib.pyplot as plt

fig, axs = plt.subplots(1, 3, figsize=(20, 10))

for i, regime in enumerate(dynamical_regimes):
    ax = axs[i]
    ax.set_title(regime)
    ax.set_ylabel('Time Constant')
    ax.set_xticklabels(order)
    ax.set_xticks(range(7))
    for j, network in enumerate(order):
        data = [timeconstants[network][alpha] for alpha in dynamical_regimes[regime]]
        # average the time constants across alpha values for each network
        data = [np.mean(data, axis=0)]
        ax.boxplot(data, positions=[j], showfliers=False)

# save
plt.savefig('./results/connectome_timeconstants_boxplot.png')