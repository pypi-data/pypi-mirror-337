import numpy as np

class Synapse:
    def __init__(self, pre_neuron, post_neuron, weight=None):
        self.pre_neuron = pre_neuron
        self.post_neuron = post_neuron
        self.weight = np.random.randn() * 0.01 if weight is None else weight

    def transmit_signal(self, signal):
        return self.weight * signal

    def update_weight(self, delta):
        self.weight += delta
