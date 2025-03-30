def hebbian_update(neuron, pre_synaptic, post_synaptic, lr=0.01):
    delta = lr * pre_synaptic * post_synaptic
    neuron.update_weights(delta)

def stdp_update(neuron, pre_synaptic, post_synaptic, lr=0.01):
    if post_synaptic > pre_synaptic:
        delta = lr * abs(post_synaptic - pre_synaptic)
    else:
        delta = -lr * abs(pre_synaptic - post_synaptic)
    neuron.update_weights(delta)
