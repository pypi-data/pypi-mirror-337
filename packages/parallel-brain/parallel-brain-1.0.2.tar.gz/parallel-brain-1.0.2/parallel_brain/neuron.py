import numpy as np

class Neuron:
    def __init__(self, threshold=0.5):
        self.threshold = threshold
        self.weights = np.random.randn(10) * 0.01  # Small random weights

    def activate(self, inputs):
        net_input = np.dot(self.weights, inputs)
        return 1 if net_input > self.threshold else 0

    def update_weights(self, delta):
        self.weights += delta
