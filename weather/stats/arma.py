from collections import deque
from dataclasses import dataclass
from random import gauss
from typing import Iterable, Optional

from weather.stats.envelope import ClippingEnvelope, Envelope


@dataclass
class WeightGenerator:
    """A list of `n` weights for use in data generating functions.

    The weights start at `base / n` and tail off according to the `tailoff`
    parameter.

    The total sum of the weights is restricted to be less than one. If this
    isn't the case with the `base` and `tailoff` specified, then the weights
    are scaled down accordingly.
    """
    base: float
    tailoff: float

    def __call__(self, n: int):
        weights = list(self.base / (n + self.tailoff**i) for i in range(n))

        if weight_sum := sum(weights) >= 1:
            return [w / weight_sum for w in weights]

        return weights


@dataclass
class ArmaModel:
    """Autoregressive Moving Average model

    en.wikipedia.org/wiki/Autoregressive–moving-average_model

    A random data generating process with "stickiness" in both the value and
    the direction of the elements. In other words, the next value depends on
    the previous values, and the previous direction of travel.

    The default weight generators produce a series which is "fairly" sticky,
    but has a strong tendency to return to the mean. By default, values are
    clipped between 0 and 100.
    """

    mean = 0
    order = 5
    standard_deviation = 0.5
    autoregressive_weight_generator = WeightGenerator(1.7, 2)
    moving_average_weight_generator = WeightGenerator(1.2, 2)
    envelope: Optional[Envelope] = None

    def __post_init__(self):

        self.values = deque(maxlen=self.order)
        self.errors = deque(maxlen=self.order)

        self.ar_weights = self.autoregressive_weight_generator(self.order)
        self.ma_weights = self.moving_average_weight_generator(self.order)
        
    def __iter__(self):

        return self

    def __next__(self):

        error = gauss(mu=self.mean, sigma=self.standard_deviation)
        ar_term = self._sumproduct(self.values, self.ar_weights)
        ma_term = self._sumproduct(self.errors, self.ma_weights)

        value = error + ar_term + ma_term

        if self.envelope:
            value = self.envelope(value)

        self.values.append(value)
        self.errors.append(error)

        return value

    def _sumproduct(self, x: Iterable, y: Iterable):
        return sum(x_element * y_element for x_element, y_element in zip(x, y))
