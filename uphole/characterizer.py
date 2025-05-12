import math

label_names = ["Chalk", "Clay"]

class Chalk_Characterizer:
    def __init__(self, w_r, w_g, w_b, bias):
        self.w_r = w_r
        self.w_g = w_g
        self.w_b = w_b
        self.bias = bias

    def sigmoid(self, x):
        return 1 / (1 + math.exp(-x))

    def characterize(self, r, g, b):
        z = self.w_r * r + self.w_g * g + self.w_b * b + bias
        prob = self.sigmoid(z)
        return label_names[1] if prob >= 0.5 else label_names[0]
