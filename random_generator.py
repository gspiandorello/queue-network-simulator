class PseudoRandomNumberGenerator:
    def __init__(self, quantity, seed):
        self.quantity = quantity
        self.seed = seed
        self.a = 1664525
        self.c = 1013904223
        self.M = 2**32

    def generate(self):
        self.seed = (self.a * self.seed + self.c) % self.M
        return self.seed / self.M
        # numbers = []
        # for _ in range(self.quantity):
        #     self.seed = (self.a * self.seed + self.c) % self.M
        #     numbers.append(self.seed / self.M)
        # return numbers
