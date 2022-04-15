from ..Circuit import SubCircuit


class Potentiometer(SubCircuit):
    """Potentiometer spice model."""
    def __init__(self, name: str, R: float, wiper_position: float):
        super().__init__(name, ['n1', 'n2', 'n3'])
        self._resistance = R
        self._w = wiper_position

        self.R('1', 'n1', 'n2', str(R * wiper_position))
        self.R('2', 'n2', 'n3', str(R * (1.0-wiper_position)))

    def wiper(self, wiper_positioniper_position: float):
        """
        Set the wiper position.

        :param w float: position 0.0 - 1.0.
        """
        if wiper_positioniper_position == 0:
            self.R1.value = str(self._resistance * 0.0000001)
            self.R2.value = str(self._resistance * 0.9999999)
        elif wiper_positioniper_position == 1:
            self.R1.value = str(self._resistance * 0.9999999)
            self.R2.value = str(self._resistance * 0.0000001)
        else:
            self.R1.value = str(self._resistance * wiper_positioniper_position)
            self.R2.value = str(self._resistance * (1.0-wiper_positioniper_position))
