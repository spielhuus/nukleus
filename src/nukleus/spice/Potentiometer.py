from ..Circuit import SubCircuit


class Potentiometer(SubCircuit):
    def __init__(self, name: str, R: float, w: float, **kwargs):
        super().__init__(name, ['n1', 'n2', 'n3'])
        self.__R = R
        self.__w = w

        self.R('1', 'n1', 'n2', str(R * w))
        self.R('2', 'n2', 'n3', str(R * (1.0-w)))

    def wiper(self, w):
        if w == 0:
            self.R1.value = self.__R * 0.0000001
            self.R2.value = self.__R * 0.9999999
        elif w == 1:
            self.R1.value = self.__R * 0.9999999
            self.R2.value = self.__R * 0.0000001
        else:
            self.R1.value = self.__R * w
            self.R2.value = self.__R * (1.0-w)
