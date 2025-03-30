# Parallel Brain

Parallel Brain is a neural simulation framework with stabilized thresholds.

## Installation

Install the package via pip:

```bash
pip install parallel-brain

from parallel_brain import ParallelBrainWithStabilizedThreshold

# Create a brain model
brain = ParallelBrainWithStabilizedThreshold(num_neurons=1000)

# Stimulate some neurons
brain.stimulate_neurons([0, 1, 2], signal_strength=20.0)

# Run the simulation
brain.propagate_signals(steps=10)

---

### **5. `LICENSE`**
Use the MIT license for simplicity:
```plaintext
MIT License

Copyright (c) 2025 Darshan

Permission is hereby granted, free of charge, to any person obtaining a copy...
