import numpy as np

def normalize(arr):
    return (arr - np.min(arr)) / (np.max(arr) - np.min(arr) + 1e-8)

def sigmoid(x):
    return 1 / (1 + np.exp(-x))
