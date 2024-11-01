# NarrativeConn2Res

## Method

Method used follows the Narrative Integration Reservoir experiment code from [Peter Dominey's repository](https://github.com/pfdominey/Narrative-Integration-Reservoir/).

- Create 4 reservoirs based on [Conn2Res connectomes](https://www.nature.com/articles/s41467-024-44900-4).
- Create comparison randomly connected reservoir with [ReservoirPy](https://reservoirpy.readthedocs.io/en/latest)
- Encode text from NotTheFall story using [Wikipedia2Vec](https://wikipedia2vec.github.io/wikipedia2vec/) and preprocess
- Feed encodings as timeseries into reservoirs and save resulting states
- Visualize autocorrelation of states
- Segment states states of reservoirs using Baldassano et al.'s [Hidden Markov Model](https://pubmed.ncbi.nlm.nih.gov/28772125/)

## Investigations

### Connectivity Matrices of Conn2Res Networks

![Alt text](results/Conn2Resconnectivities.png?v=2)

### Reservoir States for NotTheFall Narrative

![Alt text](results/statespernetwork.png?v=2)

### Autocorrelation by Network for NotTheFall Narrative

![Alt text](results/states_autocorr.png?v=2)

### HMM Segmentation Size by Network

![Alt text](results/segmentation_size.png?v=2)

### Reservoir State Alignment and Divergence by Network

![Alt text](results/alignment_divergence.png?v=2)

### Time Constants per Network

![Alt text](results/timeconsts-across-seeds.png?v=2)