import numpy as np

class SimpleNeuralNetwork:
    def __init__(self, input_size):
        self.w = np.random.randn(input_size)
        self.b = 0.0

    def sigmoid(self, z):
        return 1 / (1 + np.exp(-z))

    def forward(self, x):
        z = np.dot(x, self.w) + self.b
        y_hat = self.sigmoid(z)
        return y_hat


if __name__ == "__main__":
    np.random.seed(42)

    num_samples = 100
    x = np.random.randn(num_samples, 2)
    y = (2 * x[:, 0] + x[:, 1] - 1 > 0).astype(int)

    nn = SimpleNeuralNetwork(input_size=2)

    predictions = nn.forward(x)

    print("Sample inputs (x):")
    print(x[:5])

    print("\nCorresponding true labels (y):")
    print(y[:5])

    print("\nPredictions (y-hat) from the untrained model:")
    print(predictions[:5])
