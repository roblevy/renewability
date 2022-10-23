from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Envelope(ABC):
    """Prevent a value exceeding a minimum and maximum."""

    minimum: float
    maximum: float

    @abstractmethod
    def __call__(self, value: float):
        pass


class ClippingEnvelope(Envelope):
    """Simply clip the given value to minimum and maximum."""

    def __call__(self, value: float):

        if value < self.minimum:
            return self.minimum

        if value > self.maximum:
            return self.maximum

        return value

