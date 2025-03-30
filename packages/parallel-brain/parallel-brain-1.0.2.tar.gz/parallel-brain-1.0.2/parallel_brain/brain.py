import numpy as np
from .neuron import Neuron
from .learning import hebbian_update, stdp_update

class ParallelBrainWithStabilizedThreshold:
    def __init__(self, num_neurons=100, threshold=0.5, stability_factor=0.1):
        self.neurons = [Neuron(threshold) for _ in range(num_neurons)]
        self.threshold = threshold
        self.stability_factor = stability_factor

    def forward(self, inputs):
        outputs = np.array([neuron.activate(inp) for neuron, inp in zip(self.neurons, inputs)])
        self.adapt_threshold(outputs)
        return outputs

    def adapt_threshold(self, outputs):
        avg_activity = np.mean(outputs)
        self.threshold += self.stability_factor * (avg_activity - self.threshold)

    def learn(self, pre_synaptic, post_synaptic):
        for neuron in self.neurons:
            hebbian_update(neuron, pre_synaptic, post_synaptic)
            stdp_update(neuron, pre_synaptic, post_synaptic)
