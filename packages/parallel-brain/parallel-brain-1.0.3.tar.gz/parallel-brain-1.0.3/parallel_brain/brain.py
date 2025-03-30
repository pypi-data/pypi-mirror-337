import numpy as np
from .neuron import Neuron
from .learning import hebbian_update, stdp_update

class ParallelBrainWithStabilizedThreshold:
    """
    A neural model implementing:
    - Hebbian Learning for synaptic plasticity
    - STDP (Spike-Timing-Dependent Plasticity) for time-based adaptation
    - Adaptive threshold stabilization
    - Parallel neuron activation
    """

    def __init__(self, num_neurons=100, threshold=0.5, stability_factor=0.1):
        """
        Initialize the Parallel Brain Model.

        Parameters:
        - num_neurons (int): Number of neurons in the model.
        - threshold (float): Initial firing threshold.
        - stability_factor (float): Factor controlling threshold adaptation.
        """
        self.num_neurons = num_neurons
        self.neurons = [Neuron(threshold) for _ in range(num_neurons)]
        self.threshold = threshold
        self.stability_factor = stability_factor

    def forward(self, inputs):
        """
        Compute forward pass for the neural network.

        Parameters:
        - inputs (array-like): Input vector.

        Returns:
        - outputs (numpy array): Activation values of neurons.
        """
        if len(inputs) != self.num_neurons:
            raise ValueError(f"Input size mismatch! Expected {self.num_neurons}, got {len(inputs)}")

        outputs = np.array([neuron.activate(inp) for neuron, inp in zip(self.neurons, inputs)])
        self.adapt_threshold(outputs)
        return outputs

    def adapt_threshold(self, outputs):
        """
        Dynamically adjust the neuron firing threshold based on activity.

        Parameters:
        - outputs (numpy array): Activation values of neurons.
        """
        avg_activity = np.mean(outputs)
        self.threshold += self.stability_factor * (avg_activity - self.threshold)

    def learn(self, pre_synaptic, post_synaptic):
        """
        Apply Hebbian Learning and STDP to adjust weights.

        Parameters:
        - pre_synaptic (numpy array): Pre-synaptic neuron activations.
        - post_synaptic (numpy array): Post-synaptic neuron activations.
        """
        for neuron in self.neurons:
            hebbian_update(neuron, pre_synaptic, post_synaptic)
            stdp_update(neuron, pre_synaptic, post_synaptic)
