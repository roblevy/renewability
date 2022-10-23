from datetime import datetime
import json
import os
from time import sleep
from typing import Any

from kafka import KafkaProducer

from weather.stats.arma import ArmaModel
from weather.stats.envelope import ClippingEnvelope


class WindGenerator:
    """Generate random wind speeds and write them to a Kafka topic."""

    TOPIC = "wind"
    MAX_WIND = 100
    KAFKA_BOOTSTRAP_SERVERS = os.environ["KAFKA_BOOTSTRAP_SERVERS"]

    def __init__(self):
        self.producer = KafkaProducer(bootstrap_servers=self.KAFKA_BOOTSTRAP_SERVERS)

    def generate(self):

        wind_speed_process = ArmaModel(envelope=ClippingEnvelope(0, self.MAX_WIND))

        while True:
            self._send(
                {
                    "ts": datetime.utcnow(),
                    "windspeed": next(wind_speed_process),
                }
            )
            sleep(1)

    def _send(self, message: Any):
        self.producer.send(
            topic=self.TOPIC, value=json.dumps(message, default=str).encode()
        )
