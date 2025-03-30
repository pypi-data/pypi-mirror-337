# Parallel Brain 🧠

A brain-inspired AI framework implementing Hebbian learning, STDP, and stabilized threshold mechanisms.

## Installation
```sh


##usage
pip install parallel-brain
from parallel_brain import ParallelBrainWithStabilizedThreshold

brain = ParallelBrainWithStabilizedThreshold(num_neurons=10)
inputs = [0.5] * 10
output = brain.forward(inputs)
print(output)
