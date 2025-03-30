import torch

class ParallelBrainWithStabilizedThreshold:
    def __init__(self, num_neurons, avg_connections=500, decay=0.95, base_threshold=50.0):
        self.num_neurons = num_neurons
        self.decay = decay
        self.base_threshold = base_threshold

        # Initialize neuron states
        self.potentials = torch.zeros(num_neurons, device='cuda')
        self.thresholds = torch.ones(num_neurons, device='cuda') * base_threshold
        self.refractory = torch.zeros(num_neurons, dtype=torch.int, device='cuda')
        self.firing_activity = torch.zeros(num_neurons, device='cuda')

        # Create sparse connectivity matrix
        row_indices = torch.randint(0, num_neurons, (avg_connections * num_neurons,), device='cuda')
        col_indices = torch.arange(num_neurons, device='cuda').repeat_interleave(avg_connections)
        weights = torch.rand(avg_connections * num_neurons, device='cuda') * 3.0 + 1.0  # ✅ Lowered weight range (1.0 - 4.0)

        indices = torch.stack([row_indices, col_indices])
        self.connection_weights = torch.sparse_coo_tensor(
            indices, weights, size=(num_neurons, num_neurons), device='cuda'
        )

    def stimulate_neurons(self, neuron_ids, signal_strength=20.0):
        """Provide initial stimulation to selected neurons."""
        self.potentials[neuron_ids] += signal_strength

    def propagate_signals(self, steps=10):
        """Propagate signals dynamically through the network."""
        for step in range(steps):
            active_neurons = self.refractory == 0

            # Signal propagation via sparse matrix multiplication
            signals = torch.sparse.mm(self.connection_weights, self.potentials.unsqueeze(1)).squeeze()
            signals = signals * active_neurons  

            # ✅ Apply stricter signal cap
            signals = torch.clamp(signals, min=0, max=2500)  # 🔹 Lowered from 5000 to 2500

            # 🔹 Introduce balanced background noise
            noise = torch.randn(self.potentials.size(), device='cuda') * 0.3
            self.potentials += noise

            # 🔥 Determine firing neurons
            fired_neurons = signals >= self.thresholds
            self.firing_activity = self.firing_activity * 0.9 + fired_neurons.float() * 0.1

            # ✅ Limit excessive firings (40% cap)
            max_firing = int(self.num_neurons * 0.40)  
            if fired_neurons.sum() > max_firing:
                top_indices = torch.argsort(signals, descending=True)[:max_firing]
                fired_neurons = torch.zeros_like(fired_neurons, device='cuda')
                fired_neurons[top_indices] = 1

            # ⏳ Refractory period update
            self.refractory = torch.where(
                fired_neurons,
                torch.randint(1, 3, (self.num_neurons,), device='cuda'),
                torch.clamp(self.refractory - 1, min=0)
            )

            # 🛠 Adaptive threshold modulation
            self.thresholds = torch.where(self.firing_activity > 0.5, self.thresholds * 1.01, self.thresholds * 0.99)
            self.thresholds = torch.clamp(self.thresholds, min=40.0, max=100.0)  # 🔹 Increased minimum threshold to 40

            # 🏋️ Weight stabilization
            avg_weight = torch.mean(self.connection_weights._values())
            weight_scaling = 2.0 / avg_weight if avg_weight > 2.0 else 1.0
            self.connection_weights = self.connection_weights * weight_scaling

            # 🚨 Prevent neuron death (restore activity if too low)
            inactive_neurons = self.potentials < 1.0
            self.potentials[inactive_neurons] += 5.0  

            # ⚖️ Apply smoother decay
            self.potentials = self.potentials * 0.97  

            # 🔹 Keep potentials within bounds
            self.potentials = torch.clamp(self.potentials, min=0.0, max=50.0)

            # 📊 Debugging info
            max_signal = torch.max(signals).item()
            mean_signal = torch.mean(signals).item()
            max_threshold = torch.max(self.thresholds).item()

            print(f"Step {step + 1}/{steps} | Mean Signal: {mean_signal:.2f}, "
                  f"Max Signal: {max_signal:.2f}, Max Threshold: {max_threshold:.2f}, Neurons Fired: {fired_neurons.sum().item()}")

            # 🛑 Stop if all neurons are inactive
            if torch.max(self.potentials) == 0:
                print("⚠️ All neurons have zero potential! Adjust stimulation, decay, or inhibition.")
                break

# ================================
# 🧠 Run Version 3.1 Neural Model
# ================================
num_neurons = 10_000
avg_connections = 500
steps = 50

# Create brain model
brain = ParallelBrainWithStabilizedThreshold(num_neurons=num_neurons, avg_connections=avg_connections)

# Stronger stimulation for testing
stimulated_neurons = torch.randint(0, num_neurons, (100,), device='cuda')  # 100 randomly selected neurons
brain.stimulate_neurons(stimulated_neurons, signal_strength=20.0)

# Run simulation
brain.propagate_signals(steps=steps)

# Output final neuron potentials
print("\nPotentials of the first 10 neurons after simulation:")
for i in range(10):
    print(f"Neuron {i}: Potential = {brain.potentials[i].item():.2f}")
