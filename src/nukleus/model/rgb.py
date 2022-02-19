from typing import Tuple, Any

class rgb():
    def __init__(self, r: float, g: float, b: float, a: float):
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    def get_hex(self) -> str:
        return "#{int(r, 16)}{int(g, 16)}{int(b, 16)}{int(a*100, 16)}"

    def get(self) -> Tuple[float, float, float, float]:
        return (self.r, self.g, self.b, self.a)

    def __eq__(self, other: Any) -> Any:
        return self.r == other.r and \
            self.g == other.g and \
            self.b == other.b and \
            self.a == other.a
